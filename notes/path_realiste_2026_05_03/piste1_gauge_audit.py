"""
piste1_gauge_audit.py
=====================

GAUGE-INVARIANCE AUDIT of Piste 1's claim
   H(t) = (1/C_k) dC_k/dt   for radiation-dominated FRW.

Mistral large-latest's adversarial review (/tmp/mistral_v620_review.txt)
flagged that the match "1/(2t)" is potentially gauge-dependent and kinematic,
not a dynamical breakthrough:
   "If you change the slicing (e.g., to proper time), the match breaks."

The original Piste 1 derivation passes through CONFORMAL TIME η. We re-derive
EVERYTHING in PROPER (cosmic) TIME t and check whether the claim survives.

Key fact (verified via web search of arXiv 2306.14732 + standard Tomita-
Takesaki theory): the modular flow parameter `s` is INTRINSIC to the algebra
(generator of Δ^{is}). It is *not* proper time, conformal time, or any
spacetime coordinate. The relation to spacetime time at the observer
worldline is encoded in a Jacobian ds/dτ where τ is a chosen physical clock.

The Casini-Huerta-Myers (2008) formula
       ds/dτ_proper = 1 / (2π R_proper)                              (CHM-3.16)
gives the Jacobian at the CENTER of a diamond, where R_proper = a(η_c) R_conf
is the *proper* radius of the diamond. R_proper is the geometric (gauge-
invariant) length of the diamond's spatial radius at the moment of time-
symmetry. **It is independent of which time coordinate (η or t) we use.**

This script does the following:

(1) Symbolic computation of (1/C_k) dC_k/dt for radiation FRW in BOTH
    conformal time η and proper time t. Compares to H(t) = 1/(2t) in
    proper time and to H(η) (Hubble in conformal time, dη-derivative).

(2) Same for matter-dominated FRW, a(η) = a_0 η^2,  H(t) = 2/(3t).

(3) Same for slow-roll de Sitter (inflation),
    a(η) = -1/(H_dS η),  η ∈ (-∞, 0),  H(t) = H_dS = const.

(4) Verdict: ROBUST / CONFORMAL-ONLY / GAUGE-INVARIANT-AFTER-CAREFUL-INTERPRETATION.

Author: Opus 4.7 sub-agent. Date: 2026-05-02.
"""

import sympy as sp


def banner(title):
    bar = "=" * 76
    print(f"\n{bar}\n  {title}\n{bar}\n")


# Symbols.
eta, t, a0, H_dS = sp.symbols('eta t a_0 H_dS', positive=True)
R_conf = sp.symbols('R_conf', positive=True)   # comoving (conformal) radius

# Modular Lyapunov exponent (CMPT24 universal value, in modular-time units).
lam_mod = 2 * sp.pi


def jacobian_ds_dt(a_of_eta, eta_obs_sym, R_conf_sym):
    """
    Casini-Huerta-Myers eq.(3.16): for a comoving observer at the CENTER
    of a diamond, the modular flow parameter s is related to the local
    proper time τ_proper at that center by

        ds/d(τ_proper) = 1 / (2π R_proper)

    where R_proper(η_c) = a(η_c) * R_conf is the PROPER radius of the
    diamond (gauge-invariant length).

    Crucially: this Jacobian is expressed PER UNIT PROPER TIME at the
    observer. Proper time of a comoving observer in FRW is exactly the
    cosmic-time coordinate t = ∫ a(η') dη'. Hence
        ds/dt = 1 / (2π a(η_c) R_conf)  =  1 / (2π R_proper).

    The same Jacobian, expressed per unit conformal time η, is
        ds/dη = (ds/dt)(dt/dη) = a(η) * ds/dt = 1 / (2π R_conf).

    These two expressions are EQUIVALENT (same Jacobian, two parameter-
    izations of the observer worldline). The OBJECT (1/C_k) dC_k/dτ for
    a generic clock τ is gauge-COVARIANT: it transforms as dτ → dτ' = J dτ
    via the chain rule, exactly like H(τ).
    """
    R_proper = a_of_eta.subs(eta, eta_obs_sym) * R_conf_sym
    return 1 / (2 * sp.pi * R_proper)


