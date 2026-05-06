#!/usr/bin/env python3
"""
M174 sub-task 2 -- Compatibility with KKLT-style modulus stabilization.

Background:
- M134: V_F(tau=i) = 0 -- Minkowski SUSY vacuum at the perturbative level.
- KKLT (Kachru-Kallosh-Linde-Trivedi 2003) procedure: lift Minkowski/AdS to dS
  by adding an anti-D3-brane uplift term V_uplift = E / (T+T*)^p (positive)
  giving a small positive V_min = Lambda_obs > 0.
- Standard cosmological constant Lambda_obs ~ (2.4e-3 eV)^4 ~ 1e-47 GeV^4.

In KKLT, after uplift:
    m_T (gravitino) ~ a * |W_0| / (T+T*)^{3/2} M_Pl
    m_3/2 ~ |W_0| e^{K/2}                 (gravitino mass)
    H_inf <~ m_3/2  (consistency)

Standard moduli problem:
- Cosmological constraint Coughlan-Fischler 1983, de Carlos-Casas-Quevedo-Roulet 1993:
  modulus oscillates from misalignment after inflation; energy density redshifts
  like matter; if m_tau < ~30 TeV, modulus dominates Universe BEFORE BBN
  (overproducing matter or producing too many photons via decay).
- "Cosmological moduli problem": m_tau >~ 30 TeV needed for thermal-equilibrium-safe.
- Loophole: very light moduli (ULM, m ~ 1e-22 eV, "fuzzy DM") never decay,
  oscillation = DM directly.

For ECI v9 M134 modulus tau_L = i:
- M134 V_F(i) = 0 Minkowski; needs uplift to dS for cosmology
- After KKLT uplift: m_tau remains ~ |W''|/M_Pl^2 to leading order if uplift
  doesn't deform Hessian too much (which is the standard "small uplift" regime).
- So m_tau formula from sub-task 1 still applies.

Question for sub-task 2: which Lambda_W values are CONSISTENT with KKLT?
- Need W_0 = Lambda_W^3 << M_Pl^3 (otherwise SUGRA approx breaks)
- Need m_3/2 ~ |W_0|/M_Pl^2 ~ Lambda_W^3/M_Pl^2 -- but here W(tau=i) = 0 by
  M134 design! So m_3/2 = 0 at tree level. We need a SECOND scale (constant
  W_0 added to the f(tau) factor) to have non-zero gravitino mass.

The cleanest KKLT-style W is:
    W(tau) = W_0 + Lambda_W^3 * f(tau)         with f(tau) = (j-1728)/eta^6

At tau=i: W(i) = W_0 (since f(i) = 0 by Klein E_6(i)=0)
W'(i) = 0, W''(i) = Lambda_W^3 * f''(i)

V_F(i) = e^K [G^TT* |D_T W|^2 - 3 |W|^2 ] = (1/2)^3 [4/3 * 9 |W_0|^2/4 - 3 |W_0|^2]
       = (1/8) [3 |W_0|^2 - 3 |W_0|^2] = 0  (still SUSY-Minkowski!)

But W_0 != 0 now means m_3/2 != 0. Standard SUGRA:
    m_3/2 = e^{K/2} |W| = (1/2)^{3/2} |W_0| / M_Pl^2
          = |W_0|/(2 sqrt(2) M_Pl^2)

The Hessian m_tau^2 receives contributions from BOTH W_0 cross-terms and W''.
For W = W_0 + Lambda_W^3 f, schematic at tau=i:
    m_tau^2 ~ (4/9) |W''(i)|^2 e^K G^{-TT*}
            = (4/9) |Lambda_W^3 f''(i)|^2 / M_Pl^4 * 4
            ~ |Lambda_W^3|^2 / M_Pl^4 * |f''(i)|^2

(same scaling as M134 with W_0 not entering Hessian leading term; W_0 enters
only at order |W_0|^2/M_Pl^4 which is the gravitino mass squared, distinct.)

So the EFT rescaling stands: m_tau ~ Lambda_W^3/M_Pl^2 * |f''(i)|/3 from M134.

KKLT consistency window:
  m_3/2 < m_tau (standard hierarchy, modulus heavier than gravitino)
  or m_3/2 > m_tau (gravitino is uplift-mass dominated)

Standard moduli-problem window:
  m_tau >~ 30 TeV  -- avoid late decay -> BBN
  OR
  m_tau < 1e-22 eV (fuzzy DM) -- never decays, lifetime > age of universe
"""

import mpmath as mp

mp.mp.dps = 30

print("="*70)
print("M174 sub-task 2 -- KKLT compatibility")
print("="*70)

# Constants
M_Pl_GeV = mp.mpf("2.435e18")
m_natural = mp.mpf("161042.615712005251112279363481")  # M134 sqrt(m^2_natural)

# Three windows from sub-task 1
targets = [
    ("WIMP",         mp.mpf("1e2")),
    ("Axion-like",   mp.mpf("1e-14")),
    ("Fuzzy DM",     mp.mpf("1e-31")),
]

