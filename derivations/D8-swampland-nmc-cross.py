"""
D8 — Swampland × NMC cross-constraint
======================================
Derives the consistency bound that emerges if A4 (NMC thawing scalar χ) and
A5 (Dark Dimension with Swampland parameter c') share a common EFT cutoff Λ.

Formulation (user spec, paper/eci.tex §Axioms)
----------------------------------------------
  Λ ~ M_P · (H / M_P)^c'                              [Bedroya 2503.19898]
  PPN γ−1 ≈ −4 ξ_χ² (χ₀/M_P)²                          [D7]
  |γ−1| ≲ 2.3×10⁻⁵ (Cassini 1σ)                        [BIT 2003]
  EFT self-consistency for the op (ξ/2) R χ² :
       δM_P² ≡ ξ_χ χ₀²  ≤  Λ²
  ⇒    ξ_χ (χ₀/M_P)²  ≤  (Λ/M_P)²  =  (H/M_P)^(2c')

Combining:
  • Cassini:  |ξ_χ| (χ₀/M_P) ≤ 2.4×10⁻³                 (D7)
  • Swampland-EFT:  ξ_χ (χ₀/M_P)² ≤ (H_0/M_P)^(2c')

Eliminating (χ₀/M_P) between the two gives the cross-constraint; the
resulting region is plotted in the (c', ξ_χ) plane.

Limits verified
---------------
  (ξ_χ → 0):  Swampland-EFT is trivial; Cassini is trivial; recovers GR.
  (c'  → 0):  Λ → M_P; EFT cutoff disappears; the Swampland-EFT line
              ξ_χ (χ₀/M_P)² ≤ 1 becomes the no-ghost condition A4 already
              imposes; only Cassini survives → ξ_max = 2.4×10⁻² at
              χ₀=M_P/10 (D7 result, exactly).

Honesty
-------
  If the "shared cutoff" hypothesis is dropped (χ 4D-localised, KK bulk),
  the cross-constraint evaporates. The D8 result is conditional on
  A4-χ being a bulk mode of the same dark sector as A5-KK.
"""

# ─── runtime caps (per task spec) ───────────────────────────────────────────
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

import resource
resource.setrlimit(resource.RLIMIT_AS, (4_000_000_000, 4_000_000_000))

import logging
from logging.handlers import RotatingFileHandler
_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "D8.log")
_handler = RotatingFileHandler(_log_path, maxBytes=2_000_000, backupCount=1)
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler])
log = logging.getLogger("D8")

# ─── imports ────────────────────────────────────────────────────────────────
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ─── constants ──────────────────────────────────────────────────────────────
# Reduced Planck mass in GeV
M_P_GeV = 2.435e18
# H_0 ≈ 67.5 km/s/Mpc in GeV  (h·2.1332e-42 GeV,  h≈0.7)
H0_GeV = 1.44e-42
# Dimensionless ratio
x_H = H0_GeV / M_P_GeV       # ≈ 5.9×10⁻⁶¹
log.info(f"H0/M_P = {x_H:.3e}")

# Cassini 1σ PPN envelope
gamma_minus_1_max = 2.3e-5
cassini_bound = 0.5 * np.sqrt(gamma_minus_1_max)   # |ξ|·(χ₀/M_P) ≤ this
# = 2.398e-3

# Reference thawing amplitude used in D7
chi0_over_MP_ref = 0.1     # χ₀ = M_P / 10

# ═══════════════════════════════════════════════════════════════════════════
# PART 1 — Symbolic setup & limit checks
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("D8 — Swampland × NMC cross-constraint")
print("=" * 72)

xi, chi, MP, H, Mp, cp = sp.symbols(r"xi chi M_P H M_P c'",
                                    positive=True, real=True)
# Cutoff (user spec)
Lambda = MP * (H / MP) ** cp
print(f"\nΛ(c', H) = M_P · (H/M_P)^c'")

# EFT self-consistency:  ξ χ₀² ≤ Λ²
eft_condition = sp.Eq(xi * chi**2, Lambda**2)
x = chi / MP    # χ₀/M_P
eft_x_max = sp.sqrt((Lambda / MP)**2 / xi)    # x ≤ sqrt(Λ²/(ξ M_P²))
print(f"EFT-bulk:  (χ₀/M_P)_max = (H/M_P)^c' / sqrt(ξ)")

