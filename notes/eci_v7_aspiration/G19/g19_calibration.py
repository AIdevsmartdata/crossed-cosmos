"""
G1.9 CALIBRATION ANALYSIS

Identify which part of the 2-loop beta functions is causing the
discrepancy with Wang-Zhang table values.

Strategy:
1. Run with 2-loop gauge only (no 2-loop Yukawa) → check y_t at GUT
2. Run with different Yukawa 2-loop coefficients → find which matches WZ
3. Verify the sign/magnitude of the dominant g_3^2 y_t^2 term

Key question: WZ gives y_t(M_GUT) = 0.4454 at 2-loop with PDG 2024 ICs.
Our code gives 0.4128 → too low by ~7%.

If 1-loop (WZ ICs at M_Z) would give some value, and 2-loop gives less,
we need to check the sign of the 2-loop correction.

KNOWN RESULT: 2-loop makes y_t run FASTER (to lower values) — but by how much?
  WZ: 1-loop y_t at GUT ~ 0.44 (from our code), 2-loop y_t ~ 0.4454 (WZ)
  So WZ 2-loop y_t is HIGHER than our 1-loop → our 2-loop y_t is too LOW.

This means our 2-loop Yukawa beta function is too negative (overcorrecting downward).

The main culprit: the term +20 g_3^2 y_t^2 in A_t^(2).
This term is POSITIVE in A_t^(2), meaning it INCREASES the rate of change of y_t.
At high scale where we run upward, MORE positive A_t means y_t changes FASTER.

But wait: in 1-loop, the dominant term is -8 g_3^2 < 0 (gauge suppression).
So the 1-loop beta is NEGATIVE → y_t decreases as mu increases (upward).
The 2-loop correction +20 g_3^2 y_t^2 should REDUCE this suppression.

Let me check: in the 2-loop code, the sign convention:
  A_t^(2) adds to A_t^(1) with factor 1/(16pi^2).
  A_t^(1) ≈ -(8 g_3^2) y_t [dominant gauge]
  A_t^(2) = +20 g_3^2 y_t^2 + gauge^4 terms

  So the 2-loop correction to dy_t/dt is:
    +y_t × (1/16pi^2) × (+20 g_3^2 y_t^2)
  = +(20/16pi^2) g_3^2 y_t^3 > 0

  This is POSITIVE, meaning dy_t/dt is LESS NEGATIVE at 2-loop.
  → y_t runs SLOWER (stays HIGHER) at high scale.
  → y_t(M_GUT) should be HIGHER at 2-loop than 1-loop.

BUT our result shows 2-loop gives y_t(M_GUT) = 0.4178 LOWER than 1-loop 0.4430!
This means the GAUGE 2-loop is the dominant issue, not Yukawa.

The gauge 2-loop (B matrix) makes g_3 run FASTER downward:
  beta_g3_2 includes B33 × g_3^5 with B33 = -26 → strongly negative
  This makes g_3 decrease more rapidly → at high scale g_3 is LOWER.

But wait: B33 = -26 means the 2-loop correction to g_3 is MORE NEGATIVE.
  16pi^2 dg_3/dt = -7 g_3^3 + (1/16pi^2) × (-26 g_3^5 + ...) g_3
  The 2-loop term with -26 g_3^5 means g_3 is additionally SUPPRESSED.
  → g_3 at GUT scale is LOWER in 2-loop than 1-loop.

Now, g_3 suppresses y_t running. Less g_3 → less suppression → y_t stays higher?
But if g_3 DECREASES faster, then at intermediate scales there's LESS g_3,
meaning LESS suppression of y_t, meaning y_t stays HIGHER at GUT.

This would explain why WZ 2-loop y_t(GUT) ≈ 0.4454 is HIGHER than our 1-loop.

But our code gives 2-loop LOWER. Something is wrong with our B33.

The issue: B33 = -26 should be NEGATIVE (this is the 2-loop gauge self-coupling).
In the context of the BETA FUNCTION for g_3:
  If B33 < 0, the 2-loop correction is MORE NEGATIVE → g_3 decreases faster at low energy.
  But we're running UP from m_t to M_GUT.

Let me recalculate this more carefully.

Wait - I need to re-examine the B matrix convention.
The MV formula gives:
  16pi^2 dg_i/dt = b_i g_i^3 + (1/16pi^2) [B_{ij}] g_j^2 g_i^3

For g_3 with B33 = -26:
  The 2-loop term: (1/16pi^2) × (-26) × g_3^5

If g_3 ~ 1 at low scales and decreases to ~0.53 at GUT:
  At low scale: (1/16pi^2) × (-26) × g_3^5 ≈ (1/158) × (-26) × 1 ≈ -0.165
  This makes the beta function MORE NEGATIVE → g_3 goes LOWER than 1-loop.

But the 2-loop effect on y_t through gauge:
  In the 1-loop y_t beta: A_t^(1) = ... -8 g_3^2 ...
  If 2-loop makes g_3 smaller, then -8 g_3^2 is LESS NEGATIVE.
  This means A_t^(1) is LESS NEGATIVE at 2-loop (g_3 running).
  → y_t should indeed go HIGHER at 2-loop through this mechanism.

So the problem is: why is our code giving y_t LOWER at 2-loop?

Diagnosis: We need to separate the effects.
Let me run:
1. 1-loop everything
2. 2-loop gauge only (no 2-loop Yukawa)
3. 2-loop gauge + 2-loop Yukawa
"""