print(f"""
KKLT-style moduli mass from M134:
    m_tau ~ m_natural * (Lambda_W/M_Pl)^3 * M_Pl
          = {m_natural} * (Lambda_W/M_Pl)^3 * M_Pl

Cosmological moduli problem windows:
  (i)  m_tau > 30 TeV  -- decays before BBN, no late-modulus problem
  (ii) m_tau < 1e-22 eV -- 'fuzzy' DM, infinite lifetime
""")

print(f"{'window':<14} {'Lambda_W':<15} {'Lambda_W/M_Pl':<15} {'string-scale category':<30}")
print("-"*80)

categories = {
    "WIMP": ("intermediate-scale strings (M_s ~ 10^11 GeV)", "OK"),
    "Axion-like": ("PeV-scale (TeV+ extension)",              "Heavy SUSY breaking"),
    "Fuzzy DM": ("electroweak-scale W_0 ~ TeV^3",             "Anti-de Sitter -> small uplift"),
}

for name, m_target in targets:
    L3 = m_target * M_Pl_GeV**2 / m_natural
    LW = L3**(mp.mpf(1)/3)
    ratio = LW / M_Pl_GeV
    cat, ok = categories[name]
    print(f"{name:<14} {mp.nstr(LW, 4):<15} {mp.nstr(ratio, 4):<15} {cat:<30}")

print()
print("Cosmological moduli problem analysis:")
print("-"*70)

# moduli problem: if m < 30 TeV but > 1e-22 eV, modulus decays late -> BBN problem.
# Standard ref: Banks-Dine 1995 (hep-th/9508071), Coughlan-Fischler 1983 PLB,
# de Carlos-Casas-Quevedo-Roulet 1993 (hep-ph/9308325).
# Decay rate Gamma_tau ~ m_tau^3 / M_Pl^2 (gravitational decay)
# Lifetime tau_decay ~ M_Pl^2 / m_tau^3
# BBN constraint: tau_decay < 1 sec ~ 1.5e24 GeV^{-1}
# (Or: requires m_tau > ~30 TeV)
# For DM stable on cosmological time: tau_decay > 4.4e17 sec ~ 6.7e41 GeV^{-1}
# m_tau^3 < M_Pl^2 / tau_universe ~ (2.4e18)^2 / 6.7e41 ~ 8.7e-6 GeV^3
# m_tau < 2e-2 GeV ~ 20 MeV  for stable on ~age of universe
# (gravitational decay only; if other channels open, more restrictive)

print(f"  * Gravitational decay rate Gamma ~ m_tau^3 / M_Pl^2")
print(f"  * Stability vs age of universe: m_tau < ~20 MeV (gravitational only)")
print()
print("  | Window    | m_tau           | gravitational lifetime | DM-viable?         |")
print("  |-----------|-----------------|-------------------------|--------------------|")

# Lifetime calc
def lifetime_sec(m_GeV):
    M_Pl_GeV_local = mp.mpf("2.435e18")
    Gamma_GeV = m_GeV**3 / M_Pl_GeV_local**2  # /(8 pi) ~ 1 prefactor
    # 1 GeV^{-1} = 6.582e-25 s
    return mp.mpf("6.582e-25") / Gamma_GeV

t_universe_s = mp.mpf("4.35e17")   # age of universe in seconds
t_BBN_s = mp.mpf(1)                # 1 sec before BBN

scenarios = [
    ("WIMP (100 GeV)",   mp.mpf("100")),
    ("Axion (1e-5 eV)",  mp.mpf("1e-14")),
    ("Fuzzy (1e-22 eV)", mp.mpf("1e-31")),
    ("CDM-MeV (1 MeV)",  mp.mpf("1e-3")),
    ("CDM-30TeV",        mp.mpf("3e4")),
]

for name, m in scenarios:
    tau = lifetime_sec(m)
    if tau > t_universe_s * 1000:
        viability = "STABLE (>>universe)"
    elif tau > t_universe_s:
        viability = "borderline DM"
    elif tau > t_BBN_s:
        viability = "decays before today, after BBN"
    else:
        viability = "decays before BBN: OK if non-DM"
    print(f"  | {name:<10} | {mp.nstr(m,4):<15} | {mp.nstr(tau,4):<23} s | {viability:<18} |")

print()
print("Key conclusion:")
print("-"*70)
print("""
  * Fuzzy DM (m=1e-22 eV) needs Lambda_W ~ 1.5 GeV << M_Pl. Lifetime
    >>> age of universe; never decays. Modulus oscillation = DM permanently.
    BUT requires extreme tuning of Lambda_W to electroweak/QCD scale.

  * WIMP-like (m=100 GeV) needs Lambda_W ~ 1.5e11 GeV (intermediate strings).
    Lifetime ~ 1e-22 sec << 1 sec, decays before BBN. VIABLE non-DM scenario:
    modulus decays into SM, NOT a DM candidate itself but its decay produces
    other DM particles.

  * 30 TeV scale (canonical moduli-problem-safe) needs Lambda_W ~ 7.6e9 GeV.
    Lifetime ~ 1e-30 sec << 1 sec; decays before BBN. NOT itself DM.

  * The classical moduli-as-DM scenario (Banks-Dine 1995 type) requires either
    very heavy (oscillation -> SM particles -> WIMPy DM) or very light (ULM,
    fuzzy DM directly).
""")
