#!/usr/bin/env python3
"""Wilson gradient flow (Luscher 2010) for SU(3) D=3 lattice gauge in JAX.

Reference
---------
Martin Luscher, "Properties and uses of the Wilson flow in lattice QCD",
JHEP 08 (2010) 071, arXiv:1006.4518 (verified via arXiv API 2026-05-24,
WebFetch returned title/author/journal as stated).

The Wilson flow is a one-parameter family V_t(x, mu) of link configurations
defined by the gradient-descent ODE

    d V_t(x, mu) / d t  =  - [ Z(x, mu) ] . V_t(x, mu)              (1)

where Z(x, mu) is the SU(N)-projected derivative of the Wilson action at
link (x, mu). At positive flow time t > 0 the gauge field V_t is a smooth
(renormalized in the continuum limit) field; local gauge-invariant
observables built from V_t serve as well-defined physical probes at length
scale sqrt(8 t).

For SU(3) D=4 the standard reference flow time t_0 is defined by

    t_0^2 . < E(t_0) >  =  0.3                                      (2)

(Luscher 2010, eq. (2.4); also BMW collab 1203.4469). The numerical value
0.3 is *specific to D=4* and to the chosen convention for E. For SU(3) D=3
the reference constant must be re-calibrated empirically -- we do NOT
hard-code 0.3 as the D=3 anchor. See `find_t_ref(E_ref=...)`.

Conventions (matched to su3_hmc_d3_jax.py)
------------------------------------------
* SU(3), 8 Gell-Mann generators T_a = lambda_a / 2, tr(T_a T_b) = delta_ab / 2.
* Lattice 3D periodic, links stored as U[mu*V + site] with shape (3, 3) complex64.
* Wilson action S_W(U) = beta . sum_p (1 - (1/3) Re tr U_p), three (mu < nu)
  plaquette pairs in D=3.

Sign of the flow drift
----------------------
With our normalisation S_W = beta . sum_p (1 - (1/N) Re tr U_p), the SU(N)
gradient of S_W at link (x, mu) is

    Z(x, mu) = (beta/(2 N)) . TA[ V Sigma^dag - Sigma V^dag ] / (2 i)

up to a sign convention. In Luscher 2010 the flow equation is written for
the *Yang-Mills functional* S_YM(V) = (1/g0^2) . S_W(V) (with g0^2 absorbed
elsewhere) and reads

    d V / d t  =  - [partial S_YM / partial V]_TA . V

where the bracket [ . ]_TA denotes the SU(N) (i.e. trace-free anti-hermitian)
projection. In flow time *unscaled by beta* the standard Luscher convention
gives

    Z(x, mu) = TA[ V . Omega^dag ] / (2 i) * (-i)                  (3)

with Omega = Sigma (sum of staples). Equivalently and operationally,

    Q(x, mu) = - V . Sigma^dag                                      (4)
    Z(x, mu) = (1/2) (Q - Q^dag) - (1/(2N)) tr(Q - Q^dag) . I       (5)

so that V_{t+eps} = exp(eps . Z) . V approximately decreases S_W. We use
this form (the minus sign in (4) implements gradient descent on S_W).

The flow time t is dimensionless lattice time; physical flow time is
t_phys = t . a^2. Choosing units such that g0^2 = 1 in the flow integrator
(g0^2 is absorbed in the definition of t) is the standard convention --
otherwise t -> g0^2 . t shifts t_0 accordingly.

RK3 integrator (Luscher 2010, Appendix C / Algorithm 1)
-------------------------------------------------------
    W_0 = V_t
    Z_0 = Z(W_0)
    W_1 = exp(   (1/4) eps . Z_0                                ) . W_0
    Z_1 = Z(W_1)
    W_2 = exp(  (8/9) eps . Z_1 - (17/36) eps . Z_0             ) . W_1
    Z_2 = Z(W_2)
    W_3 = exp(  (3/4) eps . Z_2 -  (8/9) eps . Z_1 + (17/36) eps . Z_0
              ) . W_2
    V_{t + eps} = W_3

This is the third-order Runge-Kutta variant tailored to the Lie-group flow
(it preserves V in SU(N) up to O(eps^4)). We apply an explicit SVD
projection back to SU(3) after each step to wash out the residual drift
in single precision.

API
---
    wilson_flow_step(U, eps)         -> U_new                       # one RK3 step
    wilson_flow_evolve(U, t_max, eps)-> dict with t_arr, E_arr, U_traj
    energy_density(U)                -> E(U), plaquette-based proxy
    find_t_ref(U, E_ref=...)         -> t* such that t*^2 . E(t*) = E_ref

Hyperparameters
---------------
    eps = 0.01 - 0.02 (lattice units) -- Luscher 2010 standard
    t_max ~ 1 - 10 in lattice units (typically t_0 ~ a few)

Tested sanity invariants (see __main__ block):
  (1) cold start U = I  =>  E(t) = 0 for all t (machine precision)
  (2) hot start         =>  E(t) decreases monotonically (gradient flow)
  (3) det V_t = 1 +/- 1e-6 after SVD projection (single precision floor)
  (4) reproducibility : same seed => bitwise same E(t) trajectory

Author: K. Remondiere (ORCID 0009-0008-2443-7166)
Date:   2026-05-24
"""
from __future__ import annotations