import numpy as np
from scipy.integrate import solve_ivp

MZ = 91.1876
MT_MSBAR = 163.5
M_GUT = 2e16
v_EW = 246.22 / np.sqrt(2)

g1_MZ = 0.461228
g2_MZ = 0.65096
g3_MZ = 1.2123

# WZ Table 2 initial values at M_Z
WZ_yt_MZ = 0.967
WZ_yc_MZ = 3.56e-3

# 1-loop gauge beta coefficients (SM, Nf=6 above m_t)
b1 = 41.0/10.0
b2 = -19.0/6.0
b3 = -7.0

# 2-loop B matrix (Arason et al. 1992) - need to verify!
# The standard SM result:
B11 = 199.0/50.0;   B12 = 27.0/10.0;   B13 = 44.0/5.0
B21 = 9.0/10.0;     B22 = 35.0/6.0;    B23 = 12.0
B31 = 11.0/10.0;    B32 = 9.0/2.0;     B33 = -26.0

def make_rge(use_2loop_gauge=True, use_2loop_yukawa=True, which_yukawa2=None):
    """
    which_yukawa2: None (use all), 'gauge4_only', 'cross_only', 'yukawa4_only'
    """
    def rge(t, y):
        g1, g2, g3, yt, yc = y
        g1 = max(g1, 0.01); g2 = max(g2, 0.01); g3 = max(g3, 0.01)
        yt = max(yt, 1e-10); yc = max(yc, 1e-15)

        g1sq = g1**2; g2sq = g2**2; g3sq = g3**2; ytsq = yt**2

        loop1 = 1.0 / (16.0 * np.pi**2)
        loop2 = loop1**2

        # Gauge 1-loop
        bg1_1 = b1 * g1sq * g1
        bg2_1 = b2 * g2sq * g2
        bg3_1 = b3 * g3sq * g3

        # Gauge 2-loop
        if use_2loop_gauge:
            Br1 = B11*g1sq + B12*g2sq + B13*g3sq
            Br2 = B21*g1sq + B22*g2sq + B23*g3sq
            Br3 = B31*g1sq + B32*g2sq + B33*g3sq
            # Yukawa corrections to gauge 2-loop (from Arason 1992):
            # Note: these should ADD to the beta function for g_i
            # The conventional sign: +C_i * y_t^2 * g_i^3 in 16pi^2 dg_i/dt
            # From Arason et al. 1992 Table AI:
            # For g_1: Yukawa contribution = -(17/10) y_t^2 g_1 [wait: is this + or -?]
            # The Yukawa contribution is POSITIVE (Yukawa increases gauge running):
            # 16pi^2 dg_i/dt = b_i g_i^3 + (1/16pi^2)[B_ij g_j^2 g_i^3 + Y_i g_i y_t^2]
            # where Y_i are POSITIVE:
            # Y_1 = 17/10 (Yukawa makes g_1 run faster = positive contribution)
            # Y_2 = 3/2
            # Y_3 = 2
            # These make gauge couplings run FASTER at 2-loop due to top quark.
            Y1 = 17.0/10.0  # NOT negative!
            Y2 = 3.0/2.0
            Y3 = 2.0
            bg1_2 = (Br1 * g1sq + Y1 * ytsq) * g1
            bg2_2 = (Br2 * g2sq + Y2 * ytsq) * g2
            bg3_2 = (Br3 * g3sq + Y3 * ytsq) * g3
        else:
            bg1_2 = bg2_2 = bg3_2 = 0.0

        dg1 = loop1 * bg1_1 + loop2 * bg1_2
        dg2 = loop1 * bg2_1 + loop2 * bg2_2
        dg3 = loop1 * bg3_1 + loop2 * bg3_2

        # Yukawa 1-loop
        G_up = (17.0/20.0)*g1sq + (9.0/4.0)*g2sq + 8.0*g3sq
        At1 = -G_up + (9.0/2.0)*ytsq
        Ac1 = -G_up + 3.0*ytsq

        # Yukawa 2-loop
        if use_2loop_yukawa:
            # From Arason et al. 1992, Eq. A.6:
            # beta_t^(2) / y_t = gauge^4 terms + Yukawa*gauge^2 + Yukawa^4
            #
            # The dominant correction comes from g_3 terms.
            # The key 2-loop coefficient for g_3^2 y_t^2:
            # From the SM 2-loop Yukawa beta function (Arason 1992):
            # β_t^(2)/y_t = -3/2 y_t^4  [pure Yukawa]
            #   + y_t^2 × [ (17/10)g_1^2 + (9/2)g_2^2 + 20 g_3^2 ]   [cross terms]
            #   + [ gauge^4 terms ]

            gauge4 = (+(1187.0/600.0) * g1sq**2
                      - (9.0/20.0) * g1sq * g2sq
                      - (23.0/4.0) * g2sq**2
                      + (19.0/15.0) * g1sq * g3sq
                      + 9.0 * g2sq * g3sq
                      - 108.0 * g3sq**2)

            cross = ytsq * ((17.0/10.0)*g1sq + (9.0/2.0)*g2sq + 20.0*g3sq)

            yukawa4 = -(9.0/4.0) * ytsq**2

            if which_yukawa2 == 'gauge4_only':
                At2 = gauge4
            elif which_yukawa2 == 'cross_only':
                At2 = cross
            elif which_yukawa2 == 'yukawa4_only':
                At2 = yukawa4
            else:
                At2 = gauge4 + cross + yukawa4

            Ac2 = gauge4 + cross + yukawa4  # Same for y_c
        else:
            At2 = Ac2 = 0.0

        dyt = loop1 * yt * At1 + loop2 * yt * At2
        dyc = loop1 * yc * Ac1 + loop2 * yc * Ac2

        return [dg1, dg2, dg3, dyt, dyc]
    return rge


