---
name: M20 Theoretical derivation — Steinberg-edge eigenvalue via Hecke character theory
date: 2026-05-06
agent: M20 (Sonnet 4.6, validation)
---

# Theoretical Derivation of the Eigenvalue Identity via Hecke Characters

## Setup

Let f be a CM newform of weight k, level N, nebentypus chi.
Let K = Q(sqrt(-D)) be the imaginary quadratic CM field.
Let psi be the Hecke (Groessencharakter) character of K of infinity-type (k-1, 0) such that
f = theta_psi (i.e., f is obtained by automorphic induction from psi).

The Fourier coefficients of f are given (classically, see e.g. Shimura 1971, "Introduction to
the Arithmetic Theory of Automorphic Functions", and Katz 1978 CM literature) by:

  a(n) = sum_{Norm(a)=n, a coprime to conductor(psi)} psi(a)

For a prime integer p:
- If p SPLITS in K: p = pi * pi_bar (two distinct primes), and
    a(p) = psi(pi) + psi(pi_bar)
  (Two terms, since there are two prime ideals of K above p with norm p.)

- If p is INERT in K: p remains prime in O_K, and
    a(p) = 0
  (No prime ideal of norm p, only one of norm p^2.)

- If p RAMIFIES in K: p * O_K = pi^2 (one prime ideal pi with Norm(pi) = p), and:
    a(p) = psi(pi)  [if pi is coprime to conductor(psi)]
    a(p) = 0         [if pi | conductor(psi)]

## Unitarity condition on psi

A Hecke character psi of K of infinity-type (k-1, 0) satisfies: for all x in K* embedded
into the ideles with x in K_{inf}:
  psi(x) = (x/|x|)^(k-1) = (x / bar(x))^{(k-1)/2}  * |x|^((k-1)/2) ... (more precisely)

The KEY property is: for any FINITE-order part of psi (at a prime pi of K with pi coprime
to conductor(psi)):
  |psi(pi)|^2 = psi(pi) * psi_conj(pi) = psi(pi) * psi(bar(pi))

For a ramified prime pi: bar(pi) = pi (since pi = bar(pi) in Z[i], e.g. for p=2: bar(1+i) = 1-i,
but (1+i) and (1-i) differ by the unit i, so they define the SAME ideal in Z[i]). Therefore
pi = bar(pi) as ideals.

Under the Hecke character normalization for weight-k automorphic form, the relation:
  psi(pi) * bar{psi}(pi) = N(pi)^(k-1) = p^(k-1)

This gives |psi(pi)|^2 = p^(k-1), hence |psi(pi)| = p^((k-1)/2).

Since a(p) = psi(pi) (when pi is coprime to conductor(psi)):
  |a(p)| = p^((k-1)/2).

## This is EQUIVALENT to the "saturation of Ramanujan bound at bad primes"

For p | N (a bad prime for the newform), the Ramanujan-Petersson bound takes the form:
  |a(p)| <= p^((k-1)/2)

This is NOT the Deligne bound (which is for p coprime to N and gives |a_p| <= 2*p^((k-1)/2)).
M13's SUMMARY.md states "upper edge of Deligne-Ramanujan |a_p| <= 2*p^((k-1)/2)" which is
IMPRECISE: the relevant bound for p | N is |a_p| <= p^((k-1)/2) (no factor of 2), so
4.5.b.a with a_2 = -4 = -p^((k-1)/2) is at EXACT equality of the BAD-PRIME bound,
not half the Deligne bound.

The identity is equivalently:
  a(p)^2 = p^(k-1)  [when a(p) real, e.g. chi(p) = 1 or chi a character of K]

For 4.5.b.a: (-4)^2 = 16 = 2^4 = 2^(5-1). Confirmed.

## Numerical verification (sympy-compatible)

k = 5, p = 2:
  p^((k-1)/2) = 2^((5-1)/2) = 2^2 = 4
  a_2 = -4
  |a_2| = 4 = 2^2 = p^((k-1)/2). MATCH.
  a_2^2 = 16 = 2^4 = p^(k-1). MATCH.
  slope: v_2(a_2) = v_2(4) = 2 = (k-1)/2. This IS the "critical slope" condition.

## Local Langlands perspective

Under the local Langlands correspondence (for GL_2/Q_p), the local automorphic representation
pi_p of the newform f at a prime p | N is determined by the local Galois representation rho_p.

For a CM newform f_psi with p ramified in K (and psi unramified at pi):
  rho_p|_{G_{Q_p}} = Ind_{G_{K_p}}^{G_{Q_p}}(psi_p)

where psi_p is the local character of K_p = Q_p(sqrt(-D)) and G_{K_p} is the local Galois group.
Since K_p/Q_p is a ramified extension (p ramifies in K), this induction gives a RAMIFIED
PRINCIPAL SERIES representation (not Steinberg, not supercuspidal).

The Hecke polynomial at p is (1 - a_p * X) (degree 1, since the local representation contributes
one Frobenius eigenvalue psi(pi) in the non-archimedean L-factor).
Specifically: L_p(f, s) = (1 - a_p * p^{-s})^{-1}

This degree-1 structure is confirmed for 4.5.b.a by LMFDB: characteristic polynomial at p=2
is T + 4 (degree 1), confirming the ramified principal series interpretation.

## On the term "Steinberg-edge"

The term "Steinberg representation" in p-adic group theory refers to the SPECIAL representation
of GL_2(Q_p): a non-split extension of the trivial and the absolute value character. This arises
when p || N (p exactly divides N) and the local character chi_p is unramified.

The "Steinberg-edge" as used by M13 is NOT the same as the Steinberg representation (which
corresponds to a_p = +/- p^{k/2-1} * chi(p)^{1/2} for appropriate twist). M13 uses
"Steinberg-edge" to mean "saturation of the bad-prime Ramanujan bound |a_p| = p^{(k-1)/2}."

This is a NON-STANDARD use of terminology. The standard terminology would be:
- "Critical slope at p" (slope = v_p(a_p) = (k-1)/2)
- "Bad-prime Ramanujan saturation"
- OR: "theta-critical weight-k CM point" on the eigencurve

## References for standard form of this result

The result a(p) = psi(pi) for CM newforms at ramified primes where psi is unramified at pi
follows from:
1. Shimura's fundamental work on modular forms of CM type (1971/1973)
2. Ribet's 1977 paper: "Galois representations attached to eigenforms with Nebentypus"
   (in Modular Functions of One Variable V, LNM 601)
3. The classical theory of theta series and Hecke characters — standard reference:
   The result is stated (in equivalent form) in Cohen-Strömberg "Modular Forms: A Classical
   Approach" (AMS GSM 179, 2017).
4. Li, W.C. 1975, "Newforms and Functional Equations" (Math. Ann. 212, 285-315) for the
   local theory at ramified primes.

NONE of these references use the terminology "Steinberg-edge identity." The result itself
(|a_p| = p^((k-1)/2) for CM newforms at ramified primes with unramified Hecke character) is
STANDARD and KNOWN to experts.