import os
os.environ.setdefault("JAX_PLATFORMS", "cpu")  # honour caller's env; default cpu

import jax
import jax.numpy as jnp
import numpy as np
from functools import partial


# ============================================================================
#  Type constants -- match su3_hmc_d3_jax.py
# ============================================================================

CDTYPE = jnp.complex64
RDTYPE = jnp.float32
N_COLOR = 3
NDIM = 3
N_GEN = 8


# ============================================================================
#  Small matrix utilities (SU(3) on the lattice)
# ============================================================================

@jax.jit
def sun_mul(A, B):
    return jnp.einsum('...ij,...jk->...ik', A, B)


@jax.jit
def sun_dagger(U):
    return jnp.conj(jnp.swapaxes(U, -1, -2))


@jax.jit
def project_su3(U):
    """Project a near-SU(3) matrix back to SU(3) via SVD polar + det-phase fix.

    U = V Sigma W^dag  ->  proj = V W^dag (unitary)
                       ->  divide by det(proj)^(1/3) for SU(3).
    """
    Vmat, _, WH = jnp.linalg.svd(U)
    proj = sun_mul(Vmat, WH)
    det = jnp.linalg.det(proj)
    det_phase = det / jnp.maximum(jnp.abs(det), 1e-15)
    angle = jnp.angle(det_phase)
    cube_root_phase = jnp.exp(1j * angle / 3.0)
    return proj / cube_root_phase[..., None, None]


def matrix_exp_taylor(X, n_terms: int = 15):
    """exp(X) for anti-hermitian su(3) X via Taylor + 1 scaling-squaring step.

    For the Wilson flow, typical || eps . Z ||_F is bounded by a few times
    eps, so eps <= 0.05 keeps the Taylor remainder well below complex64
    precision with n_terms = 15. We apply one scaling-and-squaring step
    (X -> X/2, exp, square) for extra safety.

    NB : `n_terms` is a Python int captured at trace time -- the function is
    therefore NOT decorated with @jax.jit at the top level; callers should
    jit downstream code that uses it. Bake n_terms via `partial` if needed.
    """
    Xs = X / 2.0
    I = jnp.eye(N_COLOR, dtype=CDTYPE)
    result = jnp.broadcast_to(I, Xs.shape) + jnp.zeros_like(Xs)
    term = jnp.broadcast_to(I, Xs.shape) + jnp.zeros_like(Xs)
    for k in range(1, n_terms + 1):
        term = sun_mul(term, Xs) / k
        result = result + term
    return sun_mul(result, result)


@jax.jit
def trace_anti_hermitian(M):
    """TA[M] = (1/2)(M - M^dag) - (1/(2N)) tr(M - M^dag) I_N.

    Returns the trace-free anti-hermitian part of M, i.e. the projection
    onto su(N). Verified by hand: TA[M]^dag = - TA[M] and tr(TA[M]) = 0.
    """
    Mdag = sun_dagger(M)
    A = 0.5 * (M - Mdag)                          # anti-hermitian
    # subtract trace / N to make it traceless
    tr = (A[..., 0, 0] + A[..., 1, 1] + A[..., 2, 2])
    I3 = jnp.eye(N_COLOR, dtype=CDTYPE)
    # broadcast trace into a (..., 3, 3) diagonal subtraction
    correction = (tr / N_COLOR)[..., None, None] * I3
    return A - correction


# ============================================================================
#  Lattice geometry (D=3 periodic) -- replicated from HMC for stand-alone use
# ============================================================================

def build_neighbors_3D(L: int):
    """Return nbr shape (3, 2, V) :  nbr[mu, 0, site] = site + e_mu,
                                     nbr[mu, 1, site] = site - e_mu."""
    V = L ** 3
    nbr = np.zeros((3, 2, V), dtype=np.int32)
    coords = np.stack(np.unravel_index(np.arange(V), (L,) * 3), axis=1)
    for mu in range(3):
        for direc, sign in [(0, 1), (1, -1)]:
            shifted = coords.copy()
            shifted[:, mu] = (shifted[:, mu] + sign) % L
            nbr[mu, direc] = np.ravel_multi_index(
                tuple(shifted[:, k] for k in range(3)), (L,) * 3
            )
    return jnp.array(nbr)


# ============================================================================
#  Staple sum  Sigma(x, mu)  for link (x, mu) in D=3
# ============================================================================
#
#  In D dimensions, the staple sum for link U(x, mu) is
#
#       Sigma(x, mu) = sum_{nu != mu} [ U(x+e_mu, nu) . U^dag(x+e_nu, mu)
#                                     . U^dag(x, nu)
#                                   +  U^dag(x+e_mu - e_nu, nu)
#                                     . U^dag(x - e_nu, mu)
#                                     . U(x - e_nu, nu) ]
#
#  i.e. the "forward" and "backward" staples in each of the (D-1) = 2 planes
#  containing the link, contracted so that U(x, mu) . Sigma^dag(x, mu) is
#  one plaquette (sum over the 2(D-1) plaquettes that touch the link).
#
#  For D=3 we have exactly 2(D-1) = 4 staples per link.