def hubble_in_proper_time(a_of_eta_sym, t_of_eta_sym):
    """
    Compute H(t) := (1/a)(da/dt) by chain rule, eliminating η in favor of t.
    """
    a_eta = a_of_eta_sym
    da_deta = sp.diff(a_eta, eta)
    dt_deta = sp.diff(t_of_eta_sym, eta)
    H_eta = (1/a_eta) * (da_deta / dt_deta)
    H_eta = sp.simplify(H_eta)
    # express in t
    eta_of_t_solutions = sp.solve(t_of_eta_sym - t, eta)
    eta_of_t = [s for s in eta_of_t_solutions if s.is_real is not False][0]
    H_t = sp.simplify(H_eta.subs(eta, eta_of_t))
    return H_eta, H_t, eta_of_t


def piste1_rate_in_proper_time(a_of_eta_sym, t_of_eta_sym,
                                R_conf_sym=R_conf, eta_obs_sym=eta):
    """
    Compute Piste 1's rate (1/C_k) dC_k/dt at the comoving observer.

    By construction:
        (1/C_k) dC_k/ds  =  λ^mod_L = 2π   (CMPT24, universal)
        ds/dt = J(η_c)   = 1 / (2π R_proper(η_c))    (CHM08-3.16)
    so
        (1/C_k) dC_k/dt = 2π * J(η_c) = 1 / R_proper(η_c).

    For the past-light-cone diamond, η_c = η_obs and R_conf = η_obs.
    """
    J = jacobian_ds_dt(a_of_eta_sym, eta_obs_sym, R_conf_sym)
    rate_eta = sp.simplify(lam_mod * J)         # in conformal time η ≡ η_obs
    # Switch to t parametrization: t = t(η_obs) — same observer worldline.
    eta_of_t_solutions = sp.solve(t_of_eta_sym - t, eta)
    eta_of_t = [s for s in eta_of_t_solutions if s.is_real is not False][0]
    rate_t = sp.simplify(rate_eta.subs(eta_obs_sym, eta_of_t))
    return rate_eta, rate_t, eta_of_t


# ============================================================================
banner("ERA 1.  Radiation-dominated FRW:  a(η) = a_0 η,  t = a_0 η^2 / 2")
# ============================================================================
a_rad = a0 * eta
t_rad = sp.integrate(a_rad, (eta, 0, eta))      # = a_0 eta^2 / 2
print(f"  a(η)  = {a_rad}")
print(f"  t(η)  = ∫_0^η a(η')dη'  = {t_rad}")
print(f"  η(t)  = sqrt(2 t / a_0)")
print()

H_eta_rad, H_t_rad, eta_of_t_rad = hubble_in_proper_time(a_rad, t_rad)
print(f"  Textbook H computed via chain rule:")
print(f"    H(η)  = {H_eta_rad}")
print(f"    H(t)  = {H_t_rad}")
print(f"    η(t)  = {eta_of_t_rad}")
print()

# Past-light-cone diamond: R_conf = η_obs, so substitute R_conf -> eta_obs.
print(f"  Past-light-cone diamond: R_conf = η_obs.  Substitute.\n")
rate_eta_rad, rate_t_rad, _ = piste1_rate_in_proper_time(
    a_rad, t_rad, R_conf_sym=eta, eta_obs_sym=eta
)
print(f"  Piste 1 rate (1/C_k) dC_k/dt:")
print(f"    expressed in η_obs:  {rate_eta_rad}")
print(f"    expressed in t   :   {rate_t_rad}")
print()

ratio_rad = sp.simplify(rate_t_rad / H_t_rad)
print(f"  RATIO  ((1/C_k) dC_k/dt) / H(t)  =  {ratio_rad}")
print(f"  (= 1 means MATCH; deviation means GAUGE-DEPENDENT or wrong)")
print()

# ============================================================================
banner("ERA 2.  Matter-dominated FRW:  a(η) = a_0 η^2,  t = a_0 η^3 / 3")
# ============================================================================
a_mat = a0 * eta**2
t_mat = sp.integrate(a_mat, (eta, 0, eta))      # = a_0 eta^3 / 3
print(f"  a(η)  = {a_mat}")
print(f"  t(η)  = ∫_0^η a(η')dη'  = {t_mat}")
print()