def run(mu1, mu2, y0, rge_fn, rtol=1e-12):
    t1 = np.log(mu1/MZ)
    t2 = np.log(mu2/MZ)
    sol = solve_ivp(rge_fn, [t1, t2], y0, method='RK45', rtol=rtol, atol=1e-14,
                    max_step=0.5, dense_output=False)
    if not sol.success:
        raise RuntimeError(f"Failed: {sol.message}")
    return sol.y[:, -1]


# Initial conditions at M_Z (WZ Table 2)
y_init = [g1_MZ, g2_MZ, g3_MZ, WZ_yt_MZ, WZ_yc_MZ]
yt_mt = MT_MSBAR / v_EW  # EW BC

print("=" * 70)
print("CALIBRATION: Diagnose 2-loop discrepancy")
print("=" * 70)
print()
print(f"WZ Table 2 targets at M_GUT: y_t = 0.4454, g_3 = 0.5310")
print()

# Test 1: 1-loop gauge + 1-loop Yukawa
y_GUT_1L = run(MZ, M_GUT, y_init, make_rge(False, False))
print(f"1-loop gauge + 1-loop Yukawa: y_t(GUT) = {y_GUT_1L[3]:.4f}, g3 = {y_GUT_1L[2]:.4f}")

# Test 2: 2-loop gauge + 1-loop Yukawa
y_GUT_2Lg1Y = run(MZ, M_GUT, y_init, make_rge(True, False))
print(f"2-loop gauge + 1-loop Yukawa: y_t(GUT) = {y_GUT_2Lg1Y[3]:.4f}, g3 = {y_GUT_2Lg1Y[2]:.4f}")

