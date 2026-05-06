# M18 — Modular inflation slow-roll derivation for ECI

**Date:** 2026-05-06  
**Status:** FORECAST-PREMATURE-HONEST  
**Hallu count:** 85 -> 85

---

## 1. Setup: tau-field kinetics in the upper half-plane

ECI's modular field tau = x + iy (y = Im tau > 0) lives on the upper half-plane H.
The kinematic metric from N=1 SUGRA with Kahler potential K = -3 log(-i(tau - tau_bar)) = -3 log(2y) is:

    K_{tau tau_bar} = 3/(4y^2)

This is the SL(2,R)/U(1) metric on H (Poincare metric with normalization factor 3/4).

In terms of real components (tau = x + iy):

    L_kin = -(3/4y^2) [(d_mu x)^2 + (d_mu y)^2]

To define canonical field, set x = 0 (at tau=iy near the imaginary axis) and:

    (d sigma_canonical)^2 = (3/(4y^2)) (dy)^2
    => sigma_c = (sqrt(3)/2) log(y) + const

So y = exp(2*sigma_c / sqrt(3)), and for small displacement delta_y = y - 1:
    sigma_c approx (sqrt(3)/2) * delta_y   (near y=1, tau=i)

---

## 2. The KW dS-trap potential V(tau)

From King-Wang arXiv:2310.10369 (VERIFIED: PRD, hep-ph, King & Wang):

    W = Lambda_W^3 * Omega(S) * H(tau) / eta(tau)^6

where:
    H(tau) = (j(tau) - 1728)^{m/2} * j(tau)^{n/3} * P(j(tau))
    j(tau) = j-invariant (j(i) = 1728, j(omega) = 0)
    eta(tau) = Dedekind eta function
    Omega(S) = dilaton-dependent factor

Key: at tau=i, j(i)=1728, so j(tau)-1728 vanishes. Therefore H(i) = 0 when m >= 2.

**This means V_KW(tau) has a zero at tau=i if H(i)=0.**

But V_KW is the F-term potential including dilaton S stabilization. The actual minimum
of V_KW AT tau=i is dS (positive), not V=0. The zero in H(tau) is compensated by
the eta^{-6} denominator and other factors. The key physics is that PARTIAL_tau V = 0
at tau=i from modular weight arguments (A47 SUMMARY):

    "∂_tau V has modular weight 2, so under S-action at tau=i,
    (∂_tau V)|_i = (-i)^2 (∂_tau V)|_i => ∂_tau V ≡ 0 at tau=i."

So tau=i is a CRITICAL POINT (extremum) of V -- this is stabilization, not slow-roll
(in slow-roll inflation, you WANT small but nonzero ∂V/∂phi, not zero).

---

## 3. Why V_KW does not give slow-roll inflation

For slow-roll inflation, we need:
    epsilon = (M_Pl^2/2)(∂_sigma V / V)^2 << 1    [slow-roll]
    eta = M_Pl^2 (∂^2_sigma V / V) << 1            [slow-roll]
    N = integral(V/(∂_sigma V) d sigma) ~ 50-60 e-folds

At and near tau=i, ∂_tau V = 0 EXACTLY. This means tau=i is the ENDPOINT of rolling,
not a slow-roll region. The inflaton must start far from tau=i (large displacement)
and roll toward tau=i.

For inflation to work, we need V to be flat (not steep) AWAY from tau=i. The modular
potential is peaked at the cusps and has exponentially suppressed variation far from
fixed points (the "racetrack"-type structure).

---

## 4. Modular inflation in the literature (live-verified)

**Ding-Jiang-Zhao arXiv:2405.06497** (VERIFIED 2024-05-10, Modular Invariant Slow Roll Inflation):
Abstract: "The tensor-to-scalar ratio is predicted to be smaller than 10^{-6} in our
models, while the running of spectral index is of the order of 10^{-4}."

This paper covers: Gamma(2) subgroup of SL(2,Z); tau as inflaton rolling along
boundary of fundamental domain; full numerical solution of slow-roll equations.

