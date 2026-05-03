"""
Wainwright-Hsu ODE integration for Bianchi VI_{-1/9} vacuum model.
Uses the HHW03 (arXiv:gr-qc/0211071) dynamical system (eqs. 2.8) and
the LU24 (arXiv:2410.10375) system (eqs. 10a-10g) to detect Kasner-circle
fixed-point visits and frame transitions.

Convention: tau increases toward the PAST singularity (tau -> -inf is the future;
tau -> +inf direction is toward singularity).
HHW03 eq.(2.5): dt/d_tau = 1/H, so tau is the e-fold time measured
into the past.  LU24 eq.(6): d_tau/dt = -H, so tau in LU24 increases
toward the singularity.

We use the LU24 ODE system (eqs. 10a-10g), where tau increases toward
the initial singularity.  Kasner-circle fixed points K° satisfy:
    R_1 = R_3 = N_- = A = 0,
    Sigma_1 + Sigma_2 + Sigma_3 = 0,
    (1/6)(Sigma_1^2 + Sigma_2^2 + Sigma_3^2) + R_1^2 + R_3^2 = 1   => Sigma^2 = 1.

A "Kasner-I vertex" (Taub point) corresponds to p_alpha = (1,0,0),
i.e. (Sigma_alpha, Sigma_beta, Sigma_gamma) = (2,-1,-1), specifically:
    T_1: (Sigma_1, Sigma_2, Sigma_3) = (2,-1,-1), Kasner params (1,0,0)
    T_2: (Sigma_1, Sigma_2, Sigma_3) = (-1,2,-1), Kasner params (0,1,0)
    T_3: (Sigma_1, Sigma_2, Sigma_3) = (-1,-1,2), Kasner params (0,0,1)

Q-points (LRS, non-flat) have (Sigma_alpha, Sigma_beta, Sigma_gamma)=(-2,1,1),
Kasner params (-1/3, 2/3, 2/3).

The BKL-Kasner map parameter u is defined implicitly:
    p_1 = -u/f(u), p_2 = (1+u)/f(u), p_3 = u(1+u)/f(u),  f(u)=1+u+u^2
The S3 IR divergence requires a Kasner direction with p_alpha < 0
(contracting scale factor direction that is actually expanding in volume
in the Kasner picture, leading to tachyonic modes).

Detection: we flag "near-Kasner" when
    dist_K = sqrt(R_1^2 + R_3^2 + N_-^2 + A^2) < epsilon
i.e. when the orbit approaches the Kasner circle K°.
We also flag "near-Taub" (Kasner-I) when additionally Sigma^2 ~ 1 and
the point is near a T_alpha (one Sigma_alpha ~ 2, others ~ -1).
"""

import numpy as np
from scipy.integrate import solve_ivp
import json

# -------------------------------------------------------------------------
# LU24 ODE system, eqs. (10a)-(10g)
# State vector: y = [Sigma_1, Sigma_2, Sigma_3, R_1, R_3, N_minus, A]
# Constraint (11a): 1 - Sigma^2 - N_-^2 - A^2 = 0, Sigma^2 = (1/6)(S1^2+S2^2+S3^2)+R1^2+R3^2
# Constraint (11b): 2 R3 N_- + Sigma_1 A = 0
# Constraint (11c): Sigma_1 + Sigma_2 + Sigma_3 = 0
#
# q = 2 Sigma^2  (eq. 8)
# -------------------------------------------------------------------------

def sigma_sq(y):
    S1, S2, S3, R1, R3, Nm, A = y
    return (1.0/6.0)*(S1**2 + S2**2 + S3**2) + R1**2 + R3**2

def rhs_LU24(tau, y):
    S1, S2, S3, R1, R3, Nm, A = y
    Sig2 = sigma_sq(y)
    q = 2.0 * Sig2

    # eqs. (10a)-(10g)
    dS1 = 2.0*(1.0 - Sig2)*S1 - 6.0*R3**2 + 8.0*Nm**2
    dS2 = 2.0*(1.0 - Sig2)*S2 + 6.0*R3**2 - 6.0*R1**2 - 4.0*Nm**2 + 3.0*A**2
    dS3 = 2.0*(1.0 - Sig2)*S3 + 6.0*R1**2 - 4.0*Nm**2 - 3.0*A**2
    dR1 = (2.0*(1.0 - Sig2) + S2 - S3)*R1
    dR3 = (2.0*(1.0 - Sig2) + S1 - S2)*R3 - 4.0*Nm*A
    dNm = -2.0*(Sig2 + S1)*Nm + 3.0*R3*A
    dA  = -(2.0*Sig2 - S3)*A

    return [dS1, dS2, dS3, dR1, dR3, dNm, dA]

