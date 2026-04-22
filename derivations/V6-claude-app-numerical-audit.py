import numpy as np
from math import pi, sqrt, log, exp

# Fundamental constants
c = 2.99792458e8         # m/s
G = 6.67430e-11          # m^3 kg^-1 s^-2
hbar = 1.054571817e-34   # J·s
kB = 1.380649e-23        # J/K
h = 2*pi*hbar

# ----- Claim 1: Planck angular frequency
omega_P = sqrt(c**5/(G*hbar))
print(f"[C1] omega_P = sqrt(c^5/Ghbar) = {omega_P:.6e} rad/s")
print(f"     Claimed  = 1.85487e43 rad/s")
print(f"     Match: {abs(omega_P - 1.85487e43)/1.85487e43 < 1e-3}")
print()

# ----- Claim 2: omega_P = 2*pi*kB*T_P/hbar
T_P = sqrt(hbar*c**5/(G*kB**2))
omega_from_T_P = 2*pi*kB*T_P/hbar
print(f"[C2] T_P = {T_P:.6e} K")
print(f"     2*pi*kB*T_P/hbar = {omega_from_T_P:.6e} rad/s")
print(f"     omega_P           = {omega_P:.6e} rad/s")
print(f"     Ratio 2pi*kT_P/hbar / omega_P = {omega_from_T_P/omega_P:.4f}")
print(f"     IDENTITY '2pi kB T_P/hbar = omega_P' EXACT? {abs(omega_from_T_P - omega_P)/omega_P < 1e-6}")
print()

# ----- Claim 3: H_0 = 2.184e-18 s^-1 (and 67.4 km/s/Mpc consistency)
Mpc_in_m = 3.0857e22
H0_kmsMpc = 67.4
H0_SI = H0_kmsMpc*1000/Mpc_in_m
print(f"[C3] H_0 (67.4 km/s/Mpc) = {H0_SI:.4e} s^-1")
print(f"     Claimed = 2.184e-18 s^-1")
print(f"     Match (67.4) : {abs(H0_SI - 2.184e-18)/2.184e-18 < 0.01}")
# Try SH0ES
H0_SH = 73.0*1000/Mpc_in_m
print(f"     H_0 (73.0 km/s/Mpc) = {H0_SH:.4e} s^-1")
print()

# ----- Claim 4: Lambda/M_P^4 = (H_0/omega_P)^2 = 10^-122
ratio_sq = (H0_SI/omega_P)**2
print(f"[C4] (H_0/omega_P)^2 = {ratio_sq:.4e}")
print(f"     Claimed = 10^-122")
print(f"     log10 = {log(ratio_sq)/log(10):.2f}")
# Actual Lambda/M_P^4
# Lambda = 3 Omega_Lambda H_0^2 / c^2; energy density rho_Lambda = Lambda*c^2/(8*pi*G)
Omega_L = 0.6847
rho_L = Omega_L * 3*H0_SI**2 * c**2/(8*pi*G)  # J/m^3
# Planck energy density rho_P = M_P^4 c^5/hbar^3
M_P = sqrt(hbar*c/G)
rho_P = c**5 * M_P**4 / hbar**3 / c**3  # natural-units Planck energy density: roughly c^7/(hbar G^2)
# cleaner: rho_P in Planck natural units = 1 Planck^4 = c^7/(hbar G^2) energy/vol
rho_P = c**7/(hbar*G**2)
print(f"     rho_Lambda = {rho_L:.4e} J/m^3")
print(f"     rho_Planck = {rho_P:.4e} J/m^3")
print(f"     rho_L/rho_P = {rho_L/rho_P:.4e}, log10 = {log(rho_L/rho_P)/log(10):.2f}")
print(f"     Conventional cosmological constant problem: log10(rho_L/rho_P) ~ -123 (well known)")
print(f"     (H_0/omega_P)^2 log10 = {log(ratio_sq)/log(10):.2f}")
print()

# ----- Claim 5: PBH at M* = 5.1e14 g, S_BH ~ 10^25
M_star_g = 5.1e14
M_star_kg = M_star_g*1e-3
# BH entropy S/kB = A/(4 hbar G/c^3) = 4*pi*G*M^2/(hbar c) (Schwarzschild)
S_star = 4*pi*G*M_star_kg**2/(hbar*c)  # dimensionless (in units of kB)
print(f"[C5] S_BH(M*=5.1e14 g) = {S_star:.4e} (in kB)")
print(f"     Claimed ~ 10^25")
print(f"     log10 = {log(S_star)/log(10):.2f}")
print()

# ----- Claim 6: S^-0.05 ~ 0.055, ln S ~ 58, Dt/tau ~ 3
S = S_star
S_pow = S**(-0.05)
ln_S = log(S)
print(f"[C6] S^-0.05 = {S_pow:.4f} (claimed 0.055)")
print(f"     ln S    = {ln_S:.2f} (claimed 58)")
print(f"     S^-0.05 * ln S = {S_pow*ln_S:.4f} (claimed ~3)")
print()

# ----- Claim 7: T_dS = hbar H_0/(2 pi kB)
T_dS = hbar*H0_SI/(2*pi*kB)
print(f"[C7] T_dS = hbar H_0/(2 pi kB) = {T_dS:.4e} K")
print(f"     Claimed = 2.66e-30 K")
print()

# ----- Claim 8: LISA Omega_gw h^2 sensitivity 5e-13 at 1 mHz (Claude app claim)
print(f"[C8] LISA sensitivity at 1 mHz: literature value is typically Omega_gw h^2 ~ 1e-11 to 1e-13 depending on configuration.")
print(f"     Document claims 5e-13. Order of magnitude plausible but configuration-dependent.")
print()

# ----- Claim 9: 1/4 factor from 2pi/8pi
print(f"[C9] Claim: '2pi/8pi = 1/4' provides Bekenstein-Hawking 1/4 factor.")
print(f"     Arithmetic: 2pi/8pi = 1/4 ✓. But connecting this to S_BH = A/4 requires")
print(f"     a specific derivation; the document assertion is heuristic, not derivational.")