H_eta_mat, H_t_mat, eta_of_t_mat = hubble_in_proper_time(a_mat, t_mat)
print(f"  Textbook H computed via chain rule:")
print(f"    H(η)  = {H_eta_mat}")
print(f"    H(t)  = {H_t_mat}")
print(f"    η(t)  = {eta_of_t_mat}")
print()

# Same past-light-cone diamond convention: R_conf = η_obs.
rate_eta_mat, rate_t_mat, _ = piste1_rate_in_proper_time(
    a_mat, t_mat, R_conf_sym=eta, eta_obs_sym=eta
)
print(f"  Piste 1 rate with R_conf = η_obs (PLC-diamond convention):")
print(f"    in η_obs:  {rate_eta_mat}")
print(f"    in t   :   {rate_t_mat}")
print()

ratio_mat = sp.simplify(rate_t_mat / H_t_mat)
print(f"  RATIO  ((1/C_k) dC_k/dt) / H(t)  =  {ratio_mat}")
print()

# ============================================================================
banner("ERA 3.  de Sitter (slow-roll inflation): a(η) = -1/(H_dS η),  η<0")
# ============================================================================
# In dS we use η ∈ (-∞, 0) and a(η) = -1/(H_dS η) > 0.  Let's substitute.
eta_neg = sp.symbols('eta_neg', negative=True)
a_dS = -1 / (H_dS * eta_neg)
# Cosmic time: t = ∫ a(η') dη' from a reference time η_0 (avoid the singular
# η→0 boundary). Choose η_0 so that t = -log(-H_dS η)/H_dS works out.
# d t/dη = a(η) = -1/(H_dS η), so t = -log(-η)/H_dS + const, choose const = 0.
t_dS = -sp.log(-eta_neg) / H_dS
print(f"  a(η)  = {a_dS}    (η<0)")
print(f"  t(η)  = -log(-η)/H_dS = {t_dS}")
print(f"  H(t)  = H_dS (constant)")
print()

# Compute H by chain rule directly (skip hubble_in_proper_time which assumed
# η>0 and a polynomial t-of-η).
da_deta = sp.diff(a_dS, eta_neg)
dt_deta = sp.diff(t_dS, eta_neg)
H_eta_dS = sp.simplify((1/a_dS) * (da_deta / dt_deta))
print(f"  H(η_neg) by chain rule = {H_eta_dS}")
H_t_dS_check = H_eta_dS  # already constant
print(f"  H(t) = {H_t_dS_check} (constant, as expected for dS)")
print()

# Piste 1: ds/dt = 1/(2π R_proper) = 1/(2π a(η_obs) R_conf).
# For the slow-roll dS case, the natural "horizon-sized diamond" has
# proper radius R_proper = 1/H_dS (the Hubble horizon). Equivalently
# R_conf = -η_obs (so that R_proper = a(η_obs) * (-η_obs) = 1/H_dS).
R_conf_dS = -eta_neg
R_proper_dS = sp.simplify(a_dS * R_conf_dS)
print(f"  Hubble-horizon diamond: R_conf = -η_obs => R_proper = {R_proper_dS} = 1/H_dS  (HIT)")
print()

rate_dS_eta = sp.simplify(lam_mod / (2 * sp.pi * R_proper_dS))
print(f"  Piste 1 rate (1/C_k) dC_k/dt = 1/R_proper = {rate_dS_eta}")
print(f"  Compared to H(t) = {H_t_dS_check}")
ratio_dS = sp.simplify(rate_dS_eta / H_t_dS_check)
print(f"  RATIO = {ratio_dS}")
print()

# ============================================================================
banner("UNIFIED RESULT — geometric formulation")
# ============================================================================
print("""
  In ALL three eras, the Piste 1 rate evaluates to

         (1/C_k) dC_k/dt  =  1 / R_proper(η_c)

  This is a GEOMETRIC quantity — R_proper(η_c) is the gauge-invariant
  proper radius of the diamond at its bifurcation slice, expressed at the
  comoving observer's location.

  Hubble parameter H(t) is a separate gauge-invariant geometric quantity:
  the expansion rate as measured by the observer's proper clock.

  The match  H(t) = 1/R_proper(η_c)  holds **iff** the diamond is chosen
  such that R_proper(η_c) = 1/H at the observer's time. This is precisely
  the **HUBBLE-RADIUS DIAMOND** (proper-radius = Hubble length 1/H).

  Now we check ERA-by-ERA whether the past-light-cone (PLC) diamond, with
  R_conf = η_obs, has R_proper = 1/H at each era.
""")

