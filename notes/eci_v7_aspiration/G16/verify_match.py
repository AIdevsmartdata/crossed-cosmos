"""
verify_match.py — G1.6 Sign Resolution
ECI v7-R&D | 2026-05-04

PURPOSE
-------
Verify the relationship between H2's 3hat2(5) eigenvalues and LMFDB 4.5.b.a.

FINDINGS (G1.6.A/B/C/D summary):
  1. H2's formula for 3hat2(5) is correctly transcribed from NPP20 App D.
  2. The sign pattern lambda_H2(p) / a_LMFDB(p) = chi_21(p) for all tested primes.
  3. This is NOT a genuine twist (chi_21 has conductor 21, twist would be level 1764).
  4. It is a Groessencharacter normalisation ambiguity in the CM form.
  5. The CM eigenvalue 2*Re((a+bi)^(k-1)) for p = a^2+b^2 is unique up to the choice
     of which of the two Gaussian primes above p is "canonical."
  6. For p=13 (=3^2+2^2) and p=29 (=5^2+2^2): both 2*Re((odd+even*i)^4) and
     2*Re((even+odd*i)^4) are equal in absolute value but the task prompt lists them
     with opposite signs. The CM formula gives -238 for ALL choices of pi above 13;
     a value of +238 is impossible from 2*Re(pi^4).
  7. CONCLUSION: the task prompt's LMFDB a(p) values for p=13 and p=29 are incorrect.
     The correct LMFDB 4.5.b.a values (from CM theory) are a(13)=-238, a(29)=+82,
     which match H2's eigenvalues exactly with NO sign discrepancy.

REQUIRES: sympy (for exact arithmetic), no network access needed.
"""

# ============================================================
# Section 1: CM eigenvalue computation from first principles
# ============================================================

def sum_of_two_squares(p):
    """Find a, b >= 1 with a^2 + b^2 = p, a odd."""
    for a in range(1, int(p**0.5) + 1):
        b_sq = p - a * a
        b = int(b_sq**0.5)
        if b * b == b_sq and b > 0:
            if a % 2 == 1:
                return a, b
            else:
                return b, a  # swap so a is odd
    return None, None


def cm_eigenvalue_4_5_b_a(p):
    """
    Compute a(p) for the CM newform of weight 5, level 4, nebentypus chi_4,
    with CM by Q(i).

    For p ≡ 1 mod 4 (split in Q(i)):
      p = a^2 + b^2 with a odd, b even.
      The Groessencharacter psi satisfies psi(pi) = pi^4 for the canonical
      Gaussian prime pi above p.  The q-expansion coefficient is:
        a(p) = psi(pi) + psi(pi_bar) = 2 * Re(pi^4)
      where the choice of pi vs pi_bar determines the sign.

    For p ≡ 3 mod 4 (inert in Q(i)): a(p) = 0.

    NOTE: The specific sign of a(p) depends on the canonical choice of pi.
    For the LMFDB normalisation of 4.5.b.a, the canonical pi is chosen so
    that pi ≡ 1 mod (2+2i) in Z[i] (primary Gaussian integer).
    Both pi = a+bi and pi = b+ai give the SAME 2*Re(pi^4) when a^2+b^2=p,
    since (a+bi)^4 and (b+ai)^4 differ only in their imaginary parts.
    The real part depends only on |a^2 - b^2| and the relative sign, not on
    which is called a vs b.
    """
    if p % 4 != 1:
        return 0
    a, b = sum_of_two_squares(p)
    if a is None:
        return None
    # Ensure a is odd (as found above)
    # Compute (a + b*i)^4
    re2 = a*a - b*b
    im2 = 2 * a * b
    re4 = re2*re2 - im2*im2
    return 2 * re4


# ============================================================
# Section 2: Kronecker symbol for character search
# ============================================================

def kronecker(a, n):
    """Compute Kronecker symbol (a|n) iteratively."""
    if n == 0:
        return 1 if abs(a) == 1 else 0
    if n == 1:
        return 1
    if n < 0:
        result = kronecker(a, -n)
        if a < 0:
            result = -result
        return result
    if a == 0:
        return 0 if n > 1 else 1
    # Factor out powers of 2
    e = 0
    m = n
    while m % 2 == 0:
        m //= 2
        e += 1
    result = 1
    if e > 0:
        if a % 2 == 0:
            k2 = 0
        elif abs(a) % 8 in (1, 7):
            k2 = 1
        else:
            k2 = -1
        result = k2 ** e
        if result == 0:
            return 0
    # Jacobi symbol for odd part
    a_rem = a % m
    if a_rem == 0:
        return 0 if m > 1 else 1
    j = 1
    while a_rem != 0:
        while a_rem % 2 == 0:
            a_rem //= 2
            if m % 8 in (3, 5):
                j = -j
        a_rem, m = m, a_rem
        if a_rem % 4 == 3 and m % 4 == 3:
            j = -j
        a_rem = a_rem % m
    if m == 1:
        return j * result
    else:
        return 0


# ============================================================
# Section 3: Main verification
# ============================================================

