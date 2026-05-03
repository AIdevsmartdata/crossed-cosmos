"""
ccm_hartnoll_frw_bridge.py

Verification: does the Connes-Consani-Moscovici (CCM) zeta-spectral-triple
dilation operator D^(λ)_log = -i u ∂_u match (up to a simple factor) the
conformal pullback of the Hislop-Longo modular Hamiltonian K_HL on the de Sitter
slow-roll sector of frw_typeII_note Cor 3.7?

Sources of verbatim formulas (no fabrication):

CCM 2511.22755 v1, eq. (5.14), p.20:
    D^(λ)_log = -i u ∂/∂u = -i ∂/∂(log u)
acting on L²([λ⁻¹, λ], du/u) with periodic boundary conditions.

CCM 2511.22755 v1, eq. (3.19), p.8:
    QW_λ(f,f) = ∫_R |f̂(t)|² · (1/π) ∂_t θ(t) dt + ...  [Weil quadratic form]
where θ is the Riemann-Siegel angular function (their eq. (3.9)).

CCM 2511.22755 v1, Theorem 1.1, p.2:
    D^(λ,N)_log = D^(λ)_log - |D^(λ)_log ξ⟩⟨δ_N|     [rank-one perturbation]

Hartnoll-Yang 2502.02661 v2, eq. (37), p.12 (CQM principal-series generators
on L²(R, dx) with weight ∆ = 1/2 + iε):
    H ψ = -i dψ/dx
    D ψ = i (x dψ/dx + ∆ ψ)
    K ψ = -i (x² dψ/dx + 2x∆ ψ)
Eq. (43): dilatation eigenfunctions  ψ_t(x) = x^{-1/2 - i(ε+t)}, with D ψ_t = t ψ_t.

frw_typeII_note frw_note.tex Cor 3.7 (de Sitter slow-roll):
    a(η) = -1/(Hη), η ∈ (-∞, 0)
    Conformal pullback unitary: (U f)(η, x) = a(η)^{-1} f(η, x) (acting on the
    scalar field by a^{-3/2} on phase-space test functions, see §3 (eq. (3.4)
    of the note); equivalently U conjugates the FRW conformal vacuum onto
    Minkowski vacuum on the conformally identified diamond M_O.
    K_FRW = U^{-1} K_HL U                              (Theorem 3.5(1))
    K_HL  = generator of the Hislop-Longo Möbius flow on the Mink diamond
            (a conformal Killing field of η_{μν}, conjugate to a boost in SO(2,4))

Setup of the comparison (this script):

(A) CCM dilation acts on the multiplicative group R*_+ via u → λ^a u, with
    e^{-i s D^(λ)_log} f(u) = f(e^{-s} u).  Spectrum: discrete 2π Z/L on
    [λ⁻¹,λ] with periodic BC, BUT before periodic-BC restriction, the
    operator on L²(R*_+, du/u) has continuous Lebesgue spectrum on R.
    (Periodic BC are an IR cutoff, not a structural change.)

(B) HY dilation D = i(x ∂_x + ∆) on L²(R_+, dx) is unitarily equivalent to
    -i ∂_y on L²(R, dy) under x = e^y, ψ → e^{y/2} ψ. Continuous Lebesgue
    spectrum on R.

(C) FRW K_FRW = U^{-1} K_HL U on the de Sitter conformal diamond.
    By Hislop-Longo, K_HL on the Mink diamond is conjugate to the boost
    generator -i (x ∂_t + t ∂_x) (extended to a Möbius generator that fixes
    the diamond tips). Spectrum: continuous Lebesgue on R.

The candidate bridge is: under the de Sitter conformal time change
    η = -1/(Hλ),  (the standard slow-roll variable),
the "scaling" of η ↦ λη corresponds to a multiplicative Lorentz dilation
of η at the comoving observer. Does the Möbius generator K_HL pull back
to the multiplicative dilation -i η ∂_η?

We check this symbolically.
"""

import sympy as sp