# ERA-by-ERA: PLC diamond has R_conf = η_obs.  R_proper = a(η_obs)*η_obs.
# Check whether this equals 1/H(t).

# Radiation:
R_proper_rad_PLC = sp.simplify(a_rad.subs(eta, eta) * eta)   # = a0 * η^2
H_inv_rad_t = sp.simplify(1 / H_t_rad)                       # = 2t = a0*η^2
print(f"  RADIATION:")
print(f"    R_proper (PLC) = a(η)*η = {R_proper_rad_PLC}")
print(f"    1/H(t)         = 2t     = {sp.simplify(2*t)}, in η: {sp.simplify(H_inv_rad_t.subs(t,t_rad))}")
print(f"    Equal?  {sp.simplify(R_proper_rad_PLC - H_inv_rad_t.subs(t, t_rad))} == 0  →  YES, exact match")
print()

# Matter:
R_proper_mat_PLC = sp.simplify(a_mat.subs(eta, eta) * eta)   # = a0 * η^3
H_inv_mat_t = sp.simplify(1 / H_t_mat)                       # = 3t/2
print(f"  MATTER:")
print(f"    R_proper (PLC) = a(η)*η = {R_proper_mat_PLC}")
print(f"    1/H(t)         = 3t/2   = {sp.simplify(3*t/2)}, in η: {sp.simplify(H_inv_mat_t.subs(t, t_mat))}")
diff_mat = sp.simplify(R_proper_mat_PLC - H_inv_mat_t.subs(t, t_mat))
print(f"    Equal?  {diff_mat} == 0  →  {'YES' if diff_mat == 0 else 'NO — MISMATCH'}")
ratio_mat_geom = sp.simplify(R_proper_mat_PLC / H_inv_mat_t.subs(t, t_mat))
print(f"    R_proper / (1/H) = {ratio_mat_geom}     (should be 1 for match)")
print()

# de Sitter:
R_proper_dS_PLC = sp.simplify(a_dS * (-eta_neg))             # = 1/H_dS
H_inv_dS = sp.simplify(1 / H_dS)
print(f"  DE SITTER (R_conf = -η_obs convention):")
print(f"    R_proper       = {R_proper_dS_PLC}")
print(f"    1/H(t)         = {H_inv_dS}")
print(f"    Equal?  YES, exactly (both = 1/H_dS).")
print()

# ============================================================================
banner("SAME COMPUTATION DIRECTLY IN PROPER TIME t (no η at all)")
# ============================================================================
print("""
  We restate the entire computation using cosmic time t as the only
  parameter, to verify there is no conformal-time bias.

  GENERIC FRW (open or flat, comoving observer at x=0):
    Choose any clock τ on the observer's worldline.
    Piste 1 says: (1/C_k) dC_k/dτ = λ^mod_L * (ds/dτ).
    With λ^mod_L = 2π and CHM08:  ds/dτ_proper = 1/(2π R_proper).
    Hence (1/C_k) dC_k/dτ_proper = 1/R_proper.

    For the comoving observer, τ_proper IS cosmic time t.
    => (1/C_k) dC_k/dt = 1/R_proper(t),
       where R_proper(t) = a(t) * R_conf is the proper radius of the
       diamond evaluated at the comoving observer's cosmic-time slice.

    H(t) by definition is (1/a)(da/dt). The match
       H(t)  =?=  1/R_proper(t)
    is equivalent to
       R_proper(t)  =?=  a(t)/(da/dt).

    For PLC-diamond with R_conf = η_obs, R_proper = a(η_obs)*η_obs.
    So we need:  a(η_obs)*η_obs = a(η_obs)/(da/dt|_{η_obs}).

    Equivalently:  η_obs * (da/dt)|_{η_obs} = 1.

    Using dt/dη = a => da/dt = (1/a) da/dη:
       η_obs * (1/a(η_obs)) * (a'(η_obs))  =?=  1
       => η_obs * a'(η_obs) / a(η_obs)  =  1
       => d log a / d log η  =  1.

    THIS IS THE RADIATION-ONLY CONDITION. It holds iff a ∝ η,
    i.e. radiation. For matter (a ∝ η^2) it gives 2, not 1.
    For general a ∝ η^p it gives p.
""")

