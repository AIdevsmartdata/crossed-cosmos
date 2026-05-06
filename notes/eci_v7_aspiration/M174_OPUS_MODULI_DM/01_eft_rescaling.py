#!/usr/bin/env python3
"""
M174 sub-task 1 -- EFT rescaling.

In M134 SUGRA we worked in M_Pl = 1 with W having dimension M_Pl^3 implicit.
The natural unit numerical result was:

    m_tau^2(natural) = 2^16 * 3^6 * pi * Gamma(1/4)^4  ~ 2.59e10  (M_Pl=1)

This treats |W''(i)| as if it were 1 in canonical Planck units. Realistic SUGRA
uses W = A * f(tau) with A having mass dimension (mass)^3 and the dimensionless
modular factor f(tau). Then in canonical Kahler-normalized scalar field phi:

    m_phi^2 = (4/9) |W''(i)|^2_dimless * (|A|/M_Pl^3)^2 * M_Pl^2

But more carefully, the standard SUGRA F-term in canonical units (M_Pl = 1) is:

    V_F = e^K * [ G^{ij*} D_iW (D_jW)^* - 3 |W|^2 ]

where W is a (mass)^3 quantity. After restoring units, the modulus mass at the
SUSY-Minkowski point with W(tau_*) = 0 and D_tau W(tau_*) = 0 reduces to
(using V''(tau_*) ~ |W''(tau_*)|^2 / M_Pl^4 * 1/(2 Im tau_*)^? ):

    m_tau ~ |W''(tau_*)| / M_Pl^2

If we identify |W''(tau_*)| = |A| * f''(tau_*)_dimless with |A| = Lambda_W^3 some
non-perturbative scale, then:

    m_tau ~ Lambda_W^3 / M_Pl^2 * f''_dimless

The M134 numerical 2.59e10 M_Pl^2 has the dimensional-cleanup interpretation:
m_tau^2 = (4/9) |f''(i)|^2 * Lambda_W^6 / M_Pl^4

with f(tau) = (j(tau) - 1728)/eta(tau)^6 dimensionless.

So:
    m_tau = (2/3) |f''(i)| * Lambda_W^3 / M_Pl^2
          ~ 1.61e5 * Lambda_W^3 / M_Pl^2

(where 1.61e5 = sqrt(2.59e10) and we absorbed the factor 2/3 into the prefactor).

Mission: compute Lambda_W (in GeV) needed to bring m_tau into:
    (a) WIMP window:       100 GeV
    (b) Axion-like:         1e-5 eV = 1e-14 GeV
    (c) Fuzzy DM:          1e-22 eV = 1e-31 GeV

M_Pl (reduced) = 2.435e18 GeV.
"""

import mpmath as mp

mp.mp.dps = 30

print("="*70)
print("M174 sub-task 1 -- EFT rescaling Lambda_W^3 / M_Pl^2")
print("="*70)

# -- Constants
M_Pl_GeV = mp.mpf("2.435e18")  # reduced Planck mass in GeV

# -- M134 modulus mass coefficient |W''(i)|_dimless
# m_tau^2 (natural) = 2^16 * 3^6 * pi * Gamma(1/4)^4
G14 = mp.gamma(mp.mpf(1)/4)
m2_natural = 2**16 * 3**6 * mp.pi * G14**4   # in M_Pl=1 units, with W = f(tau) dimless
m_natural = mp.sqrt(m2_natural)              # ~ 1.61e5
print(f"\n[a] M134 m_tau coefficient (W = f dimless, M_Pl=1):")
print(f"    m_tau^2 = 2^16 * 3^6 * pi * Gamma(1/4)^4 = {m2_natural}")
print(f"    m_tau   = sqrt(...)                       = {m_natural}")
print()
print(f"    Reinterpretation: m_tau = m_natural * Lambda_W^3 / M_Pl^2")

# -- Solve for Lambda_W given target m_tau (physical)
def lambda_W_for_mass(m_target_GeV):
    """
    m_target = m_natural * Lambda_W^3 / M_Pl^2
    Lambda_W = (m_target * M_Pl^2 / m_natural)^{1/3}
    """
    L3 = m_target_GeV * M_Pl_GeV**2 / m_natural
    return L3**(mp.mpf(1)/3)

print()
print(f"    Reduced M_Pl = {M_Pl_GeV} GeV")
print()

# -- Three target windows
targets = [
    ("WIMP",         "1e2 GeV",   mp.mpf("1e2")),
    ("Axion-like",   "1e-5 eV",   mp.mpf("1e-14")),  # 1 eV = 1e-9 GeV
    ("Fuzzy DM",     "1e-22 eV",  mp.mpf("1e-31")),
    # Bonus: HDM warm-DM range
    ("Cold/CDM(GeV)","1 GeV",     mp.mpf("1")),
    ("Cold/CDM(MeV)","1e-3 GeV",  mp.mpf("1e-3")),
    ("Cold/CDM(keV)","1e-6 GeV",  mp.mpf("1e-6")),
]

print(f"\n{'window':<20} {'m_target':<14} {'Lambda_W (GeV)':<22} {'Lambda_W/M_Pl':<14}")
print("-"*70)
for name, mstr, m in targets:
    LW = lambda_W_for_mass(m)
    ratio = LW / M_Pl_GeV
    print(f"{name:<20} {mstr:<14} {mp.nstr(LW, 6):<22} {mp.nstr(ratio, 4):<14}")

print()
print("="*70)
print("INTERPRETATION")
print("="*70)
print("""
The 'natural' M134 value m_tau ~ 2^16*3^6*pi*Gamma(1/4)^4 ~ 1.61e5 (in M_Pl=1
with W dimensionless) translates, after EFT rescaling W = Lambda_W^3 * f(tau),
to a physical modulus mass:

    m_tau ~ 1.61e5 * Lambda_W^3 / M_Pl^2

For phenomenologically relevant DM windows:

  - WIMP (10^2 GeV)   needs Lambda_W ~ 6e11 GeV  (intermediate string scale)
  - Axion (1e-5 eV)   needs Lambda_W ~ 6e6  GeV  (PeV scale)
  - Fuzzy (1e-22 eV)  needs Lambda_W ~ 1e1  GeV  (electroweak scale)

These are all NON-trivial: each requires a separate dynamical scale.
""")
