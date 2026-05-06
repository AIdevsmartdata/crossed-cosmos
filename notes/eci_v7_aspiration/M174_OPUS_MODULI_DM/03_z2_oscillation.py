#!/usr/bin/env python3
"""
M174 sub-task 3 -- Z_2 class-group oscillation between tau_a = i*sqrt(22) and
tau_b = i*sqrt(11/2) for K = Q(sqrt(-22)), h = 2.

Setup (from M155):
- W^Q_double = H_{-88}(j(tau))^2 / eta(tau)^12 vanishes at BOTH class reps
- V_F(tau_a) = V_F(tau_b) = 0 (both Minkowski SUSY)
- Hessian ratio: m^2(tau_a) / m^2(tau_b) = 2.49e31  (asymmetric!)
- Class-group action [p_2]: tau_a -> tau_b realized by M_11 = [[0,-11],[1,0]] (det=11)

Question: does Z_2 oscillation between {tau_a, tau_b} contribute Omega_DM h^2 ~ 0.12?

Key physics:
1. The two class reps are DEGENERATE in V_F (both = 0) but not in m^2.
2. A Z_2 mod field theory has an Ising-like double-well potential, where each
   well is V_F(tau_*) = 0 but oscillation between wells has energy.
3. Energy stored in misalignment from one well's center.

But here the wells are CONNECTED by a finite-Im-tau path (not the usual Z_2 mod
in canonical field theory). The transition tau_a -> tau_b is a DISCRETE class
group action, not a continuous oscillation.

INTERPRETATION: in Galois/Hecke-correspondence language, the modulus tau lives
on the orbifold M = upper half plane / GL_2^+(Q)_class-group. The two class reps
are RELATED POINTS in moduli space, not two separate physical configurations.

So 'oscillation' between them is NOT a sinusoidal coherent oscillation around
a single vacuum. It's a discrete tunneling between two degenerate vacua in a
double-well potential.

Question: what's the tunneling rate? What energy density is stored?

ANSWER:
1. Tunneling rate: Gamma ~ A * exp(-S_E) where S_E is the Euclidean action
   between vacua.
2. Energy density: oscillation amplitude * mass^2 / 2 in canonical field.

Let's quantify.

From M155: in canonical Kahler-norm coords, the "distance" between tau_a and
tau_b is:
    delta tau = tau_a - tau_b = i (sqrt(22) - sqrt(11/2)) = i * sqrt(11/2) * (sqrt(2) - 1)/sqrt(2)
              = i * 2.3452..  approximately

Or in the appropriate canonical frame at midpoint: not well-defined since
G_TT* depends on Im tau. Use approximate average G_TT* ~ 3/(Im(tau_a)+Im(tau_b))^2.

Energy density:
   rho_DM = (1/2) m^2 |phi|^2  where phi is canonically-normalized modulus field
                                (departure from vacuum).

For Omega_DM h^2 = 0.12:
   rho_DM (today) = 0.12 * 3 H_0^2 M_Pl^2 / h^2 = critical_density * Omega_DM
                  ~ 1.0e-47 GeV^4    (Planck 2018 cosmology)

If oscillation amplitude is phi_*, then today's rho_DM (after redshift):
   rho_today = (a_osc/a_today)^3 * rho_osc      (CDM-like dilution)
   rho_osc   = (1/2) m^2 phi_*^2  evaluated at oscillation onset (H ~ m)

Standard misalignment:
   phi_* ~ Lambda_W (moduli VEV scale)
   onset H_osc = m_tau
   T_osc satisfies H = m: T_osc ~ sqrt(m * M_Pl)  (radiation era)
        or M_Pl * sqrt(m/M_Pl)
   a_osc/a_today = (T_today/T_osc)
"""

import mpmath as mp

mp.mp.dps = 30

print("="*70)
print("M174 sub-task 3 -- Z_2 class-group oscillation")
print("="*70)