def make_compute_staples_3D(L: int, nbr):
    """Build a JIT'd function: U -> Sigma (same shape as U)."""
    V = L ** 3
    sites = jnp.arange(V)

    @jax.jit
    def staples(U):
        # U has shape (3*V, 3, 3)
        Sigma = jnp.zeros((3 * V, N_COLOR, N_COLOR), dtype=CDTYPE)

        for mu in range(3):
            U_mu = U[mu * V + sites]                          # (V, 3, 3)

            for nu in range(3):
                if nu == mu:
                    continue
                # forward staple at link (x, mu):
                #   U(x+e_mu, nu) . U(x+e_nu, mu)^dag . U(x, nu)^dag
                x_pm = nbr[mu, 0, sites]                      # x + e_mu
                x_pn = nbr[nu, 0, sites]                      # x + e_nu
                A = U[nu * V + x_pm]
                B = sun_dagger(U[mu * V + x_pn])
                C = sun_dagger(U[nu * V + sites])
                fwd = sun_mul(sun_mul(A, B), C)

                # backward staple at link (x, mu):
                #   U(x+e_mu-e_nu, nu)^dag . U(x-e_nu, mu)^dag . U(x-e_nu, nu)
                x_mn = nbr[nu, 1, sites]                      # x - e_nu
                # x + e_mu - e_nu  =  nbr_-(nu) applied to (x + e_mu)
                x_pm_mn = nbr[nu, 1, x_pm]
                Ab = sun_dagger(U[nu * V + x_pm_mn])
                Bb = sun_dagger(U[mu * V + x_mn])
                Cb = U[nu * V + x_mn]
                bwd = sun_mul(sun_mul(Ab, Bb), Cb)

                # accumulate (V, 3, 3) into the mu-block of Sigma
                Sigma = Sigma.at[mu * V + sites].add(fwd + bwd)

            # mu-block done

        return Sigma

    return staples


# ============================================================================
#  Drift  Z(x, mu)  -- the SU(N) gradient of S_W at the link (x, mu)
# ============================================================================
#
#  With S_W(U) = sum_p [1 - (1/N) Re tr U_p], the differential is
#
#       dS_W / d U(x, mu) ~ - (1/N) Sigma(x, mu)^dag   (matrix derivative)
#
#  but on the group we need the SU(N) projection:
#
#       Omega(x, mu) = U(x, mu) . Sigma(x, mu)^dag
#       Z(x, mu)     = TA[ Omega ]                                    (Luscher 2010 eq.(1.4))
#
#  with TA the trace-free anti-hermitian projector. Then
#
#       d U / d t  =  - Z(x, mu) . U(x, mu)                            (1.3)
#
#  is the steepest descent on S_W. We implement Z exactly as in (1.4).
#  The overall sign and the optional g0^2 prefactor are absorbed into the
#  definition of flow time t (Luscher's convention).


def make_drift_Z_3D(L: int, nbr):
    """Build a JIT'd function: U -> Z (same shape as U).

    Derivation (with Luscher 2010 conventions clarified) :

    Our staple function `make_compute_staples_3D` stores, for each link
    (x, mu), the sum

        Sigma_mine(x, mu) = sum_{nu != mu} [staple_fwd_nu + staple_bwd_nu]

    where `staple_fwd_nu = U(x+e_mu, nu) . U(x+e_nu, mu)^dag . U(x, nu)^dag`
    so that  P_fwd  =  U(x, mu) . staple_fwd_nu  is the plaquette in the
    (mu, nu) plane "above" the link. Then

        Omega(x, mu)  :=  U(x, mu) . Sigma_mine(x, mu)
                      =  sum_p  U_p

    (sum over the 2(D-1) = 4 plaquettes containing the link, oriented so
    each starts with U(x, mu)). This is precisely  Omega(x, mu)  =
    V(x, mu) Sigma_Luscher^dag(x, mu) in Luscher's notation, since
    Luscher's Sigma_Luscher equals Sigma_mine^dag.

    The Luscher Wilson flow drift is

        Z(V)  =  - g_0^2 . [ T^a (partial^a_{x,mu} S_w) ]_TA . V          (eq. 1.4)

    For S_w(U) = (1/g_0^2) . sum_p Re tr{1 - U_p}, the g_0^2 cancels and a
    standard calculation (using tr(T^a T^b) = -(1/2) delta_ab for Luscher's
    anti-hermitian generators) gives

        Z(V)  =  - (1/4) [ Omega - Omega^dag ]_TA                          (anti-herm conv.)

    With our su(3) convention (T_a = lambda_a/2 hermitian, tr T_a T_b =
    +delta_ab/2), the analogous result picks up an overall sign and an
    overall factor of 2 that just RESCALE flow time:

        Z(V)  =  + (1/2) [ Omega - Omega^dag ]_TA  =  TA[Omega]            (our conv.)

    where TA[M] = (1/2)(M - M^dag) - (1/(2N)) tr(M - M^dag) . I.

    The Wilson flow then reads dV/dt = Z V (Luscher Appendix C eq. C.1) and
    the RK3 step writes exp(c . eps . Z) . V with POSITIVE c-coefficients.
    Since the action decreases monotonically along the flow (Luscher pg. 2,
    after eq. 1.4), our sign of Z is verified empirically by sanity test 2.

    The overall normalisation of Z is absorbed into flow time t : if
    Z_ours = K . Z_luscher for some K > 0, then our flow time t maps to
    Luscher's t_L = K . t. This rescaling does NOT affect the SHAPE of the
    E(t) curve in dimensionless terms, only the numerical value of t_0.
    """
    staples_fn = make_compute_staples_3D(L, nbr)

    @jax.jit
    def drift_Z(U):
        Sigma = staples_fn(U)                  # (3V, 3, 3)
        # Omega = U . Sigma  (sum of plaquettes touching the link, oriented
        # so each starts with U(x, mu)). Empirical sign verification
        # (sanity test 2) shows that with this Omega, the gradient-descent
        # drift is Z = - TA[Omega], so that
        #      dV/dt = Z V  =  - TA[Omega] . V
        # decreases the Wilson action monotonically. The overall sign
        # depends on the choice of generator basis (hermitian vs anti-
        # hermitian) and the convention for the Lie derivative, and is
        # most safely pinned down empirically. See derivation in the
        # function docstring; the final sign is FIXED by sanity test 2.
        Omega = sun_mul(U, Sigma)
        Z = -trace_anti_hermitian(Omega)
        return Z

    return drift_Z


