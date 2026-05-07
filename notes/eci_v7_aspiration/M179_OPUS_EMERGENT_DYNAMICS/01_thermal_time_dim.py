"""
M179 — Test of dimensional structure of Connes-Rovelli thermal time σ_t

Verbatim Connes-Rovelli 1994 (gr-qc/9406019):

  Eq (43)  α_t A = e^{i β t H} A e^{-i β t H}
  Eq (44)  α_t  =  γ_{β t}                       (modular = Hamilton, rescaled by β)
  Eq (55)  α_t  =  β_{2π a^{-1} t}               (Bisognano-Wichmann, Rindler wedge)
  Eq (56)  t_{thermal}  =  (2π / a) τ_{proper}
  Eq (57)  T = a / (2π k_b)                      (Unruh)

  §5 verbatim: "the classical limit of the thermodynamical time hypothesis
   implies that the thermal time defined by the cosmic background radiation
   is precisely the conventional Friedman-Robertson-Walker time"
   (citing Rovelli, Class. Quant. Grav. 10 (1993) 1567).

KEY DIMENSIONAL POINT:
  α_t is a 1-parameter group of automorphisms.  Its parameter t is
  DIMENSIONLESS (the "time" in α_t = exp(i t H) carries [time]·[energy]
  via H, so for the unit α_t to be dimensionless we have [t]·[H] = 1
  in ℏ = 1 units, hence [t] = [E]^{-1} = [T]).

  The thermal flow has natural [T]-dimension because H carries [E].
  But for the abstract Tomita-Takesaki α_t = Δ^{-it}, t is a pure number
  (Δ is a positive operator on a Hilbert space, no physics dimension).

  The DIMENSIONAL bridge is provided by the IDENTIFICATION of σ_t with
  a physical time flow γ_τ via the Bisognano-Wichmann / Connes-Rovelli
  proportionality relations: the constant of proportionality (β in non-
  rel limit, 2π/a in Rindler, T_CMB-related in FRW) carries the [T]-
  dimension.

CONSEQUENCE FOR ECI v9:
  σ_t on type II_∞ algebra (M28 / M101 / M141 / M148) is INTRINSICALLY
  DIMENSIONLESS unless we identify it with a physical clock.  Just like
  λ_BKL = π²/(6 log 2) is a dimensionless rate (per Gauss-shift iteration),
  not a physical [T^{-1}].

  This is exactly the M175 dimensional bridge failure restated.

WHAT EMERGENT REFRAMING MIGHT ADD:
  If the FRW thermal time IS the Connes-Rovelli σ_t for the photon-gas
  KMS state, then asking for H_0 = d/dt log(a) is the question:
  what is the LATE-TIME DRIFT RATE of σ_t against the FRW comoving
  observer's clock?  Answer (by definition): they coincide.  H_0 must
  still be set by Friedmann: H² = (8πG/3) ρ_tot.  The thermal time
  hypothesis does NOT predict H_0.
"""
import mpmath
mpmath.mp.dps = 30

# Fundamental constants in SI then natural units
hbar_SI = mpmath.mpf("1.054571817e-34")            # J·s
k_B_SI = mpmath.mpf("1.380649e-23")                # J/K
T_CMB = mpmath.mpf("2.7255")                        # K  (Fixsen 2009)
c_SI = mpmath.mpf("299792458")                      # m/s
G_SI = mpmath.mpf("6.67430e-11")                    # m^3 kg^-1 s^-2

# The thermal time scale set by the CMB photon gas
# β = ℏ/(k_B T) — this is the modular flow period in [T]
beta_CMB = hbar_SI / (k_B_SI * T_CMB)
print(f"β_CMB = ℏ/(k_B T_CMB) = {beta_CMB} s")
print(f"           = {1/beta_CMB} Hz   (CMB Bohr frequency)")
print()

# Hubble time today (Planck 2018-like)
H0_SI = mpmath.mpf("67.4") * 1000 / (mpmath.mpf("3.0857e22"))  # s^-1
t_H = 1 / H0_SI
print(f"H_0 = 67.4 km/s/Mpc = {H0_SI} s^-1")
print(f"t_H = 1/H_0       = {t_H} s = {t_H / (3600*24*365.25*1e9)} Gyr")
print()

# Ratio: thermal time period vs Hubble time
ratio = beta_CMB * H0_SI
print(f"H_0 · β_CMB = (CMB Bohr freq) / (Hubble freq) DIMENSIONLESS = {ratio}")
print(f"Inverse:      Hubble time / β_CMB                          = {1/ratio}")
print()

# This is HUGE -- thermal time period is much shorter than the Hubble time
# β_CMB ~ 2.8e-12 s, t_H ~ 4.6e17 s, ratio ~ 1.6e29
# So if H_0 emerged from σ_t, it would have to be a vastly suppressed rate

# Connes-Rovelli §5 equates σ_t with FRW time t up to overall scaling β.
# Effectively σ_t is THE time, β is just the unit choice.
# So d/dt log(a) computed in σ_t coordinate = H(t) by definition,
# not derived from arithmetic.

print("="*68)
print("VERDICT 01_thermal_time_dim:")
print("="*68)
print()
print("Connes-Rovelli σ_t IS the FRW Friedmann time when ω is the")
print("photon-gas KMS state.  This identifies WHICH time variable, not its")
print("RATE H_0.  The Friedmann equation H^2 = (8πG/3) ρ_tot still requires")
print("ρ_tot input from cosmology measurements.")
print()
print("The dimensional bridge t_{thermal} = (β / 2π) τ_proper  (Eq 56-57)")
print("provides [T]-dimension via the inverse temperature β = 1/(k_B T).")
print("In FRW with photon T_CMB = 2.7255 K, β_CMB ≈ 2.8e-12 s.")
print()
print("This is six orders below CMB last-scattering time (380 kyr after BB)")
print("and twenty-nine orders below Hubble time.  σ_t is a HIGH-FREQUENCY")
print("clock; it does not carry information about late-time expansion rate.")