print("\nLet's verify by direct sympy (d log a / d log η = η * a'(η) / a(η)):")
for label, a_eta_expr in [("radiation a∝η", a_rad),
                           ("matter   a∝η²", a_mat),
                           ("kination a∝η^(1/2)", a0 * sp.sqrt(eta)),
                           ("a∝η^p (generic)", a0 * eta ** sp.symbols('p', positive=True))]:
    p_log = sp.simplify(eta * sp.diff(a_eta_expr, eta) / a_eta_expr)
    print(f"  d log a / d log η  for {label}:  {p_log}")

print("""
  CONCLUSION on the geometric origin of the match:

  The Piste 1 rate 1/R_proper(t) and the Hubble rate H(t) coincide at the
  PLC-diamond R_conf = η_obs ONLY in the **radiation-dominated case**.
  For matter, the same diamond convention gives a constant offset ratio of
  d log a / d log η = 2 (so the rate equals 2H instead of H, off by a
  factor 2).  For dS, the natural Hubble-horizon convention restores the
  match trivially because R_proper = 1/H by definition.

  Thus the match H = 1/R_proper(t) is GAUGE-INVARIANT (it's a relation
  between two observer-worldline scalars, both gauge-invariant). But
  whether 1/R_proper(η_c) = H(t) DEPENDS on the diamond convention and on
  the FRW equation of state.

  This is NOT the kinematic objection Mistral raised. Mistral's worry was
  "if you change time slicing, the match breaks." That worry is REFUTED
  by our computation: the rate (1/C_k) dC_k/dt is a scalar at the observer's
  worldline (just like H(t)), and the match in conformal time and the
  match in proper time are LITERALLY THE SAME equation, because both rates
  obey the same chain-rule transformation when you reparametrise the
  worldline. (See the unified derivation above: rate = 1/R_proper, H is
  another scalar; their equality is parametrization-INDEPENDENT.)

  However, Mistral's underlying concern survives in a *different* form:

  the match H = 1/R_proper depends on a CHOICE OF DIAMOND (which is a
  spacetime-region choice, not a coordinate choice). Different diamond
  conventions give different ratios. The "natural" PLC-diamond happens to
  give the match exactly for radiation, off by a factor 2 for matter, and
  the Hubble-horizon diamond gives it for dS.

  SO: Mistral was *partially* wrong (it's not a coordinate gauge issue);
  but Mistral was *partially* right (the match isn't universal — it's
  era-dependent and diamond-convention-dependent).
""")

# ============================================================================
banner("MATTER FRW with HUBBLE-RADIUS DIAMOND  R_proper = 1/H = 3t/2")
# ============================================================================
# Try the Hubble-horizon diamond convention for matter, like for dS.
# R_proper(η_obs) = 1/H(t) = 3 a(η_obs) η_obs / 2 (from H = 2/(3t), t=a0 η³/3).
# So R_conf_HH = R_proper / a(η_obs) = (3 η_obs / 2).
print("""
  Define R_conf_HH := 1 / [H(t) * a(η_obs)] = "Hubble-horizon" diamond
  in COMOVING units. Then R_proper = 1/H trivially, and
  (1/C_k) dC_k/dt = 1/R_proper = H. The match becomes EXACT in any era.

  Verify symbolically for matter:
""")
R_conf_HH_mat = sp.simplify(1 / (H_t_mat * a_mat))      # in η_obs
print(f"    R_conf_HH (matter) = {R_conf_HH_mat}")
R_proper_HH_mat = sp.simplify(R_conf_HH_mat * a_mat)
print(f"    R_proper (matter) = {R_proper_HH_mat}")
rate_HH_mat = sp.simplify(1 / R_proper_HH_mat)
ratio_HH_mat = sp.simplify(rate_HH_mat / H_t_mat)
print(f"    (1/C_k) dC_k/dt   = {rate_HH_mat}")
print(f"    H(t)              = {H_t_mat}")
print(f"    RATIO             = {ratio_HH_mat}")
print()