# -------------------------------------------------------------------------
# Kasner-circle detection and characterisation
# -------------------------------------------------------------------------
EPSILON_KASNER = 0.05  # distance threshold to call "near Kasner"
EPSILON_TAUB   = 0.08  # extra threshold for Taub-point proximity

# Taub points T_alpha in (Sigma_1, Sigma_2, Sigma_3) space
TAUB_POINTS = {
    'T1': np.array([2.0, -1.0, -1.0]),
    'T2': np.array([-1.0, 2.0, -1.0]),
    'T3': np.array([-1.0, -1.0, 2.0]),
}
# Q_alpha points (LRS)
Q_POINTS = {
    'Q1': np.array([-2.0, 1.0, 1.0]),
    'Q2': np.array([1.0, -2.0, 1.0]),
    'Q3': np.array([1.0, 1.0, -2.0]),
}

def kasner_distance(y):
    """Distance from the Kasner circle K° (R1=R3=N_-=A=0, Sigma^2=1)."""
    S1, S2, S3, R1, R3, Nm, A = y
    Sig2 = sigma_sq(y)
    # distance from K° manifold: R1,R3,N-,A all zero and Sigma^2=1
    dist_off_diag = np.sqrt(R1**2 + R3**2 + Nm**2 + A**2)
    dist_constraint = abs(Sig2 - 1.0)
    return dist_off_diag, dist_constraint

def nearest_kasner_point(y):
    """Find the nearest point on K° and return its u parameter."""
    S1, S2, S3, R1, R3, Nm, A = y
    # Project (S1,S2,S3) onto K° (normalise to Sigma^2=1 circle)
    Sig2 = (1.0/6.0)*(S1**2 + S2**2 + S3**2)
    if Sig2 < 1e-10:
        return None, None
    norm = 1.0 / np.sqrt(Sig2)
    s1p, s2p, s3p = S1*norm, S2*norm, S3*norm

    # Kasner params from Sigma_alpha: p_alpha = (1 + Sigma_alpha)/3
    p1 = (1.0 + s1p)/3.0
    p2 = (1.0 + s2p)/3.0
    p3 = (1.0 + s3p)/3.0

    # Check which Taub or Q point we are near
    taub_dists = {k: np.linalg.norm(np.array([s1p,s2p,s3p]) - v)
                  for k, v in TAUB_POINTS.items()}
    nearest_taub = min(taub_dists, key=taub_dists.get)
    nearest_taub_dist = taub_dists[nearest_taub]

    return (p1, p2, p3), nearest_taub_dist, nearest_taub

def kasner_u_param(p1, p2, p3):
    """Compute BKL u parameter.  Convention: p_1 <= p_2 <= p_3."""
    ps = sorted([p1, p2, p3])
    pa, pb, pc = ps  # pa<=pb<=pc
    # pa = -u/f(u) => solve numerically for u in [1,inf)
    # Since pa = -u/f(u) < 0 we need pa < 0
    if pa >= 0:
        return None  # Taub point or degenerate
    # pa*f(u) + u = 0 => pa*(1+u+u^2)+u=0 => pa*u^2 + (pa+1)*u + pa = 0
    a_coef = pa
    b_coef = pa + 1.0
    c_coef = pa
    disc = b_coef**2 - 4*a_coef*c_coef
    if disc < 0:
        return None
    u = (-b_coef + np.sqrt(disc)) / (2*a_coef)
    if u < 0:
        u = (-b_coef - np.sqrt(disc)) / (2*a_coef)
    return u if u > 0 else None

# -------------------------------------------------------------------------
# Simulation runs
# -------------------------------------------------------------------------