# Constants
M_Pl_GeV = mp.mpf("2.435e18")
T_today_GeV = mp.mpf("2.348e-13")    # T_CMB ~ 2.725 K = 2.35e-4 eV
g_star = mp.mpf("3.36")              # effective DOF today (gamma + neutrinos)
g_star_osc_default = mp.mpf("106.75")  # full SM at high T
H0_GeV = mp.mpf("1.4e-42")           # h = 0.674 -> H_0 = 67.4 km/s/Mpc
rho_crit = 3 * H0_GeV**2 * M_Pl_GeV**2  # in GeV^4
rho_DM = mp.mpf("0.12") * rho_crit / mp.mpf("0.674")**2 * mp.mpf("0.315")  # Omega_DM ~ 0.265
# More directly: Omega_DM h^2 = 0.12, so rho_DM h^2 = 0.12 * rho_crit_h
# rho_crit (h=1) = 1.05e-5 (h)^2 GeV/cm^3 = ...
# Use known: rho_DM today ~ 1.26e-6 GeV/cm^3 = 1.26e-6 * (1.97e-14 cm)^{-3} GeV
# 1 cm^{-1} in GeV: 1 cm = 5.07e13 GeV^{-1}, so 1 cm^{-3} = 1.30e-41 GeV^3
# rho_DM = 1.26e-6 GeV/cm^3 = 1.26e-6 * 1.30e-41 GeV^4 = 1.64e-47 GeV^4
rho_DM_GeV4 = mp.mpf("1.6e-47")

print(f"\nrho_DM (today, GeV^4) = {rho_DM_GeV4}")
print(f"M_Pl = {M_Pl_GeV} GeV")
print(f"T_today = {T_today_GeV} GeV")
print(f"H_0 = {H0_GeV} GeV")
print()

# CM points
sqrt22 = mp.sqrt(22)
sqrt_11_2 = mp.sqrt(mp.mpf(11)/2)
tau_a = mp.mpc(0, sqrt22)
tau_b = mp.mpc(0, sqrt_11_2)
print(f"tau_a = i*sqrt(22)    = i*{sqrt22}")
print(f"tau_b = i*sqrt(11/2)  = i*{sqrt_11_2}")
print(f"|tau_a - tau_b| = {abs(tau_a - tau_b)} (in tau coords)")
print()

# Canonical field difference: integrate phi = sqrt(3)/(2 Im tau) d tau
# from tau_b (Im=sqrt(11/2)) to tau_a (Im=sqrt(22))
# phi_a - phi_b = sqrt(3)/2 * integral (1/y) dy from y_b to y_a
#               = sqrt(3)/2 * log(y_a/y_b) = sqrt(3)/2 * log(sqrt(22)/sqrt(11/2))
#               = sqrt(3)/2 * log(sqrt(2*2)) = sqrt(3)/2 * log(2)
sqrt3 = mp.sqrt(3)
delta_phi = sqrt3/2 * mp.log(sqrt22 / sqrt_11_2)
print(f"Canonical field separation in M_Pl units:")
print(f"  delta_phi = sqrt(3)/2 * log(y_a/y_b) = {delta_phi} M_Pl")
print(f"           = {sqrt3/2 * mp.log(2)} M_Pl  (since sqrt(22)/sqrt(11/2)=2)")
print()

# This is O(1) in Planck units! Trans-Planckian oscillation amplitude.
print(f"=== KEY OBSERVATION ===")
print(f"Canonical separation between class reps is delta_phi = {sqrt3/2 * mp.log(2)} M_Pl")
print(f"This is sub-Planckian (O(0.6) M_Pl), within EFT validity.")
print()

# Now: what oscillation pattern? Two scenarios:

# (A) DOUBLE-WELL Z_2 instanton tunneling
# Action between vacua: S_E ~ (delta phi)^2 * m_tau / (something)
# More carefully, for double-well V(phi) = lambda (phi^2 - v^2)^2 with
# vacua at +-v, the tunneling action is S_E = 2 sqrt(2)/3 * v * sqrt(2 lambda) * v^2
#                                            = 4/3 * m * v / lambda  (where m^2 = 8 lambda v^2)
# In our case the "well" structure is non-perturbative; rough estimate:
# S_E ~ 2 m_tau (delta phi) / (small numerical)

# (B) COHERENT MISALIGNMENT around average vacuum
# Energy density rho ~ (1/2) m^2 phi_*^2 with phi_* ~ misalignment

# Let's pick a target Lambda_W and compute oscillation freq.
# For DM, m_tau is the oscillation frequency.