# Cassini bound (D7):  ξ · x ≤ b_C
b_C = sp.Symbol("b_C", positive=True)   # = 2.4e-3
x_cassini_max = b_C / xi

# Cross-constraint: the allowed χ₀/M_P must satisfy BOTH
# → ξ is consistent iff there EXISTS some χ₀/M_P > 0 in both regions,
# but if we demand the same physical χ₀, we compare the two upper limits.
# The tighter of the two controls:
#   EFT gives small x  ⟺  large ξ or large c'
#   Cassini gives small x  ⟺  large ξ
# For a GIVEN χ₀ demanded by phenomenology, ξ is bounded above by min of:
#   ξ_C(χ₀)   = b_C / (χ₀/M_P)                         [Cassini]
#   ξ_S(c', χ₀) = (H_0/M_P)^(2c') / (χ₀/M_P)²          [Swampland-EFT]

# Limit checks
print("\n— Limit checks (symbolic) —")
# (a) ξ → 0: both constraints are vacuous. EFT: 0 ≤ Λ² (trivial).
lim_a = sp.limit(xi * x**2, xi, 0)
assert lim_a == 0, "ξ→0 should make the NMC op vanish"
print(f"  ξ→0  :  ξ(χ/M_P)² → {lim_a}  ✓ (minimal coupling recovered)")