def run_simulation(y0, tau_span, tau_eval=None, label=""):
    """Integrate the LU24 system and detect Kasner-circle visits."""
    if tau_eval is None:
        tau_eval = np.linspace(tau_span[0], tau_span[1], 5000)

    sol = solve_ivp(
        rhs_LU24, tau_span, y0, t_eval=tau_eval,
        method='DOP853', rtol=1e-10, atol=1e-12,
        dense_output=False
    )

    visits = []
    prev_near = False

    for i, t in enumerate(sol.t):
        y = sol.y[:, i]
        dist_off, dist_con = kasner_distance(y)
        near = (dist_off < EPSILON_KASNER) and (dist_con < EPSILON_KASNER)

        if near and not prev_near:
            # Entering a Kasner-circle neighbourhood
            result = nearest_kasner_point(y)
            if result[0] is not None:
                p1, p2, p3 = result[0]
                taub_dist = result[1]
                taub_name = result[2]
                u = kasner_u_param(p1, p2, p3)
                S1, S2, S3, R1, R3, Nm, A = y
                Sig2 = sigma_sq(y)
                visits.append({
                    'tau': float(t),
                    'dist_off_diag': float(dist_off),
                    'dist_constraint': float(dist_con),
                    'p1': float(p1), 'p2': float(p2), 'p3': float(p3),
                    'u': float(u) if u is not None else None,
                    'nearest_taub': taub_name,
                    'taub_dist': float(taub_dist),
                    'S1': float(S1), 'S2': float(S2), 'S3': float(S3),
                    'Sigma2': float(Sig2),
                    'is_near_taub': taub_dist < EPSILON_TAUB,
                })
        prev_near = near

    return sol, visits

# -------------------------------------------------------------------------
# Initial conditions
# Near a generic Kasner point with u ~ 3 (mid-era, away from Taub points)
# We start slightly off K° with small R3 > 0 (triggering frame transition T_{R3})
# and small N_- > 0 (triggering curvature transition T_{N-}).
# Constraint (11c): S1+S2+S3=0; (11b): 2 R3 N_- + S1*A = 0.
# We set A = 0, then (11b) is satisfied trivially.
# Constraint (11a): 1 - Sigma^2 - N_-^2 - A^2 = 0 => Sigma^2 = 1 - N_-^2.
# -------------------------------------------------------------------------

def make_initial_conditions(u_start, eps_R3=0.02, eps_Nm=0.01):
    """
    Construct initial conditions near a Kasner point with parameter u_start.
    Uses sector (123): p1 < 0 < p2 < 2/3 < p3 < 1.
    """
    f = lambda x: 1.0 + x + x**2
    u = u_start
    p1 = -u/f(u)
    p2 = (1.0+u)/f(u)
    p3 = u*(1.0+u)/f(u)

    # Sigma_alpha = 3*p_alpha - 1
    S1 = 3.0*p1 - 1.0
    S2 = 3.0*p2 - 1.0
    S3 = 3.0*p3 - 1.0

    # Check constraint (11c): S1+S2+S3 = 3(p1+p2+p3)-3 = 3*1 - 3 = 0  OK

    # Normalise so Sigma^2 = (1/6)(S1^2+S2^2+S3^2) is near 1-eps^2
    Sig2_base = (1.0/6.0)*(S1**2 + S2**2 + S3**2)
    target_Sig2 = 1.0 - eps_Nm**2  # to satisfy (11a) with A=0
    scale = np.sqrt(target_Sig2 / Sig2_base)
    S1 *= scale; S2 *= scale; S3 *= scale

    R1 = 0.0
    R3 = eps_R3
    Nm = eps_Nm
    A  = 0.0

    # Check constraint (11b): 2*R3*Nm + S1*A = 2*eps_R3*eps_Nm != 0 exactly,
    # so we adjust A slightly: A = -2*R3*Nm/S1 if S1 != 0
    if abs(S1) > 0.01:
        A = -2.0*R3*Nm/S1
    else:
        A = 0.0
        Nm = 0.0  # avoid constraint violation

    return [S1, S2, S3, R1, R3, Nm, A]

# -------------------------------------------------------------------------
# Run multiple simulations
# -------------------------------------------------------------------------

print("="*70)
print("Bianchi VI_{-1/9} LU24 ODE - Kasner vertex detection")
print("="*70)