# Compute oscillation parameters for each candidate window
print("="*70)
print("OSCILLATION FREQUENCY AND ENERGY DENSITY")
print("="*70)
print()
print(f"For W^Q^double (M155 quark sector), |W''(tau_b)| ~ 3.12e43 in M_Pl=1, dimless f.")
print(f"After EFT rescaling W = Lambda_W^3 * f:")
print(f"  m_tau^2(tau_b) = (4/9) |Lambda_W^3 W''_dimless|^2 / M_Pl^4")
print()

# For tau_b: m_tau (natural) ^2 ~ 2.49e84 (M155 Table 4)
# Note: this is in M_Pl=1 with W normalized as f
m_tau_b_natural_sq = mp.mpf("2.457e84")
m_tau_b_natural = mp.sqrt(m_tau_b_natural_sq)
print(f"m_tau(tau_b) natural sqrt = {mp.nstr(m_tau_b_natural, 6)} (M_Pl=1)")
print()

# Lambda_W to bring this to physical mass
def lambda_W_for_quark_modulus(m_target_GeV, m_natural=m_tau_b_natural):
    L3 = m_target_GeV * M_Pl_GeV**2 / m_natural
    return L3**(mp.mpf(1)/3)

# Same windows
print(f"{'Target m':<14} {'Lambda_W (GeV) for tau_b':<25} {'Lambda_W/M_Pl':<14}")
print("-"*70)
for name, m in [("WIMP 100 GeV", mp.mpf("1e2")),
                 ("Axion 1e-5 eV", mp.mpf("1e-14")),
                 ("Fuzzy 1e-22 eV", mp.mpf("1e-31"))]:
    LW = lambda_W_for_quark_modulus(m)
    print(f"{name:<14} {mp.nstr(LW, 6):<25} {mp.nstr(LW/M_Pl_GeV, 4):<14}")

print()
print("="*70)
print("Z_2 OSCILLATION ENERGY DENSITY (MISALIGNMENT)")
print("="*70)

# Misalignment: oscillation around tau_b with amplitude up to delta_phi (= sqrt(3)/2 log 2 M_Pl)
# rho_osc = (1/2) m^2 phi_*^2 evaluated at H = m_tau (oscillation onset)
# For radiation era: H = sqrt(g_star * pi^2/30 / 3) T^2 / M_Pl ~ T^2 / M_Pl

# Onset: T_osc such that H(T_osc) = m_tau
# H = sqrt(pi^2 g_star / 90) T^2 / M_Pl
# T_osc^2 = m_tau * M_Pl / sqrt(pi^2 g_star/90)
# Approximate: T_osc ~ sqrt(m_tau * M_Pl)

def T_osc(m_GeV, gstar=g_star_osc_default):
    # H = pi sqrt(g*/90) T^2 / M_Pl, set = m
    return (m_GeV * M_Pl_GeV / (mp.pi * mp.sqrt(gstar/90)))**mp.mpf("0.5")

def rho_osc_GeV4(m_GeV, phi_star_MPl):
    # rho = (1/2) m^2 (phi_* * M_Pl)^2 in GeV^4
    return mp.mpf("0.5") * m_GeV**2 * (phi_star_MPl * M_Pl_GeV)**2

def Omega_misalignment(m_GeV, phi_star_MPl, gstar=g_star_osc_default):
    """
    Standard misalignment formula:
    Omega h^2 = (m_tau / 5e-2 eV) * (phi_*/M_Pl)^2 * 0.6  (very rough)
    More precisely from energy conservation:
        rho_osc(t_osc) = (1/2) m^2 phi_*^2, redshifts as a^{-3} matter-like.
        rho_today / rho_osc = (a_osc/a_today)^3 = (T_today/T_osc)^3 * (g_*s,today/g_*s,osc)
    """
    Tosc = T_osc(m_GeV, gstar)
    rho_osc_init = rho_osc_GeV4(m_GeV, phi_star_MPl)
    g_today_s = mp.mpf("3.94")
    redshift_factor = (T_today_GeV / Tosc)**3 * (g_today_s / gstar)
    rho_today = rho_osc_init * redshift_factor
    Omega = rho_today / rho_DM_GeV4 * mp.mpf("0.12")  # in units of Omega_DM h^2
    return Omega, Tosc, rho_today

# phi_* = delta_phi (canonical separation between class reps)
phi_star = sqrt3/2 * mp.log(2)  # ~ 0.6 M_Pl
print(f"\nUse phi_* = sqrt(3)/2 * log(2) = {phi_star} M_Pl (full Z_2 separation)")
print()