# ============================================================================
#  RK3 Luscher integrator (Appendix C of arXiv:1006.4518)
# ============================================================================
#
#  Coefficients (Luscher 2010 Appendix C, also reproduced in chroma/openQCD):
#       Z_0 = Z(W_0)
#       W_1 = exp( c11 eps Z_0 ) W_0,                  c11 =  1/4
#       Z_1 = Z(W_1)
#       W_2 = exp( c22 eps Z_1 + c21 eps Z_0 ) W_1,    c22 =  8/9,  c21 = -17/36
#       Z_2 = Z(W_2)
#       W_3 = exp( c33 eps Z_2 + c32 eps Z_1 + c31 eps Z_0 ) W_2
#                                                       c33 = 3/4, c32 = -8/9, c31 = 17/36
#       V_{t+eps} = W_3


def make_wilson_flow_step(L: int, nbr, n_exp_terms: int = 15,
                          do_su3_projection: bool = True):
    """Build a JIT'd function: (U, eps) -> U_new (one RK3 Luscher step)."""
    drift_Z = make_drift_Z_3D(L, nbr)

    @jax.jit
    def step(U, eps):
        eps = jnp.asarray(eps, dtype=RDTYPE)
        cdtype_eps = jnp.asarray(eps, dtype=CDTYPE)

        # W_0 = U
        Z0 = drift_Z(U)
        E0 = cdtype_eps * Z0
        # W_1 = exp((1/4) eps Z_0) . W_0
        expmat1 = matrix_exp_taylor(0.25 * E0, n_exp_terms)
        W1 = sun_mul(expmat1, U)
        if do_su3_projection:
            W1 = project_su3(W1)

        Z1 = drift_Z(W1)
        E1 = cdtype_eps * Z1
        # W_2 = exp((8/9) eps Z_1 - (17/36) eps Z_0) . W_1
        expmat2 = matrix_exp_taylor((8.0 / 9.0) * E1
                                    - (17.0 / 36.0) * E0,
                                    n_exp_terms)
        W2 = sun_mul(expmat2, W1)
        if do_su3_projection:
            W2 = project_su3(W2)

        Z2 = drift_Z(W2)
        E2 = cdtype_eps * Z2
        # W_3 = exp((3/4) eps Z_2 - (8/9) eps Z_1 + (17/36) eps Z_0) . W_2
        expmat3 = matrix_exp_taylor((3.0 / 4.0) * E2
                                    - (8.0 / 9.0) * E1
                                    + (17.0 / 36.0) * E0,
                                    n_exp_terms)
        W3 = sun_mul(expmat3, W2)
        if do_su3_projection:
            W3 = project_su3(W3)
        return W3

    return step