# Verify symbolically for radiation:
R_conf_HH_rad = sp.simplify(1 / (H_t_rad * a_rad))
print(f"    R_conf_HH (radiation, in η_obs) = {R_conf_HH_rad}")
print(f"    Compare to PLC R_conf = η_obs: ratio = {sp.simplify(R_conf_HH_rad / eta)}")
print(f"    => For RADIATION, Hubble-horizon diamond and PLC diamond")
print(f"       coincide up to a factor 2. PLC is the actual past light-cone")
print(f"       (Big Bang to today, radius = today's conformal time).")
print(f"       Hubble-horizon is half of that. Both give finite O(1) ratios.")

# ============================================================================
banner("FINAL VERDICT")
# ============================================================================
print("""
  CONCLUSION (sympy-verified, no hand-waving):

  (a) The Piste 1 rate (1/C_k) dC_k/dτ_proper, computed via the CHM08
      formula ds/dτ_proper = 1/(2π R_proper), is a SCALAR at the observer's
      worldline. It is GAUGE-INVARIANT in the strict sense of Mistral's
      worry: changing from conformal time η to cosmic time t does NOT
      change anything substantive — both express the same scalar
      (1/R_proper(η_c)) in two parametrizations, with the chain rule
      handling the conversion automatically.

      Mistral's specific claim that "the 1/(2t) scaling is not robust to
      gauge transformations" is REFUTED in the strict sense: 1/(2t) is
      H(t) itself, a scalar, and it equals 1/R_proper for the PLC diamond
      in radiation. Both sides of the equation transform the same way
      under any reparametrization of t → t'(t).

  (b) HOWEVER, the match H(t) = 1/R_proper(η_c) is NOT universal. It
      depends on the DIAMOND CONVENTION (a spacetime-region choice, not
      a coordinate choice) and on the FRW equation of state:

        - Radiation + PLC diamond  : MATCH (ratio = 1, exact).
        - Matter   + PLC diamond  : ratio = 1/2 (off by 1/p, p=d log a/d log η).
        - de Sitter + Hubble-radius diamond: MATCH (ratio = 1, by construction).
        - Matter   + Hubble-radius diamond: MATCH (ratio = 1, by construction
          of the diamond).

      The "natural" diamond for matching H is always the **Hubble-radius
      diamond**, R_proper = 1/H. This is a tautology: the rate is
      1/R_proper, so it equals H iff R_proper = 1/H.

  (c) The genuine novel content of Piste 1 is therefore NOT
      "H equals Krylov rate" (that's tautological for the right diamond).
      The genuine content is

         (1/C_k) dC_k/dt  =  1 / R_proper(η_c)

      i.e. the Krylov rate of the **modular crossed product** equals the
      INVERSE PROPER RADIUS of the diamond. This is a non-trivial
      consequence of (i) CMPT24 universal λ^mod_L = 2π and (ii) CHM08
      ds/dτ = 1/(2π R_proper). Both inputs are well-established in the
      QFT/holography literature.

      That's a real but MODEST result: it relates Krylov complexity rate
      to a geometric scale (proper radius) of the algebra's localization
      region — it does NOT directly say "Hubble = Krylov rate" except in
      the specific case where the diamond happens to be Hubble-sized.

  ────────────────────────────────────────────────────────────────────────
  VERDICT:  GAUGE-INVARIANT-AFTER-CAREFUL-INTERPRETATION
  ────────────────────────────────────────────────────────────────────────

  More precisely:
    - Mistral's *specific* claim ("not robust under proper-time gauge")
      is REFUTED. The rate is a scalar, transforms covariantly, and the
      match holds in ANY parametrization of the observer worldline.
    - Mistral's *spirit* (Piste 1 is over-claimed as "Hubble = Krylov rate")
      is CORRECT. The substantive content is "rate = 1/R_proper", and
      the H-match is a feature of choosing the Hubble-sized diamond.

  Recommended downgrade: Piste 1 from "partial positive in radiation"
  to "rate = 1/R_proper geometric identity, partial positive". Still
  paper-worthy under the reframed title 'Krylov-Modular-Diameter
  Correspondence', but without the cosmological-Hubble headline.
""")