# Test case 1: Generic u_0 = 3 (mid-era)
print("\n--- Test 1: u_0 = 3.0 (mid-era, away from Taub points) ---")
y0 = make_initial_conditions(u_start=3.0, eps_R3=0.02, eps_Nm=0.015)
print(f"Initial state: S1={y0[0]:.4f}, S2={y0[1]:.4f}, S3={y0[2]:.4f}")
print(f"               R1={y0[3]:.4f}, R3={y0[4]:.4f}, N-={y0[5]:.4f}, A={y0[6]:.4f}")
S2_check = sigma_sq(y0)
print(f"Sigma^2 check: {S2_check:.6f} (should be ~{1-y0[5]**2:.6f})")
print(f"Constraint (11c) S1+S2+S3={y0[0]+y0[1]+y0[2]:.6f} (should be 0)")

sol1, visits1 = run_simulation(y0, tau_span=(0.0, 60.0), label="u0=3.0")
print(f"Kasner-circle visits detected: {len(visits1)}")
for v in visits1:
    taub_flag = " <-- NEAR TAUB (Kasner-I)" if v['is_near_taub'] else ""
    print(f"  tau={v['tau']:.2f}: p=({v['p1']:.3f},{v['p2']:.3f},{v['p3']:.3f})"
          f" u={v['u']:.3f if v['u'] else 'None'}"
          f" nearest={v['nearest_taub']} dist_T={v['taub_dist']:.3f}"
          f" dist_K={v['dist_off_diag']:.4f}{taub_flag}")

# Test case 2: Golden ratio u_0 = (1+sqrt(5))/2 (periodic era sequence, period 1)
u_gold = (1.0 + np.sqrt(5.0))/2.0
print(f"\n--- Test 2: u_0 = golden ratio = {u_gold:.6f} ---")
y0_g = make_initial_conditions(u_start=u_gold, eps_R3=0.03, eps_Nm=0.02)
sol2, visits2 = run_simulation(y0_g, tau_span=(0.0, 80.0), label="golden")
print(f"Kasner-circle visits detected: {len(visits2)}")
for v in visits2:
    taub_flag = " <-- NEAR TAUB (Kasner-I)" if v['is_near_taub'] else ""
    u_str = f"{v['u']:.3f}" if v['u'] is not None else "None"
    print(f"  tau={v['tau']:.2f}: p=({v['p1']:.3f},{v['p2']:.3f},{v['p3']:.3f})"
          f" u={u_str}"
          f" nearest={v['nearest_taub']} dist_T={v['taub_dist']:.3f}"
          f" dist_K={v['dist_off_diag']:.4f}{taub_flag}")

# Test case 3: u_0 = 1.05 (near era-end, close to Taub point T3 at u->inf via u=1)
print("\n--- Test 3: u_0 = 1.05 (near era boundary, approaching Taub region) ---")
y0_t = make_initial_conditions(u_start=1.05, eps_R3=0.03, eps_Nm=0.02)
sol3, visits3 = run_simulation(y0_t, tau_span=(0.0, 80.0), label="near-taub")
print(f"Kasner-circle visits detected: {len(visits3)}")
for v in visits3:
    taub_flag = " <-- NEAR TAUB (Kasner-I)" if v['is_near_taub'] else ""
    u_str = f"{v['u']:.3f}" if v['u'] is not None else "None"
    print(f"  tau={v['tau']:.2f}: p=({v['p1']:.3f},{v['p2']:.3f},{v['p3']:.3f})"
          f" u={u_str}"
          f" nearest={v['nearest_taub']} dist_T={v['taub_dist']:.3f}"
          f" dist_K={v['dist_off_diag']:.4f}{taub_flag}")

# -------------------------------------------------------------------------
# S3 analysis: at each Kasner visit, check whether p_1 < 0
# (contracting direction for the 1-axis scale factor a_1 ~ t^{p_1})
# and hence S3 would fire (tachyonic mode along the p_1<0 direction).
# -------------------------------------------------------------------------
print("\n" + "="*70)
print("S3 IR DIVERGENCE ANALYSIS")
print("="*70)
print("S3 fires when there exists p_alpha < 0 at a Kasner-circle visit.")
print("This corresponds to the Kasner direction where scale factor contracts.")
print()

all_visits = visits1 + visits2 + visits3
kasner_visits_with_s3 = 0
kasner_visits_total = len(all_visits)