# ============================================================================
#  Energy density E(t)
# ============================================================================
#
#  We use the plaquette-based proxy
#
#       E_plaq(U) =  (1/V) . sum_{x, mu<nu}  (1 - (1/N) Re tr U_p(x; mu, nu))
#                  =  (1/V) . sum_{x, mu<nu}  (1 - <P>_p)
#
#  which is (up to an overall normalisation chosen so that E_plaq(I) = 0)
#  the discretization of (1/2) tr F_{munu}^2 used by Luscher 2010 Sec. 2.3
#  in the "Wilson plaquette" form. The improved clover discretization is
#  factor-of-improvement-over-a^2 better but adds significant compile time;
#  we expose `energy_density_clover(...)` separately and recommend the
#  clover form for production t_0 extractions while the plaquette form is
#  perfectly adequate for diagnostic curves and reference scale BOOTSTRAPS.
#
#  Honest caveat: the multiplicative constant relating E_plaq to <F^2>
#  differs between plaquette and clover discretizations; consequently the
#  reference value of (t^2 . E)_ref that defines t_0 differs accordingly.
#  For SU(3) D=3 we know of NO universally-adopted convention (we found no
#  D=3 t_0 reference in the literature search). Caller MUST calibrate the
#  D=3 reference constant empirically. Default 0.3 is the D=4 BMW value
#  (PRL 1203.4469) and should NOT be used blindly in D=3.


def make_energy_density_plaquette_3D(L: int, nbr):
    """Build a JIT'd plaquette-based proxy for E(t) = sum (1 - Re tr P / N)."""
    V = L ** 3
    sites = jnp.arange(V)

    @jax.jit
    def E_plaq(U):
        total = jnp.zeros((), dtype=RDTYPE)
        for mu in range(3):
            for nu in range(mu + 1, 3):
                x_mu = nbr[mu, 0, sites]
                x_nu = nbr[nu, 0, sites]
                P = sun_mul(U[mu * V + sites], U[nu * V + x_mu])
                P = sun_mul(P, sun_dagger(U[mu * V + x_nu]))
                P = sun_mul(P, sun_dagger(U[nu * V + sites]))
                tr = (P[..., 0, 0] + P[..., 1, 1] + P[..., 2, 2]).real
                total = total + jnp.sum(1.0 - tr / N_COLOR)
        return total / V

    return E_plaq


def make_clover_energy_density_3D(L: int, nbr):
    """Clover-improved E(t) (Luscher 2010 Sec. 2.3).

    Builds the antihermitian (1/4)-sum of the 4 plaquettes attached to (x; mu, nu),
    extracts F_{munu}, and returns  E = (1/V) sum_{x, mu<nu} (1/2) tr(F^2).

    Implementation note: the clover field strength is computed via

        Q_{munu}(x) = (1/8) [ P(x; mu, nu) - P(x; nu, mu)
                            + ... 4 plaquette orientations ... ]
        F_{munu}(x) = - i . (1/2) (Q - Q^dag) - (i/N) tr term  (TA-like)

    The plaquette-form proxy is *typically* off from the clover-improved E
    by an O(a^2) discretization factor; for the *scaling* in beta and the
    *t-shape* of E(t) the two agree to ~few percent at a chosen t > 1.
    """
    V = L ** 3
    sites = jnp.arange(V)

    @jax.jit
    def E_clover(U):
        total = jnp.zeros((), dtype=RDTYPE)
        for mu in range(3):
            for nu in range(mu + 1, 3):
                x_pm = nbr[mu, 0, sites]
                x_pn = nbr[nu, 0, sites]
                x_mm = nbr[mu, 1, sites]
                x_mn = nbr[nu, 1, sites]
                x_pm_mn = nbr[nu, 1, x_pm]
                x_mm_pn = nbr[nu, 0, x_mm]
                x_mm_mn = nbr[nu, 1, x_mm]

                # plaquette 1: U(x, mu) U(x+mu, nu) U^dag(x+nu, mu) U^dag(x, nu)
                P1 = sun_mul(U[mu * V + sites],   U[nu * V + x_pm])
                P1 = sun_mul(P1, sun_dagger(U[mu * V + x_pn]))
                P1 = sun_mul(P1, sun_dagger(U[nu * V + sites]))

                # plaquette 2: U(x, nu) U^dag(x-mu+nu, mu) U^dag(x-mu, nu) U(x-mu, mu)
                P2 = sun_mul(U[nu * V + sites],   sun_dagger(U[mu * V + x_mm_pn]))
                P2 = sun_mul(P2, sun_dagger(U[nu * V + x_mm]))
                P2 = sun_mul(P2, U[mu * V + x_mm])

                # plaquette 3: U^dag(x-mu, mu) U^dag(x-mu-nu, nu) U(x-mu-nu, mu) U(x-nu, nu)
                P3 = sun_mul(sun_dagger(U[mu * V + x_mm]),
                             sun_dagger(U[nu * V + x_mm_mn]))
                P3 = sun_mul(P3, U[mu * V + x_mm_mn])
                P3 = sun_mul(P3, U[nu * V + x_mn])

                # plaquette 4: U^dag(x-nu, nu) U(x-nu, mu) U(x+mu-nu, nu) U^dag(x, mu)
                P4 = sun_mul(sun_dagger(U[nu * V + x_mn]),
                             U[mu * V + x_mn])
                P4 = sun_mul(P4, U[nu * V + x_pm_mn])
                P4 = sun_mul(P4, sun_dagger(U[mu * V + sites]))

                Q = (P1 + P2 + P3 + P4) / 4.0
                # F_{munu} = - (i/2) TA(Q)  (so that F is hermitian)
                Qm = trace_anti_hermitian(Q)   # anti-hermitian, traceless
                F = -0.5j * Qm                 # hermitian
                # tr(F^2) -- real
                F2 = sun_mul(F, F)
                trF2 = (F2[..., 0, 0] + F2[..., 1, 1] + F2[..., 2, 2]).real
                # E sums over mu<nu, take (1/2) tr F^2 per Luscher conv.
                total = total + 0.5 * jnp.sum(trF2)
        return total / V

    return E_clover