def step1_ccm_dilation():
    """CCM scaling operator D = -i u ∂_u acting on f(u) on R*_+."""
    print("\n=== STEP 1. CCM dilation operator (eq. 5.14) ===")
    u, s = sp.symbols('u s', positive=True, real=True)
    f = sp.Function('f')
    # D acts on f(u) as -i u f'(u)
    Df = -sp.I * u * sp.diff(f(u), u)
    print("D f(u) = -i u ∂_u f(u) =", Df)
    # eigenfunctions: u^{i t} are eigenstates with eigenvalue t  (because
    # under v=log u, du/u = dv, D = -i ∂_v, eigenfns e^{itv} = u^{it} ↔ eigval t)
    t = sp.symbols('t', real=True)
    psi = u**(sp.I * t)
    Dpsi = -sp.I * u * sp.diff(psi, u)
    Dpsi_simpl = sp.simplify(Dpsi - t * psi)
    print(f"  on ψ_t(u) = u^(it):  D ψ_t - t ψ_t  =  {Dpsi_simpl}")
    assert Dpsi_simpl == 0, "CCM dilation eigenvalue check failed"
    print("  -> eigenvalues = t (continuous Lebesgue on R*_+); discrete 2πZ/L")
    print("     after periodic BC on [λ⁻¹, λ]")
    return Df


def step2_hartnoll_yang_dilation():
    """Hartnoll-Yang CQM dilation D = i (x ∂_x + ∆), eq. (37), with ∆ = 1/2 + iε."""
    print("\n=== STEP 2. Hartnoll-Yang dilation (eq. 37) ===")
    x, t, eps = sp.symbols('x t epsilon', real=True, positive=True)
    Delta = sp.Rational(1, 2) + sp.I * eps
    # HY eq. (43): ψ_t(x) = x^{-1/2 - i(ε+t)} ⇒ D ψ_t = t ψ_t
    psi_t = x**(-sp.Rational(1, 2) - sp.I*(eps + t))
    Dpsi = sp.I * (x * sp.diff(psi_t, x) + Delta * psi_t)
    diff = sp.simplify(Dpsi - t * psi_t)
    print(f"  ψ_t(x) = x^(-1/2 - i(ε+t))")
    print(f"  D ψ_t - t ψ_t  =  {diff}")
    assert diff == 0, "HY dilation eigenvalue check failed"
    print("  -> eigenvalues = t (continuous on R*_+, plane waves under x=e^y)")


def step3_dS_conformal_dilation():
    """
    Cor 3.7 of frw_note: a(η) = -1/(Hη). Test the candidate bridge:
    is the M\"obius / boost generator on the conformally identified Mink diamond
    equivalent to the multiplicative dilation -i η ∂_η on the conformal-time
    coordinate of the dS comoving worldline?
    """
    print("\n=== STEP 3. dS conformal-time dilation operator ===")
    eta, lam, t, H, x = sp.symbols('eta lambda t H x', real=True)

    # Substitution η → λη is the dS scaling symmetry of a(η) = -1/(Hη):
    a = -1/(H*eta)
    a_lam = a.subs(eta, lam*eta)
    a_check = sp.simplify(a_lam - a/lam)
    print(f"  a(η) = -1/(Hη);  a(λη) - a(η)/λ  =  {a_check}")
    assert a_check == 0, "dS dilation invariance check failed"
    print("  -> a(λη) = a(η)/λ.  η-dilation generator: K_dil = -i η ∂_η.")

    # Hislop-Longo modular flow on a Mink diamond is the M\"obius flow whose
    # generator is, in standard form (see Hislop-Longo 1982 eq. 4.7, or
    # Brunetti-Guido-Longo 1993; not a free parameter):
    #    K_HL = (π/r) [ (R²-η²-r²)/2 · ∂_η  -  rη · ∂_r ]   (with R = diamond radius)
    # at η=0 slice; R the radius of the ball.  This is conjugate to a boost
    # generator in SO(2,4).
    #
    # Question: does K_HL restricted to the comoving worldline (r = 0)
    # reduce to a multiplicative dilation in η?
    #
    # On the comoving worldline r = 0:
    R = sp.symbols('R', positive=True)
    K_HL_eta = sp.pi/R * (R**2 - eta**2 - 0)/2  # coefficient of ∂_η at r=0
    print(f"  K_HL on r=0 worldline ~ {K_HL_eta} · ∂_η  +  O(r)")
    # Compare to dilation generator -i η ∂_η:
    # K_HL coefficient is  (π/(2R)) (R² - η²),  whereas multiplicative
    # dilation has coefficient η (mod a sign).  These are not proportional:
    # the M\"obius generator quadratic in η, dilation linear.

    # Try to find a function f(η) so that f(η) = c η · (R²-η²)/(2R²)  has
    # constant ratio. The ratio  R²-η²  /  η   is η-dependent ⇒ no constant c.
    ratio = sp.simplify((R**2 - eta**2)/eta)
    print(f"  (R²-η²)/η = {ratio}  (η-dependent ⇒ NOT proportional to dilation)")

    # Conclusion: the M\"obius generator on a comoving worldline is NOT a
    # multiplicative dilation. It is a dilation only at the special point
    # η = R (where it vanishes — diamond tip) or in an asymptotic limit.

    print("\n  CONCLUSION step 3:")
    print("  K_HL is QUADRATIC in η (M\\\"obius); a multiplicative dilation -iη∂_η")
    print("  is LINEAR in η. They CANNOT differ by a constant factor.")
    print("  The dS scaling η→λη is a SYMMETRY of the background a(η), but")
    print("  is NOT the modular flow of the diamond. Modular flow = boost-like.")


