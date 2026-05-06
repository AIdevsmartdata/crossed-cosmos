#!/usr/bin/env python3
"""
M161B Sub-task 1: Enumerate imaginary quadratic fields with class number h=2,
discriminant D in [-100, 0). Verify class numbers via direct enumeration of
reduced binary quadratic forms (Gauss's algorithm).

Reduced form (a,b,c) with disc = b^2 - 4ac = D (D < 0):
  - 0 < a, 0 < c
  - |b| <= a <= c
  - if |b| = a or a = c, then b >= 0
  - gcd(a,b,c) = 1 (primitive form)

Number of reduced primitive forms = class number h(D).

Reference: Cox, "Primes of the Form x^2 + ny^2", 1989, Theorem 2.8.
"""

import math
from math import gcd

def reduced_forms(D):
    """Enumerate reduced primitive forms of discriminant D."""
    assert D < 0 and D % 4 in (0, 1), f"Invalid discriminant D={D}"
    forms = []
    # |b| <= a, b^2 - 4ac = D, c = (b^2 - D)/(4a)
    # a <= sqrt(|D|/3) for reduced form
    abs_D = -D
    a_max = int(math.isqrt(abs_D // 3)) + 1
    for a in range(1, a_max + 1):
        # b ranges: |b| <= a, and b ≡ D (mod 2)
        b_start = -a
        if a == 1:  # adjust for the boundary later
            b_start = 0
        for b in range(-a, a + 1):
            if (b * b - D) % (4 * a) != 0:
                continue
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            # Check reduced conditions
            if c == a and b < 0:
                continue
            if abs(b) == a and b < 0:
                continue
            # Check primitivity: gcd(a, b, c) = 1
            if gcd(gcd(a, abs(b)), c) != 1:
                continue
            forms.append((a, b, c))
    return forms

def class_number(D):
    """Return h(D) by counting reduced primitive forms."""
    return len(reduced_forms(D))

# Enumerate D in [-100, 0) with D ≡ 0 or 1 (mod 4)
print("=" * 70)
print("M161B Sub-task 1: Imaginary quadratic fields with h=2 below |D|=100")
print("=" * 70)
print()
print(f"{'D':>5} {'h(D)':>4}  Reduced forms")
print("-" * 70)

h2_fields = []
all_h_data = {}
for D in range(-1, -200, -1):
    if D % 4 not in (0, 1):
        continue
    forms = reduced_forms(D)
    h = len(forms)
    all_h_data[D] = h
    if h <= 5 and D >= -100:
        forms_str = ", ".join([f"({a},{b},{c})" for a,b,c in forms])
        print(f"{D:>5} {h:>4}  {forms_str}")
    if h == 2:
        h2_fields.append((D, forms))

print()
print(f"All h=2 fields with D in [-200, 0):")
print(f"{'D':>6} {'forms':>10}  field K")
print("-" * 70)

# Field structure for each D:
def field_label(D):
    """Return label Q(sqrt(d)) for fundamental discriminant D."""
    if D % 4 == 0:
        d_sqfree = D // 4
        return f"Q(sqrt({d_sqfree}))"
    else:
        return f"Q(sqrt({D}))"

target_D = [-15, -20, -24, -35, -40, -88]  # primary mission targets

for D, forms in h2_fields:
    if D < -100:
        continue
    label = field_label(D)
    forms_str = ", ".join([f"({a},{b},{c})" for a,b,c in forms])
    star = " <-- TARGET" if D in target_D else ""
    print(f"{D:>6}  {label:>14}  {forms_str}{star}")

print()
print("Mission targets verification:")
print("-" * 70)
for D in target_D:
    if D in all_h_data:
        h = all_h_data[D]
        forms = reduced_forms(D)
        forms_str = ", ".join([f"({a},{b},{c})" for a,b,c in forms])
        ok = "OK" if h == 2 else f"FAIL h={h}"
        label = field_label(D)
        print(f"  D={D:>4}  h(D)={h}  {label:>14}  {forms_str}  [{ok}]")
    else:
        print(f"  D={D:>4}  not enumerated")

# Cross-check with PARI via cypari2
print()
print("PARI cross-check (qfbclassno):")
print("-" * 70)
try:
    import cypari2
    pari = cypari2.Pari()
    for D in target_D:
        h_pari = int(pari.qfbclassno(D))
        h_py = all_h_data.get(D, "?")
        match = "MATCH" if h_pari == h_py else "MISMATCH"
        print(f"  D={D:>4}  h_python={h_py}  h_pari={h_pari}  [{match}]")
except ImportError:
    print("  cypari2 not available")