# (b) c' → 0: Λ → M_P, so EFT says ξ χ₀² ≤ M_P², i.e. ξ x² ≤ 1 — the
#    no-ghost condition already in the paper. Cassini alone remains the
#    binding constraint → reproduces D7 value.
Lambda_c0 = Lambda.subs(cp, 0)
assert sp.simplify(Lambda_c0 - MP) == 0, "c'→0 should give Λ=M_P"
print(f"  c'→0 :  Λ → M_P ; EFT reduces to no-ghost ξχ²<M_P² (A4)  ✓")
print(f"          Cassini-only bound (D7) recovered: |ξ|·(χ/M_P) ≤ 2.4e-3")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2 — Numerics: tightening of |ξ_max| vs c'
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 2 — Numerical bounds in (c', ξ) plane")
print("=" * 72)

def xi_max_cassini(x_chi):
    """Cassini-only: |ξ| ≤ 2.4e-3 / (χ₀/M_P)."""
    return cassini_bound / x_chi

def xi_max_swampland(cprime, x_chi):
    """EFT self-consistency: ξ ≤ (H_0/M_P)^(2c') / (χ₀/M_P)²."""
    return (x_H ** (2.0 * cprime)) / (x_chi ** 2)

def xi_max_joint(cprime, x_chi):
    return min(xi_max_cassini(x_chi), xi_max_swampland(cprime, x_chi))

# Reference χ₀ = M_P/10 (D7 fiducial)
print(f"\nFiducial χ₀ = M_P/10  (same as D7):")
print(f"  Cassini-only              : |ξ_max| = {xi_max_cassini(chi0_over_MP_ref):.3e}")
for cv in [0.01, 0.05, 0.10, 0.20, 0.50]:
    xm_s = xi_max_swampland(cv, chi0_over_MP_ref)
    xm_j = xi_max_joint(cv, chi0_over_MP_ref)
    tight = 1.0 - xm_j / xi_max_cassini(chi0_over_MP_ref)
    print(f"  c'={cv:4.2f}: Swampland |ξ|≤{xm_s:.2e} | joint |ξ|≤{xm_j:.2e}"
          f"  (tightening {100*tight:+.1f}%)")

# Same analysis for χ₀ = M_P (strong thawing)
print(f"\nStrong-thawing χ₀ = M_P:")
print(f"  Cassini-only              : |ξ_max| = {xi_max_cassini(1.0):.3e}")
for cv in [0.01, 0.05, 0.10, 0.20, 0.50]:
    xm_s = xi_max_swampland(cv, 1.0)
    xm_j = xi_max_joint(cv, 1.0)
    tight = 1.0 - xm_j / xi_max_cassini(1.0)
    print(f"  c'={cv:4.2f}: Swampland |ξ|≤{xm_s:.2e} | joint |ξ|≤{xm_j:.2e}"
          f"  (tightening {100*tight:+.1f}%)")

# Headline tightening at task-specified fiducial c'=0.05±0.01, χ₀=M_P/10
cp0, cpE = 0.05, 0.01
xm_S_cent = xi_max_swampland(cp0, chi0_over_MP_ref)
xm_S_low  = xi_max_swampland(cp0 + cpE, chi0_over_MP_ref)
xm_S_hi   = xi_max_swampland(cp0 - cpE, chi0_over_MP_ref)
xm_C      = xi_max_cassini(chi0_over_MP_ref)
print("\nHeadline (χ₀=M_P/10, c'=0.05±0.01):")
print(f"  Cassini (D7)           : |ξ_max| = {xm_C:.3e}")
print(f"  Swampland-EFT (central): |ξ_max| = {xm_S_cent:.3e}  "
      f"(range [{min(xm_S_low,xm_S_hi):.2e}, {max(xm_S_low,xm_S_hi):.2e}])")
if xm_S_cent < xm_C:
    tighten = 1.0 - xm_S_cent / xm_C
    print(f"  ⇒ Cross-constraint TIGHTENS |ξ| by {100*tighten:.1f}%")
else:
    loosen = xm_S_cent / xm_C
    print(f"  ⇒ Swampland-EFT looser by ×{loosen:.2e} — Cassini remains binding.")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3 — Compatibility of A4 (thawing DE phenomenology) with A5-EFT cutoff
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 3 — A4↔A5 phenomenological compatibility")
print("=" * 72)
# For the thawing DE to drive acceleration today, χ₀/M_P ~ O(0.1–1)
# (Scherrer-Sen, Ye-Piao). The Swampland-EFT bound with same cutoff:
#   χ₀/M_P ≤ sqrt((H/M_P)^(2c') / ξ)
# For ξ ~ 10⁻² and c' = 0.05: sqrt((10⁻⁶⁰·⁵)² / 10⁻²) = sqrt(10⁻¹·⁴) = small
# But the user's stated cutoff is Λ~meV ≃ 4e-31 · M_P (formula gives different
# value for c'=0.05 — we report both).
Lambda_over_MP_formula = x_H ** cp0
Lambda_over_MP_meV = 1e-12 / M_P_GeV       # meV-in-GeV over M_P
print(f"  Λ/M_P from formula (c'=0.05)    : {Lambda_over_MP_formula:.2e}")
print(f"  Λ/M_P for Λ = 1 meV (user spec) : {Lambda_over_MP_meV:.2e}")
print(f"  → the two differ by {Lambda_over_MP_formula/Lambda_over_MP_meV:.1e};")
print(f"    the c' that makes Λ=meV is c' ≈ log(Λ_meV/M_P)/log(H_0/M_P)"
      f" = {np.log(Lambda_over_MP_meV)/np.log(x_H):.3f}")

# EFT-allowed χ₀/M_P at ξ = ξ_max^Cassini:
xi_test = xm_C
x_max_eft_formula = np.sqrt((x_H**(2*cp0)) / xi_test)
x_max_eft_meV     = np.sqrt((Lambda_over_MP_meV**2) / xi_test)
print(f"\n  At |ξ|=2.4×10⁻², bulk-χ max (χ₀/M_P):")
print(f"    formula cutoff: {x_max_eft_formula:.2e}")
print(f"    meV cutoff    : {x_max_eft_meV:.2e}")
print(f"  Thawing DE needs χ₀/M_P ~ 0.1–1  → {'OK' if x_max_eft_formula>=0.1 else 'INCOMPATIBLE'}"
      f" (formula) ; {'OK' if x_max_eft_meV>=0.1 else 'INCOMPATIBLE'} (meV).")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4 — 2D plot in (c', ξ) plane at χ₀ = M_P/10
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 4 — 2D plot")
print("=" * 72)

cprime_grid = np.linspace(0.0, 0.6, 400)
xi_grid     = np.logspace(-6, 0, 400)
CP, XI = np.meshgrid(cprime_grid, xi_grid)

x_chi = chi0_over_MP_ref
allowed_cassini   = (XI * x_chi) <= cassini_bound
allowed_swampland = (XI * x_chi**2) <= (x_H ** (2.0 * CP))
allowed_both      = allowed_cassini & allowed_swampland

fig, ax = plt.subplots(figsize=(7.2, 5.6))

# Cassini exclusion (horizontal line, indep. of c')
xi_C_line = cassini_bound / x_chi
ax.axhline(xi_C_line, color="crimson", lw=2.0, ls="-",
           label=rf"Cassini (D7): $|\xi_\chi|\leq{xi_C_line:.2e}$ (at $\chi_0=M_P/10$)")
ax.fill_between(cprime_grid, xi_C_line, 1.0, color="crimson", alpha=0.12)

# Swampland-EFT exclusion (diagonal in log-space)
xi_S_line = (x_H ** (2.0 * cprime_grid)) / x_chi**2
ax.plot(cprime_grid, xi_S_line, color="navy", lw=2.0, ls="--",
        label=r"Swampland-EFT: $\xi_\chi\leq(H_0/M_P)^{2c'}/(\chi_0/M_P)^2$")
ax.fill_between(cprime_grid, xi_S_line, 1.0, color="navy", alpha=0.10)

# Joint allowed region (intersection) — shade green
joint = np.minimum(xi_C_line * np.ones_like(cprime_grid), xi_S_line)
ax.fill_between(cprime_grid, 1e-6, joint, color="seagreen", alpha=0.25,
                label="Allowed region (A4 ∧ A5, shared cutoff)")

# Mark the A5 fiducial c' = 0.05
ax.axvline(0.05, color="black", lw=0.8, ls=":", alpha=0.7)
ax.text(0.052, 2e-6, r"$c'_{A5}=0.05$", fontsize=9, rotation=90, va="bottom")

# Mark the meV-equivalent c' ≈ 0.52
c_meV = np.log(Lambda_over_MP_meV) / np.log(x_H)
ax.axvline(c_meV, color="grey", lw=0.8, ls=":", alpha=0.7)
ax.text(c_meV + 0.005, 2e-6, rf"$c'_{{\Lambda=\mathrm{{meV}}}}\!\simeq\!{c_meV:.2f}$",
        fontsize=9, rotation=90, va="bottom")

ax.set_yscale("log")
ax.set_xlabel(r"Swampland parameter $c'$")
ax.set_ylabel(r"NMC coupling $|\xi_\chi|$")
ax.set_title(r"D8 — Cross-constraint in $(c',\xi_\chi)$ plane at $\chi_0=M_P/10$")
ax.set_xlim(0, 0.6)
ax.set_ylim(1e-6, 1.0)
ax.grid(True, which="both", ls=":", alpha=0.4)
ax.legend(loc="lower left", fontsize=9, framealpha=0.9)

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(out_dir, exist_ok=True)
out_pdf = os.path.join(out_dir, "D8-c-xi-overlap.pdf")
out_png = os.path.join(out_dir, "D8-c-xi-overlap.png")
fig.tight_layout()
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=140)
plt.close(fig)
print(f"Figure saved: {out_pdf}")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY — machine-readable
# ═══════════════════════════════════════════════════════════════════════════
summary = {
    "cassini_xi_max_at_chi0_MP_over_10": xi_max_cassini(chi0_over_MP_ref),
    "swampland_xi_max_cprime_0p05_chi0_MP_over_10": xi_max_swampland(0.05, chi0_over_MP_ref),
    "joint_xi_max_cprime_0p05_chi0_MP_over_10": xi_max_joint(0.05, chi0_over_MP_ref),
    "tightening_vs_D7_fractional": max(0.0, 1.0 - xi_max_joint(0.05, chi0_over_MP_ref)
                                             / xi_max_cassini(chi0_over_MP_ref)),
    "cprime_meV_equivalent": float(c_meV),
    "chi0_max_over_MP_at_xi_Cassini_formula": float(x_max_eft_formula),
    "chi0_max_over_MP_at_xi_Cassini_meV":     float(x_max_eft_meV),
}
print("\n--- SUMMARY ---")
for k, v in summary.items():
    print(f"  {k} = {v}")
log.info(f"summary: {summary}")
print("\nDone.")