print(f"{'m_tau':<15} {'T_osc (GeV)':<14} {'rho_today':<14} {'Omega h^2':<14} {'verdict':<25}")
print("-"*100)
for name, m in [("WIMP 100 GeV", mp.mpf("1e2")),
                 ("CDM 1 GeV",    mp.mpf("1")),
                 ("CDM 1 MeV",    mp.mpf("1e-3")),
                 ("CDM 1 keV",    mp.mpf("1e-6")),
                 ("Axion 1e-5 eV",mp.mpf("1e-14")),
                 ("Fuzzy 1e-22 eV",mp.mpf("1e-31"))]:
    Omega, Tosc, rho_today = Omega_misalignment(m, phi_star)
    if Omega > mp.mpf("0.5") and Omega < mp.mpf("0.5"):
        verdict = "MATCH Omega_DM h^2"
    elif Omega > mp.mpf("1"):
        verdict = "OVERCLOSURE!"
    elif Omega > mp.mpf("1e-2"):
        verdict = "competitive DM"
    elif Omega > mp.mpf("1e-6"):
        verdict = "subdominant DM"
    else:
        verdict = "negligible"
    print(f"{name:<15} {mp.nstr(Tosc, 4):<14} {mp.nstr(rho_today, 4):<14} {mp.nstr(Omega, 4):<14} {verdict:<25}")

print()
print("="*70)
print("SOLVE: which m_tau gives exactly Omega h^2 = 0.12 with phi_* ~ 0.6 M_Pl?")
print("="*70)

# Solve Omega(m) = 1
# rho_today = (1/2) m^2 phi_*^2 * (T_today / sqrt(m * M_Pl))^3 * g_ratio
#           = (1/2) m^2 phi_*^2 * T_today^3 / (m * M_Pl)^{3/2} * g_ratio
#           = (1/2) phi_*^2 * T_today^3 * m^{1/2} / M_Pl^{3/2} * g_ratio
# Set = rho_DM:
# m^{1/2} = 2 rho_DM / (phi_*^2 T_today^3 / M_Pl^{3/2} * g_ratio)
# Need g_ratio = (g_today_s/g_osc) ~ 0.04 ; phi_* M_Pl in GeV in formula

phi_star_GeV = phi_star * M_Pl_GeV
g_today_s = mp.mpf("3.94")
g_osc = mp.mpf("106.75")
g_ratio = g_today_s / g_osc

# rho_today = (1/2) m^2 phi_*^2 * (T_today/T_osc)^3 * g_ratio
# T_osc = (m * M_Pl / (pi sqrt(g_osc/90)))^{1/2}
# T_osc^3 = (m M_Pl)^{3/2} * (pi sqrt(g_osc/90))^{-3/2}
# rho_today = (1/2) * m^2 * phi_GeV^2 * T_today^3 / (m M_Pl)^{3/2} * (pi sqrt(g_osc/90))^{3/2} * g_ratio
#           = (1/2) phi_GeV^2 T_today^3 / M_Pl^{3/2} * m^{1/2} * (pi sqrt(g_osc/90))^{3/2} * g_ratio

def Omega_h2_for_mass(m_GeV, phi_GeV=phi_star_GeV):
    Tosc = T_osc(m_GeV, g_osc)
    rho_init = mp.mpf("0.5") * m_GeV**2 * phi_GeV**2
    rho_today = rho_init * (T_today_GeV/Tosc)**3 * g_ratio
    # Omega h^2 = rho_today / rho_crit_h ; rho_crit/h^2 = 1.05e-5 * h^2 GeV/cm^3 / h^2
    # rho_DM_GeV4 corresponds to Omega_DM=0.265 with h=0.674
    # Omega_DM h^2 = 0.12. So Omega h^2 (modulus) = (rho_today / rho_DM_GeV4) * 0.12
    return rho_today / rho_DM_GeV4 * mp.mpf("0.12")