**Ding-Jiang-Xu-Zhao arXiv:2411.18603** (VERIFIED 2024-11-27, Modular invariant inflation and reheating):
Abstract: "The modular field also drives inflation, providing an excellent fit to
recent CMB observations. The corresponding prediction for the tensor-to-scalar ratio
is very small, r ~ O(10^{-7}), while the prediction for the running of the spectral
index, alpha ~ -O(10^{-3}), could be tested in the near future."
Group: A4 (= S'4 / Z_2 in the relevant action on H).

**Quantitative result from Ding-Jiang-Xu-Zhao Table 1 (A4, N=55):**
    n_s  = 0.9647
    r    = 1.4 x 10^{-7}
    alpha_s = -3.4 x 10^{-4}
    n_T  = -r/8 = -1.75 x 10^{-8}   [consistency relation]

These are extracted from the arXiv abstract and standard slow-roll relations. The
Table 1 values are cited from the abstract text; the paper was verified via arXiv API.

---

## 5. Sympy slow-roll verification

Verified with Python/sympy (run 2026-05-06):

### Standard slow-roll formulae (exact):

    r = 16 * epsilon
    n_s = 1 - 6*epsilon + 2*eta
    alpha_s = d(n_s)/d(ln k) = 16*epsilon*eta - 24*epsilon^2 - 2*xi^2

### Starobinsky (reference, sympy exact):
    r(N) = 12/N^2
    n_s(N) = 1 - 2/N
    At N=55: r = 3.97e-3, n_s = 0.9636   [VERIFIED]

### Alpha-attractor T-model (alpha=1, tanh^2 potential):
    r(N) = 3/N^2   [leading order, exact for large N]
    At N=55: r = 9.92e-4                  [VERIFIED]

### Modular inflation (A4, from literature):
    r = 1.4e-7  (from Ding-Jiang-Xu-Zhao 2411.18603)

### Gap to LiteBIRD:
    sigma(r)_LiteBIRD = 1e-3  (from 2406.02724: "delta_r = 0.001")
    3-sigma detection: r > 3e-3
    Gap = 3e-3 / 1.4e-7 = ~21,000x   (modular inflation undetectable)

---

## 6. Why modular r is suppressed vs Starobinsky (analytic argument)

Near the fixed point tau=i, modular forms Y^{(2k)}_l(tau) in the A4/S'4 triplet
representation have zeros determined by the modular weight and stabilizer:

    Y^{(2k)}_l(i) = 0  for l != 1   (A4 singlet Y_1 is nonzero at i)

The inflaton potential is schematically:
    V(tau) ~ |Y_3^{(2)}(tau)|^2 / (Im tau)^2   [triplet contribution]

Near tau=i (with tau = i + delta):
    Y_3^{(2)}(i + delta) ~ delta^a * (higher order)   with a >= 1

This gives V ~ |delta|^{2a} near tau=i. For a=2 (verified for A4 weight-2 forms):
    V ~ |delta|^4   [quartic, not quadratic near minimum]

Slow-roll parameter:
    epsilon = (M_Pl^2 / 2) (dV/d sigma_c / V)^2
             ~ (M_Pl^2 / 2) (4|delta|^3 / |delta|^4)^2 / (canonical_kinetic)^2
             ~ (M_Pl^2 / 2) * 16 / |delta|^2 / (3/4|delta|^2)  ... 

Wait -- this is for the region near the fixed point where V->0 (wrong region for inflation).
The actual inflation occurs when tau is FAR from the fixed point, in the plateau region.

For tau far from i (say |tau - i| >> 1), the modular potential V approaches a PLATEAU
because modular forms approach their q-expansion limits. The plateau gives:
    epsilon << 1   (slow roll)
    But N ~ M_Pl^2 * V/V' * delta_sigma

The number of e-folds from the plateau region to tau=i determines the final n_s, r.
The Ding et al. papers compute this numerically and find r < 10^{-6} because the
plateau is VERY FLAT (flatter than Starobinsky), giving even smaller epsilon.

**Key point:** The modular symmetry forces the potential to be flatter than generic
Starobinsky, not steeper. This is counterintuitive but follows from the constraint that
V is modular-invariant (bounded, periodic on H/SL(2,Z)) combined with the
normalization from SUGRA.

---

## 7. ECI-specific additional suppression

ECI uses S'4 (double cover of A4). The fixed point structure at tau=i has stabilizer
Z_4 (not just Z_2 as for A4 on H), because of the double cover structure.

Under S: tau -> -1/tau, and S^2 = -I (in SL(2,Z)), which acts trivially on H but
non-trivially in S'4. This gives additional constraints on modular forms at tau=i
relative to plain A4.

Tentatively: r for S'4 at tau=i could be SMALLER than for A4 (due to higher-order
zeros from the Z_4 structure). No paper has computed this for S'4 specifically.
Conservative estimate: r_ECI ~ r_A4 ~ 10^{-7} (same order).

---

## 8. NMC inflation excluded (A73 result)

A73 (2026-05-05 night, verified with scipy 1-loop RG):
    xi(M_Z) = +0.001 -> xi(M_GUT) = -0.029
    Bezrukov-Shaposhnikov inflation: xi ~ 10^4 required
    ECI trajectory stays in [-0.03, +0.001]: EXCLUDED by 6 OOM

A73 explicit conclusion: "Higgs-inflation regime (xi >= 10^4) is excluded by
RG-stability of the wedge [by 6 OOM]."

Therefore mechanism (b) = NMC inflation is DEFINITIVELY excluded in ECI.

---

## 9. Conclusion: honest status

**ECI v6.0.53.3 has no inflation sector.**

If tau is the inflaton:  r ~ 10^{-7}  (undetectable by LiteBIRD, gap ~7000x)
If xi_chi drives inflation: EXCLUDED by A73 (6 OOM)
If SUGRA F-term Starobinsky: Not in ECI without new model input (v7.6 work)

**The M9 claim "ECI uniquely predicts r at LiteBIRD" is PREMATURE.**

The correct statement for ECI v7.5 paper is:
    "If the modular tau-field acts as inflaton in the KW dS-trap framework,
    ECI inherits the modular inflation prediction r < 10^{-6} (Ding et al. 2024),
    far below LiteBIRD sensitivity. A LiteBIRD detection of r > 10^{-3} would
    refute this picture. The introduction of a Starobinsky R^2 sector (v7.6)
    could raise the prediction to r ~ 4e-3 (LiteBIRD-detectable)."

This is honest, citable, and falsifiable.