def main():
    SEP = "=" * 70
    sep = "-" * 70

    print(SEP)
    print("  G1.6 SIGN RESOLUTION — verify_match.py")
    print("  ECI v7-R&D | 2026-05-04")
    print(SEP)

    # The five primes tested in H2
    primes = [5, 13, 17, 29, 37]

    # H2's eigenvalues for 3hat2(5) (from closure_table.md, sympy-verified)
    h2_lambda = {5: -14, 13: -238, 17: 322, 29: 82, 37: 2162}

    # LMFDB 4.5.b.a values as stated in the task prompt
    task_lmfdb = {5: -14, 13: 238, 17: 322, 29: -82, 37: 2162}

    print()
    print("  Step 1: CM eigenvalue computation from first principles")
    print(sep)
    print(f"  {'p':>4}  {'a=odd':>6}  {'b=even':>6}  {'2*Re(pi^4)':>12}  "
          f"{'H2 lambda':>12}  {'Task LMFDB':>12}  {'Match H2?':>10}")
    print(f"  {'-'*4}  {'-'*6}  {'-'*6}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*10}")

    cm_vals = {}
    for p in primes:
        val = cm_eigenvalue_4_5_b_a(p)
        a, b = sum_of_two_squares(p)
        cm_vals[p] = val
        match_h2 = (val == h2_lambda[p])
        match_task = (val == task_lmfdb[p])
        a_str = str(a) if a else "N/A"
        b_str = str(b) if b else "N/A"
        print(f"  {p:>4}  {a_str:>6}  {b_str:>6}  {val:>12}  "
              f"{h2_lambda[p]:>12}  {task_lmfdb[p]:>12}  {str(match_h2):>10}")

    print()
    print("  Step 2: Check if +238 is achievable for p=13")
    print(sep)
    any_238 = False
    for a in range(-5, 6):
        for b in range(-5, 6):
            if a*a + b*b == 13:
                re2 = a*a - b*b
                im2 = 2*a*b
                re4 = re2*re2 - im2*im2
                val = 2 * re4
                if val == 238:
                    any_238 = True
                    print(f"  ({a:+d}{b:+d}i)^4 -> 2*Re = {val}  [WOULD MATCH TASK LMFDB]")
    if not any_238:
        print("  For p=13: NO Gaussian prime gives 2*Re(pi^4) = +238.")
        print("  The value +238 is IMPOSSIBLE from the CM formula 2*Re(pi^4).")
        print("  Therefore: a(13)_LMFDB = +238 as stated in the task prompt is INCORRECT.")

    print()
    print("  Step 3: Check if -82 is achievable for p=29")
    any_m82 = False
    for a in range(-7, 7):
        for b in range(-7, 7):
            if a*a + b*b == 29:
                re2 = a*a - b*b
                im2 = 2*a*b
                re4 = re2*re2 - im2*im2
                val = 2 * re4
                if val == -82:
                    any_m82 = True
                    print(f"  ({a:+d}{b:+d}i)^4 -> 2*Re = {val}  [WOULD MATCH TASK LMFDB]")
    if not any_m82:
        print("  For p=29: NO Gaussian prime gives 2*Re(pi^4) = -82.")
        print("  The value -82 is IMPOSSIBLE from the CM formula 2*Re(pi^4).")
        print("  Therefore: a(29)_LMFDB = -82 as stated in the task prompt is INCORRECT.")

    print()
    print("  Step 4: Corrected LMFDB 4.5.b.a eigenvalues")
    print(sep)
    print("  The correct a(p) values for 4.5.b.a (from CM theory) are:")
    print(f"  {'p':>4}  {'a(p) correct':>14}  {'H2 lambda':>12}  {'Exact match?':>12}")
    print(f"  {'-'*4}  {'-'*14}  {'-'*12}  {'-'*12}")
    all_match = True
    for p in primes:
        cv = cm_vals[p]
        h2v = h2_lambda[p]
        match = (cv == h2v)
        if not match:
            all_match = False
        print(f"  {p:>4}  {cv:>14}  {h2v:>12}  {str(match):>12}")

    print()
    if all_match:
        print("  RESULT: H2's 3hat2(5) eigenvalues EXACTLY MATCH the CM values.")
        print("  The corrected LMFDB 4.5.b.a eigenvalues agree 5/5 with H2.")
    else:
        print("  RESULT: Some mismatch remains — further investigation needed.")

    print()
    print("  Step 5: Character search — what chi satisfies chi(p) = task_ratio(p)?")
    print(sep)
    print("  task_ratio(p) = task_LMFDB(p) / H2_lambda(p):")
    for p in primes:
        ratio = task_lmfdb[p] // h2_lambda[p]
        print(f"    p={p}: {task_lmfdb[p]} / {h2_lambda[p]} = {ratio}")

    print()
    print("  chi_21 = Kronecker symbol (21|.) values:")
    for p in primes:
        c21 = kronecker(21, p)
        ratio = task_lmfdb[p] // h2_lambda[p]
        print(f"    chi_21({p}) = (21|{p}) = {c21}  [task ratio = {ratio}, match: {c21==ratio}]")

    print()
    print("  Step 6: Could the discrepancy be a genuine twist?")
    print(sep)
    print("  If 3hat2(5) = 4.5.b.a ⊗ chi_21 (genuine twist), then:")
    print("    Level of twist: 4 * 21^2 = 1764  (vs. level 4 for both forms)")
    print("    But H2's 3hat2(5) lives on Gamma(4) = level 4. Contradiction.")
    print("  Therefore: even IF the task LMFDB values were correct, a genuine")
    print("  twist interpretation would be impossible since chi_21 has conductor 21")
    print("  and the twisted form would have level 1764, not 4.")
    print()
    print("  FINAL VERDICT: See sign_resolution.md")

    print()
    print(SEP)
    print("  verify_match.py COMPLETE")
    print(SEP)


if __name__ == "__main__":
    main()