# Solve: find m such that Omega = 0.12
# Using: Omega = const * sqrt(m)
# const = (1/2) * phi^2 * T_today^3 * (pi sqrt(g_osc/90))^{3/2} / (M_Pl^{3/2} * rho_DM_GeV4) * 0.12 * g_ratio
const_factor = (mp.mpf("0.5") * phi_star_GeV**2 * T_today_GeV**3
                * (mp.pi * mp.sqrt(g_osc/90))**(mp.mpf(3)/2)
                / (M_Pl_GeV**(mp.mpf(3)/2) * rho_DM_GeV4)
                * mp.mpf("0.12") * g_ratio)
print(f"\nOmega h^2 = const * m^{{1/2}}, const = {const_factor}")
print(f"Setting Omega = 0.12: m_solve = (0.12/const)^2 = {(mp.mpf('0.12')/const_factor)**2} GeV")
m_solve = (mp.mpf("0.12")/const_factor)**2
print(f"m_solve = {mp.nstr(m_solve, 6)} GeV = {mp.nstr(m_solve/mp.mpf('1e-9'), 6)} eV")
print()

# Sanity check
omega_check = Omega_h2_for_mass(m_solve)
print(f"Sanity check Omega h^2 (m_solve) = {mp.nstr(omega_check, 6)}")
print()

# Convert to Lambda_W via m = m_natural * Lambda_W^3 / M_Pl^2
# For tau_L = i (M134): m_natural = 1.61e5
# For tau_b (M155 quark): m_natural ~ sqrt(2.46e84) = 1.57e42
print("Lambda_W needed for this Omega-saturating mass:")
m_nat_L = mp.mpf("161042.6")
m_nat_Q = mp.sqrt(mp.mpf("2.457e84"))
LW_L = (m_solve * M_Pl_GeV**2 / m_nat_L)**(mp.mpf(1)/3)
LW_Q = (m_solve * M_Pl_GeV**2 / m_nat_Q)**(mp.mpf(1)/3)
print(f"  Lepton modulus tau_L=i:    Lambda_W = {mp.nstr(LW_L, 4)} GeV  (= {mp.nstr(LW_L/M_Pl_GeV, 4)} M_Pl)")
print(f"  Quark modulus tau_b:       Lambda_W = {mp.nstr(LW_Q, 4)} GeV  (= {mp.nstr(LW_Q/M_Pl_GeV, 4)} M_Pl)")
print()

print("="*70)
print("Z_2 TUNNELING (instanton) RATE BETWEEN tau_a AND tau_b")
print("="*70)
# Estimate: between two SUSY-Minkowski vacua connected by classical path,
# tunneling rate ~ exp(-S_E)
# S_E ~ integral of L_E along path; for canonical phi field with mass m:
# S_E ~ (delta_phi)^2 * m_tau   (in natural units with dim. analysis cleanup)
# More generally for field theory with vacuum separation v:
# Gamma ~ (m^4 / 16 pi^2) exp(-S_E)

# In our M_Pl=1 units with delta_phi = O(1), S_E is O(m_tau) for m in M_Pl units.
# For physical m_tau << M_Pl, S_E in physical units = (delta_phi_GeV)^2 * m_tau_GeV / ?
# Schematic: S_E = m_tau * (delta_phi)^2 / 2 in natural mass^4*length^4 units

def tunneling_action(m_GeV, phi_GeV=phi_star_GeV):
    return m_GeV * phi_GeV**2 / mp.mpf(2)   # very rough estimate

print(f"\nSchematic tunneling action S_E ~ m_tau * (delta_phi)^2 / 2:")
print(f"{'m_tau':<15} {'S_E':<25} {'exp(-S_E)':<25}")
for name, m in [("100 GeV", mp.mpf("1e2")),
                 ("1 keV",   mp.mpf("1e-6")),
                 ("1e-5 eV", mp.mpf("1e-14")),
                 ("1e-22 eV",mp.mpf("1e-31"))]:
    SE = tunneling_action(m)
    print(f"{name:<15} {mp.nstr(SE, 4):<25} {mp.nstr(mp.exp(-SE) if SE < 700 else mp.mpf('0'), 4):<25}")

print()
print("Conclusion: with phi_* ~ 0.6 M_Pl, tunneling action S_E is HUGE (>>1)")
print("for any physical m_tau. The Z_2 vacua are EFFECTIVELY DECOUPLED on")
print("cosmological timescales -- no oscillation, just a degeneracy splitting.")
print("The Z_2 'oscillation' is more like a topological vacuum selection,")
print("not an inflaton-like coherent oscillation.")
print()