# Test 3: 2-loop gauge + 2-loop Yukawa (all terms)
y_GUT_2L = run(MZ, M_GUT, y_init, make_rge(True, True))
print(f"2-loop gauge + 2-loop Yukawa: y_t(GUT) = {y_GUT_2L[3]:.4f}, g3 = {y_GUT_2L[2]:.4f}")

# Test 4: 2-loop gauge + 2-loop Yukawa (cross only)
y_GUT_cross = run(MZ, M_GUT, y_init, make_rge(True, True, 'cross_only'))
print(f"2-loop gauge + cross-only Y2: y_t(GUT) = {y_GUT_cross[3]:.4f}, g3 = {y_GUT_cross[2]:.4f}")

# Test 5: 2-loop gauge + 2-loop Yukawa (gauge4 only)
y_GUT_g4 = run(MZ, M_GUT, y_init, make_rge(True, True, 'gauge4_only'))
print(f"2-loop gauge + gauge4-only Y2: y_t(GUT) = {y_GUT_g4[3]:.4f}, g3 = {y_GUT_g4[2]:.4f}")

print()
print("WZ target: y_t(M_GUT) = 0.4454")
print()

# Compare with signs FLIPPED on Yukawa 2-loop
# Maybe the sign convention is opposite?
def rge_flipped_yukawa2(t, y):
    g1, g2, g3, yt, yc = y
    g1 = max(g1, 0.01); g2 = max(g2, 0.01); g3 = max(g3, 0.01)
    yt = max(yt, 1e-10); yc = max(yc, 1e-15)
    g1sq = g1**2; g2sq = g2**2; g3sq = g3**2; ytsq = yt**2
    loop1 = 1.0 / (16.0 * np.pi**2)
    loop2 = loop1**2

    bg1_1 = b1 * g1sq * g1
    bg2_1 = b2 * g2sq * g2
    bg3_1 = b3 * g3sq * g3

    Br1 = B11*g1sq + B12*g2sq + B13*g3sq
    Br2 = B21*g1sq + B22*g2sq + B23*g3sq
    Br3 = B31*g1sq + B32*g2sq + B33*g3sq
    Y1 = 17.0/10.0; Y2 = 3.0/2.0; Y3 = 2.0
    bg1_2 = (Br1 * g1sq + Y1 * ytsq) * g1
    bg2_2 = (Br2 * g2sq + Y2 * ytsq) * g2
    bg3_2 = (Br3 * g3sq + Y3 * ytsq) * g3

    dg1 = loop1 * bg1_1 + loop2 * bg1_2
    dg2 = loop1 * bg2_1 + loop2 * bg2_2
    dg3 = loop1 * bg3_1 + loop2 * bg3_2

    G_up = (17.0/20.0)*g1sq + (9.0/4.0)*g2sq + 8.0*g3sq
    At1 = -G_up + (9.0/2.0)*ytsq

    # Use NEGATIVE of the Yukawa^2*gauge^2 cross terms
    # (opposite sign to what we had before)
    cross = -ytsq * ((17.0/10.0)*g1sq + (9.0/2.0)*g2sq + 20.0*g3sq)
    gauge4 = (+(1187.0/600.0) * g1sq**2 - (9.0/20.0) * g1sq * g2sq
              - (23.0/4.0) * g2sq**2 + (19.0/15.0) * g1sq * g3sq
              + 9.0 * g2sq * g3sq - 108.0 * g3sq**2)
    yukawa4 = -(9.0/4.0) * ytsq**2
    At2 = gauge4 + cross + yukawa4

    G_up_c = G_up
    Ac1 = -G_up_c + 3.0*ytsq
    Ac2 = gauge4 + cross + yukawa4

    dyt = loop1 * yt * At1 + loop2 * yt * At2
    dyc = loop1 * yc * Ac1 + loop2 * yc * Ac2

    return [dg1, dg2, dg3, dyt, dyc]

y_GUT_flip = run(MZ, M_GUT, y_init, rge_flipped_yukawa2)
print(f"2-loop gauge + FLIPPED cross Y2: y_t(GUT) = {y_GUT_flip[3]:.4f}, g3 = {y_GUT_flip[2]:.4f}")