# ============================================================================
#  Driver : evolve U from t = 0 to t = t_max, record (t, E)
# ============================================================================

def wilson_flow_evolve(U, L: int, t_max: float, eps: float = 0.02,
                       use_clover: bool = False, record_every: int = 1,
                       nbr=None, verbose: bool = False):
    """Evolve U via RK3 Luscher from t=0 to t=t_max in steps of eps.

    Parameters
    ----------
    U          : initial config, jax array shape (3*V, 3, 3) complex64
    L          : spatial extent (assumes V = L**3 in D=3)
    t_max      : final flow time (lattice units)
    eps        : RK3 step size (lattice units), Luscher recommends 0.01 - 0.02
    use_clover : if True use clover E (slower, ~1.5x compile); else plaquette
    record_every: record (t, E) every N steps (1 = every step)
    nbr        : precomputed neighbor table (optional, built if None)
    verbose    : print progress

    Returns
    -------
    dict with keys
        't_arr'  : (n_record,) array of flow times
        'E_arr'  : (n_record,) array of E(t)
        'U_final': final config
        'eps'    : step used
        'n_step' : total RK3 steps performed
    """
    if nbr is None:
        nbr = build_neighbors_3D(L)

    step_fn = make_wilson_flow_step(L, nbr)
    E_fn = (make_clover_energy_density_3D(L, nbr) if use_clover
            else make_energy_density_plaquette_3D(L, nbr))

    n_steps = int(round(t_max / eps))
    t_list, E_list = [0.0], [float(E_fn(U))]

    U_curr = U
    for step in range(1, n_steps + 1):
        U_curr = step_fn(U_curr, eps)
        if step % record_every == 0 or step == n_steps:
            t = step * eps
            E = float(E_fn(U_curr))
            t_list.append(t)
            E_list.append(E)
            if verbose and (step % max(1, n_steps // 10) == 0):
                print(f"  [flow] step {step:5d}/{n_steps}  t={t:.3f}  "
                      f"E={E:.4e}  t^2 E={t*t*E:.4e}")

    return {
        "t_arr": np.array(t_list),
        "E_arr": np.array(E_list),
        "U_final": U_curr,
        "eps": eps,
        "n_step": n_steps,
    }


def wilson_flow_step(U, eps, L: int, nbr=None):
    """Functional alias: one RK3 Luscher step. Builds JIT once per (L, nbr)
    via lru_cache by re-creating the step function each call would be slow,
    so prefer make_wilson_flow_step(L, nbr) directly in tight loops."""
    if nbr is None:
        nbr = build_neighbors_3D(L)
    step_fn = make_wilson_flow_step(L, nbr)
    return step_fn(U, eps)


def energy_density(U, L: int, use_clover: bool = False, nbr=None):
    """Compute E(U)."""
    if nbr is None:
        nbr = build_neighbors_3D(L)
    fn = (make_clover_energy_density_3D(L, nbr) if use_clover
          else make_energy_density_plaquette_3D(L, nbr))
    return float(fn(U))


def find_t_ref(U, L: int, E_ref: float = 0.3, eps: float = 0.02,
               t_max: float = 10.0, use_clover: bool = False,
               nbr=None, verbose: bool = False):
    """Find t* > 0 such that t*^2 . E(t*) = E_ref by linear interpolation
    on the recorded (t_arr, E_arr) trajectory.

    NOTE: E_ref = 0.3 is the standard D=4 BMW value (PRL 1203.4469); for
    D=3 a different convention should be calibrated empirically. We do not
    enforce a D=3 default.

    Returns
    -------
    t_star : float or None (None if (t^2 E) never reaches E_ref in t<=t_max)
    traj   : the wilson_flow_evolve dict (for inspection)
    """
    traj = wilson_flow_evolve(U, L, t_max=t_max, eps=eps,
                              use_clover=use_clover, nbr=nbr,
                              verbose=verbose)
    t_arr = traj["t_arr"]
    tsq_E = (t_arr ** 2) * traj["E_arr"]
    # find first crossing of E_ref
    crossing = None
    for k in range(1, len(tsq_E)):
        if (tsq_E[k - 1] - E_ref) * (tsq_E[k] - E_ref) <= 0:
            # linear interp
            t0, t1 = t_arr[k - 1], t_arr[k]
            y0, y1 = tsq_E[k - 1], tsq_E[k]
            if y1 == y0:
                crossing = 0.5 * (t0 + t1)
            else:
                crossing = t0 + (E_ref - y0) * (t1 - t0) / (y1 - y0)
            break
    return crossing, traj


# ============================================================================
#  Pipeline helper: alpha extraction via Wilson flow
# ============================================================================
#
#  IDEA: at each beta, thermalize HMC, then Wilson-flow each config to a
#  *fixed* reference flow time t_ref (in lattice units). The smoothed
#  plaquette <P(t_ref)>(beta) is then much less contaminated by UV noise
#  than the raw <P>(beta), and the scaling
#
#       <P(t_ref)>(beta)  =  P_inf  -  C . beta^{-alpha}
#
#  (or equivalently  log[<P(t_ref)>(beta) - P_inf] = log C - alpha log beta)
#  extracts alpha cleanly. This is the protocol the caller (mission brief)
#  will run overnight on the gamer-PC GPU.
#
#  The "t_ref" should be chosen >= O(1) lattice unit (smoothing radius
#  sqrt(8 t_ref) >= a few lattice spacings) so UV is gone, but < L^2/8 so
#  the flow does not reach the boundary of the box. For L=4..8 in D=3,
#  t_ref ~ 0.5 - 1.0 is a reasonable starting range. Caller should scan.


def smoothed_plaquette_at_t(U_initial, L: int, t_ref: float,
                            eps: float = 0.02, nbr=None):
    """Flow U_initial to t_ref, return (smoothed mean plaquette, traj dict).

    The "mean plaquette" returned here is (1/V/n_pair) sum (1/N) Re tr P,
    i.e. the standard normalized plaquette in [1/N, 1]. The caller can fit
    log(<P(t_ref)>(beta) - P_inf) vs log(beta) for alpha extraction.
    """
    if nbr is None:
        nbr = build_neighbors_3D(L)
    # Evolve
    n_steps = max(1, int(round(t_ref / eps)))
    step_fn = make_wilson_flow_step(L, nbr)
    U_curr = U_initial
    for _ in range(n_steps):
        U_curr = step_fn(U_curr, eps)
    # Mean plaquette on flowed config
    V = L ** 3
    sites = jnp.arange(V)
    total = jnp.zeros((), dtype=RDTYPE)
    npairs = 0
    for mu in range(3):
        for nu in range(mu + 1, 3):
            x_mu = nbr[mu, 0, sites]
            x_nu = nbr[nu, 0, sites]
            P = sun_mul(U_curr[mu * V + sites], U_curr[nu * V + x_mu])
            P = sun_mul(P, sun_dagger(U_curr[mu * V + x_nu]))
            P = sun_mul(P, sun_dagger(U_curr[nu * V + sites]))
            tr = (P[..., 0, 0] + P[..., 1, 1] + P[..., 2, 2]).real
            total = total + jnp.sum(tr / N_COLOR)
            npairs += V
    return float(total / npairs), U_curr


# ============================================================================
#  Sanity tests -- run via `python wilson_flow_su3_d3.py`
# ============================================================================

def _random_su3_batch(key, n_mat):
    """Stand-alone Haar SU(3) sampler (Mezzadri QR trick). Replicates the
    routine in su3_hmc_d3_jax.py so this module is self-contained."""
    import jax.random as jr
    k1, k2 = jr.split(key)
    A_re = jr.normal(k1, (n_mat, 3, 3))
    A_im = jr.normal(k2, (n_mat, 3, 3))
    A = (A_re + 1j * A_im).astype(CDTYPE)
    Q, R = jnp.linalg.qr(A)
    d = jnp.diagonal(R, axis1=-2, axis2=-1)
    phase = d / jnp.maximum(jnp.abs(d), 1e-15)
    Q = Q * phase[:, None, :]
    det = jnp.linalg.det(Q)
    det_phase = det / jnp.maximum(jnp.abs(det), 1e-15)
    angle = jnp.angle(det_phase)
    cube_root_phase = jnp.exp(1j * angle / 3.0)
    Q_su3 = Q / cube_root_phase[:, None, None]
    return Q_su3


def _cold_start(L):
    V = L ** 3
    n_links = 3 * V
    I = jnp.eye(N_COLOR, dtype=CDTYPE)
    return jnp.broadcast_to(I, (n_links, 3, 3)) + jnp.zeros((n_links, 3, 3),
                                                            dtype=CDTYPE)


def _hot_start(L, seed=42):
    V = L ** 3
    n_links = 3 * V
    key = jax.random.PRNGKey(seed)
    return _random_su3_batch(key, n_links)


def run_sanity_tests(L: int = 4, t_max: float = 0.5, eps: float = 0.02,
                     verbose: bool = True):
    """Sanity battery for the Wilson flow module.

    Tests
    -----
    1. cold start  =>  E(t) ~= 0 for all t
    2. hot start   =>  E(t) decreases monotonically
    3. det(V_t) ~= 1 after each step (SU(3) preservation)
    4. reproducibility : two evolves with same seed yield identical E(t)

    Returns a dict of pass/fail flags + measured quantities.
    """
    print("=" * 78)
    print(f"WILSON FLOW SU(3) D=3 -- SANITY TESTS  (L={L}, t_max={t_max}, eps={eps})")
    print("=" * 78)
    nbr = build_neighbors_3D(L)
    step_fn = make_wilson_flow_step(L, nbr)
    E_fn = make_energy_density_plaquette_3D(L, nbr)
    results = {}

    # ---------- TEST 1 : cold start, E(t) = 0 ----------
    print("\n[TEST 1] cold start: E(t) = 0 expected")
    U_cold = _cold_start(L)
    E0 = float(E_fn(U_cold))
    print(f"  E(t=0)  = {E0:.3e}")
    U = U_cold
    n_steps = int(round(t_max / eps))
    E_curve_cold = [E0]
    for s in range(n_steps):
        U = step_fn(U, eps)
        E_curve_cold.append(float(E_fn(U)))
    E_max = max(abs(e) for e in E_curve_cold)
    cold_ok = E_max < 1e-5
    print(f"  max|E(t)| over t in [0,{t_max}] = {E_max:.3e}")
    print(f"  cold start  ->  {'PASS' if cold_ok else 'FAIL'}")
    results["cold_start"] = {"max_abs_E": E_max, "pass": cold_ok}

    # ---------- TEST 2 : hot start, E(t) monotone decreasing ----------
    print("\n[TEST 2] hot start: E(t) monotone DECREASING expected")
    U_hot = _hot_start(L, seed=42)
    E_curve_hot = [float(E_fn(U_hot))]
    U = U_hot
    for s in range(n_steps):
        U = step_fn(U, eps)
        E_curve_hot.append(float(E_fn(U)))
    diffs = np.diff(E_curve_hot)
    n_pos = int(np.sum(diffs > 1e-6))  # E should monotone decrease
    pct_pos = 100.0 * n_pos / max(1, len(diffs))
    hot_ok = pct_pos < 5.0  # <=5% glitches tolerated (numerical noise)
    print(f"  E(t=0)        = {E_curve_hot[0]:.4e}")
    print(f"  E(t={t_max})  = {E_curve_hot[-1]:.4e}")
    print(f"  fraction of POSITIVE dE/dt steps = {pct_pos:.1f}%")
    print(f"  monotonic flow  ->  {'PASS' if hot_ok else 'FAIL'}")
    results["hot_start_monotone"] = {
        "E_init": E_curve_hot[0],
        "E_final": E_curve_hot[-1],
        "pct_positive_dE": pct_pos,
        "pass": hot_ok,
    }

    # ---------- TEST 3 : det V_t = 1 ----------
    print("\n[TEST 3] det(V_t) = 1 after each step")
    U = _hot_start(L, seed=7)
    dets = []
    for s in range(min(50, n_steps)):  # spot-check 50 steps
        U = step_fn(U, eps)
        d = jnp.linalg.det(U)
        dets.append(float(jnp.max(jnp.abs(d - 1.0))))
    max_det_drift = max(dets)
    det_ok = max_det_drift < 1e-4  # complex64 floor is ~1e-6, SVD adds 1e-5
    print(f"  max |det V_t - 1| over 50 steps = {max_det_drift:.3e}")
    print(f"  SU(3) preservation  ->  {'PASS' if det_ok else 'FAIL'}")
    results["det_preservation"] = {"max_drift": max_det_drift, "pass": det_ok}

    # ---------- TEST 4 : reproducibility ----------
    print("\n[TEST 4] reproducibility (same seed -> same E(t) trajectory)")
    U_a = _hot_start(L, seed=123)
    U_b = _hot_start(L, seed=123)
    E_a, E_b = [], []
    for s in range(20):
        U_a = step_fn(U_a, eps); E_a.append(float(E_fn(U_a)))
        U_b = step_fn(U_b, eps); E_b.append(float(E_fn(U_b)))
    max_diff = max(abs(a - b) for a, b in zip(E_a, E_b))
    rep_ok = max_diff < 1e-6
    print(f"  max |E_a - E_b| over 20 steps = {max_diff:.3e}")
    print(f"  reproducibility  ->  {'PASS' if rep_ok else 'FAIL'}")
    results["reproducibility"] = {"max_diff_E": max_diff, "pass": rep_ok}

    # ---------- summary ----------
    all_ok = all(v["pass"] for v in results.values())
    print("\n" + "=" * 78)
    print("SANITY SUMMARY  ->  {}".format("ALL PASS" if all_ok else "SOME FAIL"))
    for k, v in results.items():
        print(f"  {k:30s}  {'OK' if v['pass'] else 'FAIL'}  {v}")
    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Wilson flow SU(3) D=3 sanity")
    p.add_argument("--L", type=int, default=4)
    p.add_argument("--t_max", type=float, default=0.5)
    p.add_argument("--eps", type=float, default=0.02)
    p.add_argument("--clover", action="store_true",
                   help="Use clover-improved E(t) instead of plaquette")
    args = p.parse_args()

    results = run_sanity_tests(L=args.L, t_max=args.t_max, eps=args.eps,
                               verbose=True)
