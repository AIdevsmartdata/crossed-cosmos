# defence_memo.md — Team B response to the hostile reviewer

**Objection (paraphrased).** *"The crossed-product construction of CLPW~2023
and DEHK~2024--2025 is proven for static de Sitter patches (CLPW) and for
multi-observer QRFs on fixed Killing-horizon backgrounds (DEHK). It has not
been established for generic FLRW with matter. Invoking it as a unifying
principle for a DESI-driven framework paper is therefore premature: the
regime where DESI, Cassini, and LSST Y10 actually constrain the model is not
a static patch, and the observer-dependence you are exporting is not proven
to survive in that regime."*

## Honest response

We partially concede, and we restrict the scope of Hypothesis B accordingly.

### What we concede

1. **Matter-era and radiation-era FLRW is NOT covered.** No theorem in
   CLPW, DEHK, Faulkner--Speranza, or Kirklin establishes the type-II
   crossed-product on a generic time-dependent FLRW background with
   non-zero matter sources. The modular flow that defines the crossed
   product requires a stationary (or at least quasi-stationary) horizon;
   matter-era FLRW has no such horizon at the subregion of interest.
2. **The EDE pre-recombination sector (A4, $\phi$ axion at $z_c\sim 3500$)
   is outside Hypothesis~B's defensible scope.** The Poulin--Smith 2026
   $f_{\rm EDE}=0.09\pm0.03$ result is a matter-era statement and cannot
   be given an observer-frame re-reading with current tools.
3. **BBN-level $\xi_\chi$ bounds (Wolf~2025) are similarly out of scope.**
   They apply at a redshift where there is no static-patch asymptote.
4. **A3 (Cryptographic Censorship) cosmological transposition remains a
   working conjecture** regardless of Hypothesis~B. B re-reads A3 as a
   horizon condition on the observer's subregion, but the pseudo-Riemannian
   modular reconstruction needed to make the re-reading a theorem is not
   known (GROUND\_TRUTH.md Part~E.1; PRINCIPLES.md §8; item 10 of
   INDEX.md §4 "rejected approaches").

### What we defend: the late-time quasi-de-Sitter limit

Hypothesis B is defensible in exactly the regime where DESI~DR2 (at
$\Omega_\Lambda\simeq 0.7$), Cassini (local, solar-system), LSST~Y10
($0 < z \lesssim 2$), Euclid ($z\lesssim 2$), and the NMC perturbation
signature of §3.7 live. In this regime the following four anchors hold:

1. **Static-patch asymptote.** A late-time geodesic observer at
   $\Omega_\Lambda \gtrsim 0.7$ sees the comoving Hubble diamond approach
   a de Sitter static patch on the Hubble time; the residual deviation
   is $O(1-\Omega_\Lambda)$. CLPW~2023 applies to this asymptote, with
   corrections controlled by the same small parameter that controls the
   deviation of $w$ from $-1$.
2. **Quasi-stationary modular flow.** The adiabatic theorem for modular
   flow (Longo--Witten constructions used in CLPW §2) tolerates a slow
   drift in the background; the DESI~DR2 inferred $|\dot H|/H^2 \sim O(1)$
   at the reconstruction pivot is at the edge but not beyond what the
   adiabatic crossed-product tolerates. This is not a theorem, but it is
   on the same footing as the $|\dot H|/H^2$ assumptions implicit in the
   Faulkner--Speranza non-perturbative GSL.
3. **Scope match.** Every quantitative prediction of §3.1, §3.5, §3.6,
   and §3.7 is a late-time-observer measurement (solar system; $z<2$
   surveys; late linear perturbations at sub-horizon quasi-static scales).
   No §3 quantitative claim reaches into the matter era that Hypothesis~B
   does not cover.
4. **The pre-recombination A4 sector is a separate claim.** The axion-
   EDE phenomenology (§3.2) is inherited wholesale from Poulin--Smith 2026
   and does not invoke the crossed product even in Hypothesis~A's reading.
   Hypothesis~B therefore loses nothing by scoping out EDE; it simply
   preserves the paper's existing separation between late-time
   (observer-dependent) and pre-recombination (background-level)
   statements.

### Net posture

Hypothesis~B is offered as a **late-time unifying hypothesis** — the
algebraic story of A1--A2 is not a cosmetic preamble to §3, it is the
frame in which A4/A5/A6 should be read **at the redshifts the framework
is actually falsifiable**. The paper's §3.2 EDE sector and the BBN-level
$\xi_\chi$ scaling are kept as matter-era inputs that Hypothesis~B
neither needs nor explains; we flag this scope restriction in §1.5 itself
(see `draft_section_1_5_B.tex` part (iv)) and in the "Structural
limitations" list.

### Survives the objection?

**Partially.** The objection is correct on matter-era FLRW; Hypothesis~B
does not rescue that regime, and we do not pretend it does. The objection
fails, however, against a scoped Hypothesis~B that restricts itself to the
quasi-dS late-time limit — which is the only regime in which the paper's
quantitative DESI/Cassini/LSST Y10 predictions live. The residual honest
cost is that the §1.5 framing becomes "observer-dependent cosmology in the
late-time limit", not "observer-dependent cosmology tout court". That cost
is acceptable given that no weaker framing defensibly covers the DESI
regime, and no stronger framing is theorem-backed.

### If the owner picks Team A over Team B

Nothing in this defence forbids it. Hypothesis~A (whatever the other
unifying thesis turns out to be) may cover the matter era more
cleanly. Our posture is that Hypothesis~B is honest and defensible
within its stated scope, not that it dominates A.