print()

# Key check: what is the magnitude and sign of each 2-loop Yukawa contribution at m_t scale?
# At mu = m_t: g3 ~ 1.16, yt ~ 0.94
g3_mt_val = 1.1673  # from the code output above
yt_mt_val = 0.9391
g1_mt_val = 0.4628
g2_mt_val = 0.6479

print("=" * 50)
print("2-loop Yukawa beta function terms at mu = m_t:")
print(f"  g1={g1_mt_val:.4f}, g2={g2_mt_val:.4f}, g3={g3_mt_val:.4f}, yt={yt_mt_val:.4f}")
g3sq = g3_mt_val**2
g1sq = g1_mt_val**2
g2sq = g2_mt_val**2
ytsq = yt_mt_val**2

gauge4_mt = (+(1187.0/600.0)*g1sq**2 - (9.0/20.0)*g1sq*g2sq
             - (23.0/4.0)*g2sq**2 + (19.0/15.0)*g1sq*g3sq
             + 9.0*g2sq*g3sq - 108.0*g3sq**2)
cross_mt = ytsq * ((17.0/10.0)*g1sq + (9.0/2.0)*g2sq + 20.0*g3sq)
yukawa4_mt = -(9.0/4.0)*ytsq**2

At1_mt = -(17.0/20.0)*g1sq - (9.0/4.0)*g2sq - 8.0*g3sq + (9.0/2.0)*ytsq

print(f"  1-loop A_t^(1) = {At1_mt:.4f}")
print(f"  2-loop gauge^4 term = {gauge4_mt:.4f}")
print(f"  2-loop cross term (+20 g3^2 y_t^2) = {cross_mt:.4f}")
print(f"  2-loop yukawa^4 = {yukawa4_mt:.4f}")
print(f"  Total 2-loop At^(2) = {gauge4_mt+cross_mt+yukawa4_mt:.4f}")
loop1 = 1.0/(16*np.pi**2)
print(f"  Relative 2-loop correction: At^(2)/(16pi^2 × At^(1)) = {(gauge4_mt+cross_mt+yukawa4_mt)*loop1/At1_mt:.4f}")
print()
print(f"  DOMINANT: -108 g3^4 = {-108*g3sq**2:.4f} (strongly negative gauge4)")
print(f"  COMPETING: +20 g3^2 y_t^2 = {20*g3sq*ytsq:.4f} (cross, positive)")
print(f"  NET at m_t: gauge4 dominates with {gauge4_mt:.4f}")

print()
print("=" * 50)
print("At GUT scale (g3 ~ 0.53, yt ~ 0.44):")
g3_GUT = 0.5310; g1_GUT = 0.5752; g2_GUT = 0.5230; yt_GUT = 0.4454
g3sq_GUT = g3_GUT**2; g1sq_GUT = g1_GUT**2; g2sq_GUT = g2_GUT**2; ytsq_GUT = yt_GUT**2
gauge4_GUT = (+(1187.0/600.0)*g1sq_GUT**2 - (9.0/20.0)*g1sq_GUT*g2sq_GUT
              - (23.0/4.0)*g2sq_GUT**2 + (19.0/15.0)*g1sq_GUT*g3sq_GUT
              + 9.0*g2sq_GUT*g3sq_GUT - 108.0*g3sq_GUT**2)
cross_GUT = ytsq_GUT * ((17.0/10.0)*g1sq_GUT + (9.0/2.0)*g2sq_GUT + 20.0*g3sq_GUT)
yukawa4_GUT = -(9.0/4.0)*ytsq_GUT**2
At1_GUT = -(17.0/20.0)*g1sq_GUT - (9.0/4.0)*g2sq_GUT - 8.0*g3sq_GUT + (9.0/2.0)*ytsq_GUT

print(f"  1-loop A_t^(1) = {At1_GUT:.4f}")
print(f"  2-loop gauge^4 = {gauge4_GUT:.4f}")
print(f"  2-loop cross   = {cross_GUT:.4f}")
print(f"  2-loop yukawa4 = {yukawa4_GUT:.4f}")
print(f"  At^(2) total   = {gauge4_GUT+cross_GUT+yukawa4_GUT:.4f}")