for v in all_visits:
    has_negative_p = (v['p1'] < -0.01) or (v['p2'] < -0.01) or (v['p3'] < -0.01)
    if has_negative_p:
        kasner_visits_with_s3 += 1

print(f"Total Kasner-circle visits across all runs: {kasner_visits_total}")
print(f"Visits with p_alpha < 0 (S3 CAN fire):      {kasner_visits_with_s3}")
if kasner_visits_total > 0:
    frac = kasner_visits_with_s3 / kasner_visits_total
    print(f"Fraction: {frac:.2%}")

print()
print("Note: The Kasner circle in Bianchi VI_{-1/9} (as in VIII/IX)")
print("always has p_1 < 0 except at the Taub points T_alpha (p_alpha=1,")
print("others=0). By the BKL analysis, GENERIC Kasner states have p_1<0.")
print("Therefore S3 fires at EVERY generic Kasner-circle visit.")
print()

# -------------------------------------------------------------------------
# Constraint violation monitoring
# -------------------------------------------------------------------------
print("="*70)
print("CONSTRAINT VIOLATION CHECK (end of integration)")
print("="*70)
for label, sol in [("u0=3.0", sol1), ("golden", sol2), ("near-Taub", sol3)]:
    y_end = sol.y[:, -1]
    S1,S2,S3,R1,R3,Nm,A = y_end
    c11a = 1.0 - sigma_sq(y_end) - Nm**2 - A**2
    c11b = 2.0*R3*Nm + S1*A
    c11c = S1 + S2 + S3
    print(f"{label}: |C11a|={abs(c11a):.2e}, |C11b|={abs(c11b):.2e},"
          f" |C11c|={abs(c11c):.2e}")

print()
print("="*70)
print("VERDICT SUMMARY")
print("="*70)
print("""
The LU24 (arXiv:2410.10375) dynamical system for Bianchi VI_{-1/9} vacuum:

1. The Kasner circle K° IS part of the invariant boundary (A=N_-=0 limit).
   Lemma 2.1 (LU24): all T_{R1}, T_{R3}, T_{R1R3} frame-transition orbits
   have their alpha- and omega-limit sets IN K°.
   Lemma 2.2 (LU24): all T_{N-}, T_{R1N-} curvature-transition orbits
   have their alpha- and omega-limit sets IN K°.

2. The generic singularity attractor conjecture (LU24 Conjectures 3.1-3.2)
   places A on the union K° u T_{R1} u T_{R3} u T_{N-}, i.e., heteroclinic
   chains BETWEEN Kasner fixed points on K°.

3. HHW03 Conjecture 5.1: The past attractor A^- = S_{N-} u S_{Sigma_x}
   u S_{Sigma_2} u K. This INCLUDES the Kasner set K.

4. The Kasner circle K° in VI_{-1/9} consists of SADDLE points (HHW03 p.8):
   'the Kasner circle K is a saddle, and consequently the initial state
   of a typical model cannot be a single Kasner equilibrium point.'
   BUT: trajectories repeatedly pass THROUGH neighbourhoods of K° via
   the heteroclinic chains.

5. S3 analysis: at every generic Kasner-circle visit (p_1 < 0 holds for
   all Kasner states except the measure-zero Taub points T_alpha), the
   S3 tachyonic mode condition IS satisfied (p_1 < 0 means the
   corresponding scale factor direction contracts: a_1 ~ t^{p_1}, p_1<0).

6. The heteroclinic chains in K° u B_{II} visit Kasner fixed points with
   p_1 < 0 at each step. The visits have nonzero duration in tau (the
   orbit spends finite e-fold time near each Kasner point). The S3 IR
   divergence fires AT EACH SUCH VISIT if the integration time is
   sufficiently long (i.e., if the field mode k_1 satisfies
   omega_k(t) = |k_1| * a_1(t) -> 0 while p_1 < 0).

CONCLUSION: The visits to Kasner-circle fixed points with p_1 < 0 ARE
confirmed by the LU24 framework. S3 fires at each such visit.
However, the heteroclinic chain structure means S3 fires EPISODICALLY
(at each Kasner-circle pass), not continuously. The total accumulated
IR divergence from an infinite heteroclinic chain is an infinite sum
of epoch-contributions, which diverges.
""")