def step4_compare_spectra():
    """
    All three operators have continuous Lebesgue spectrum on R, but only
    the FRW K_FRW has a substantive type II_∞ classification.  CCM's D^(λ)_log
    has DISCRETE spectrum {2πn/L : n ∈ Z} after periodic BC ⇒ structurally
    different from the geometric Tomita-Takesaki setup.
    """
    print("\n=== STEP 4. Spectral comparison ===")
    print("  CCM D^(λ)_log on L²([λ⁻¹,λ],du/u) with periodic BC:")
    print("    spectrum = {2πn/L : n ∈ Z},  L = 2 log λ   (DISCRETE)")
    print("    rank-one perturbation D^(λ,N)_log → spectrum approximating")
    print("    Riemann zeros γ_n  ⇒  countable discrete subset of R_+.")
    print()
    print("  HY CQM D = i(x∂_x + ∆) on L²(R_+, dx):")
    print("    spectrum = R (continuous Lebesgue, plane waves under x=e^y)")
    print("    Wavefunction in dilatation basis ∝ ξ(1/2 + it),")
    print("    vanishing at the Riemann/automorphic zeros (an absorption ")
    print("    spectrum in the Connes sense, not a Hilbert-Pólya operator).")
    print()
    print("  FRW K_FRW = U^{-1} K_HL U on dS comoving diamond:")
    print("    spectrum = R (continuous Lebesgue, simple per spherical mode)")
    print("    K_FRW is unitarily equivalent to the boost generator in SO(2,4),")
    print("    NOT to a dilation in conformal time η.")
    print()
    print("  Connes 1973 cocycle invariance ⇒ Spec(K_FRW) is invariant under")
    print("  any inner perturbation; cannot be deformed to {γ_n}.")


def step5_verdict():
    print("\n=== STEP 5. VERDICT ===")
    print("  (a) CCM and FRW are STRUCTURALLY DIFFERENT spaces:")
    print("      CCM: L²([λ⁻¹,λ], du/u), 1D number-theoretic scaling space.")
    print("      FRW: L²(R³, dμ_diamond) ⊗ Fock, 4D geometric vN algebra.")
    print()
    print("  (b) Dilation operators do NOT match:")
    print("      D^(λ)_log = -i η ∂_η  is multiplicative scaling (linear in η).")
    print("      K_HL is M\\\"obius generator (quadratic in η). They differ at")
    print("      every order in η ≠ 0 — not a rescaling, not a unitary equiv.")
    print()
    print("  (c) The dS scaling η → λη is a SYMMETRY of a(η) but NOT of the")
    print("      modular flow on a diamond. The diamond breaks dilation by")
    print("      its tips η_i, η_f, leaving only the M\\\"obius flow as modular.")
    print()
    print("  (d) Hartnoll-Yang's BKL setting (η→0 singular regime) is the")
    print("      OPPOSITE limit to FRW comoving diamond (η_i, η_f bounded away")
    print("      from η=0): the HY 'end of time' BKL Wheeler-DeWitt automorphic")
    print("      construction is precisely the regime EXCLUDED by Cor 3.7 and")
    print("      by the Big Bang obstruction in Question 4 of frw_note.")
    print()
    print("  ⇒ NO SUBSTANTIVE BRIDGE in the modular-spectrum sense.")
    print("    The Piste 4 NO-GO (continuous Lebesgue vs discrete RH zeros)")
    print("    extends verbatim to CCM 2511.22755 and to HY 2502.02661.")


if __name__ == "__main__":
    step1_ccm_dilation()
    step2_hartnoll_yang_dilation()
    step3_dS_conformal_dilation()
    step4_compare_spectra()
    step5_verdict()
    print("\n[All sympy assertions passed.]")
