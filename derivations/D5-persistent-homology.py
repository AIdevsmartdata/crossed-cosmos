"""
D5 — Persistent-Homology Betti numbers PH_k as probes of primordial fNL
======================================================================
Claim (paper §5 / eq. D5): The k-th Betti numbers β_k(ν) of the
sublevel-set filtration of the late-time cosmic density field smoothed
at scale R carry primordial non-Gaussianity information at a level
competitive with the bispectrum.  In particular, at the peak ν_* of the
persistence diagram, the expectation value shifts linearly in fNL:

    <β_k(ν_*)>_{fNL}  =  <β_k(ν_*)>_G  ×  [ 1  +  c_k(ν_*, R) · fNL ]

with c_k O(10^-4) per fNL unit at R ≃ 10 Mpc/h (Yip et al. 2024).

This file is a SCAFFOLD:
  1. Writes down symbolically (sympy) the Vietoris-Rips / Čech filtration
     value r(ν) on a Gaussian random field smoothed at scale R.
  2. States the leading fNL correction to <PH_k> at the peak, cited from
     Yip, Biagetti, Cole, Viswanathan, Shiu 2024 (arXiv:2403.13985),
     derived via the local-type bispectrum B(k1,k2,k3).
  3. Runs a minimal numpy demo: 2D Gaussian field + fNL·(φ²−<φ²>)
     perturbation on 64×64 grid, computes the Euler-characteristic curve
     χ(ν) of sublevel sets (proxy for β_0−β_1), plots fNL=0 vs fNL=100.

Full PH_k computation requires GUDHI or Ripser — NOT installed here.
Euler characteristic is a PH-consistent summary: χ = Σ_k (−1)^k β_k.

References:
  - Yip, Biagetti, Cole, Viswanathan, Shiu (2024) arXiv:2403.13985
    "Cosmology with persistent homology: a Fisher forecast"
  - Biagetti, Cole, Shiu (2021) JCAP 04 061, arXiv:2009.04819
  - Pranav et al. (2019) MNRAS 485, 4167 (Betti numbers of LSS)
  - Adler & Taylor (2007) "Random Fields and Geometry" (Gaussian kinematic formula)

Expected runtime: ≲ 3 s on a modern CPU (no GPU, no GUDHI).

Run:
  python3 D5-persistent-homology.py
"""

from sympy import (
    symbols, exp, sqrt, pi, integrate, oo, simplify, Rational,
    Function, Symbol, Piecewise, erf, diff, series, latex
)
import sympy as sp
import numpy as np
import os

# ── Symbols ──────────────────────────────────────────────────────────────────
nu, R, k, sigma0, sigma1, fNL = symbols(
    r'\nu R k \sigma_0 \sigma_1 f_{NL}', real=True
)
r_fil = symbols('r', positive=True)  # filtration radius

# ── 1. Filtration formula (Vietoris-Rips / Čech on smoothed GRF) ────────────
#
# Given a Gaussian random field φ(x) smoothed at scale R with a Gaussian
# kernel W_R(k) = exp(−k²R²/2), the sublevel-set filtration is:
#
#    X_ν  =  { x : φ_R(x) ≤ ν σ_0(R) }           (ν = threshold in units of σ)
#
# where σ_n²(R) = ∫ dk/(2π)^3  k^(2n) P(k) W_R(k)²  (spectral moments).
#
# The Čech / Vietoris-Rips complex on a point cloud of peaks is equivalent
# to thresholding the distance-to-peak function at r; by Gaussian kinematic
# formula (Adler-Taylor 2007) the expected Euler characteristic is:
#
#   <χ(ν)>_G  =  (V / (2π)^((d+1)/2)) × (σ_1/σ_0)^d × H_(d−1)(ν) × exp(−ν²/2)
#
# where H_n is the probabilist's Hermite polynomial and V the survey volume.

print("── D5: Persistent Homology scaffold ────────────────────────────────")
print()
print("── 1. Filtration value on smoothed GRF ─────────────────────────────")
print()
print("  σ_n²(R) = ∫ d³k/(2π)³  k^(2n) P(k) exp(−k²R²)")
print()
print("  Sublevel set:  X_ν = { x : φ_R(x) ≤ ν σ_0 }")
print()
print("  Vietoris-Rips radius at threshold ν (heuristic):")
print("    r(ν) ≃ (σ_0 / σ_1) × √(2 ln(1/Φ(ν)))       [Φ = Gaussian CDF]")
print()

# Symbolic Gaussian-kinematic-formula Euler characteristic (d=3):
# <χ(ν)> ∝ (ν² − 1) exp(−ν²/2)  × (σ_1/σ_0)^3
chi_GKF_3d = (nu**2 - 1) * sp.exp(-nu**2 / 2)
print(f"  <χ(ν)>_G (d=3, up to prefactor) ∝ {chi_GKF_3d}")
print()

# ── 2. Leading fNL correction to <PH_k> at peak ─────────────────────────────
#
# For local-type non-Gaussianity  φ_NG = φ_G + fNL (φ_G² − <φ_G²>),
# the skewness of the smoothed density field is (Matsubara 2003):
#
#    S_3(R) ≡ <δ_R³> / σ_0⁴  =  3 fNL × S_3^primordial(R)  +  S_3^gravity(R)
#
# To first order in fNL, the Euler characteristic curve shift is
# (Matsubara 2003, Codis et al. 2013, Yip et al. 2024 §3.2):
#
#    <χ(ν)>_NG − <χ(ν)>_G  ≃  σ_0 S_3 H_3(ν) × <χ(ν)>_G / 6
#
# At the persistence-diagram peak ν_* (Yip+24 find ν_* ≃ 1.1 for β_1, 2D):
#
#    <β_k(ν_*)>_NG / <β_k(ν_*)>_G  ≈  1 + c_k(ν_*, R) fNL
#    c_k(ν_*, R)  ≃  σ_0(R) × H_3(ν_*) × S_3^prim(R) / 6
#                 ≃  O(10^-4) per fNL unit at R = 10 Mpc/h  [Yip+24 Fig 5]

print("── 2. Leading fNL correction to <PH_k> at peak ─────────────────────")
print()
print("  Local fNL model:  φ(x) = φ_G(x) + fNL (φ_G² − <φ_G²>)")
print()
H3 = nu**3 - 3*nu
print(f"  H_3(ν) = {H3}")
print()
delta_chi = sigma0 * fNL * H3 * (nu**2 - 1) * sp.exp(-nu**2/2) / 2
delta_chi = sp.simplify(delta_chi)
print("  δ<χ(ν)>/⟨χ⟩_G  =  σ_0 · f_NL · H_3(ν) · S_3^prim / 6")
print(f"  Leading form (S_3^prim absorbed): {delta_chi}")
print()
print("  Peak shift:  <β_k(ν_*)>_NG = <β_k(ν_*)>_G · [1 + c_k fNL]")
print("  Yip+24 (arXiv:2403.13985) Fig 5:  c_1 ≃ 2·10^−4 / fNL at R=10 Mpc/h")
print()

# LaTeX for paper
print("── LaTeX (paste into paper) ─────────────────────────────────────────")
print(r"  \langle \beta_k(\nu_*) \rangle_{f_{NL}} = \langle \beta_k(\nu_*) \rangle_G "
      r"\left[ 1 + c_k(\nu_*, R)\, f_{NL} \right]")
print(r"  c_k \simeq \frac{\sigma_0(R)\, H_3(\nu_*)\, S_3^{\rm prim}(R)}{6}")
print()

# ── 3. Numpy demo: Euler characteristic curve at fNL=0 vs fNL=100 ──────────
print("── 3. Numpy demo: χ(ν) curve, 64×64 2D field ───────────────────────")

try:
    from scipy.ndimage import label as ndi_label
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False
    print("  [scipy.ndimage unavailable — using pure-numpy flood fill]")


def connected_components(mask):
    """Count 4-connected components of a 2D boolean mask."""
    if HAVE_SCIPY:
        _, n = ndi_label(mask)
        return n
    # Fallback: iterative flood fill
    visited = np.zeros_like(mask, dtype=bool)
    n = 0
    H, W = mask.shape
    for i in range(H):
        for j in range(W):
            if mask[i, j] and not visited[i, j]:
                n += 1
                stack = [(i, j)]
                while stack:
                    y, x = stack.pop()
                    if y < 0 or y >= H or x < 0 or x >= W:
                        continue
                    if visited[y, x] or not mask[y, x]:
                        continue
                    visited[y, x] = True
                    stack.extend([(y+1, x), (y-1, x), (y, x+1), (y, x-1)])
    return n


def generate_field(N=64, R_smooth=3.0, fNL_val=0.0, seed=42):
    """Gaussian field + local fNL perturbation, Gaussian-smoothed at scale R."""
    rng = np.random.default_rng(seed)
    phi_G = rng.standard_normal((N, N))
    # Smooth in Fourier space
    kx = np.fft.fftfreq(N) * N
    ky = np.fft.fftfreq(N) * N
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    K2 = KX**2 + KY**2
    W = np.exp(-0.5 * K2 * (R_smooth / N * 2*np.pi)**2)
    phi_G = np.real(np.fft.ifft2(np.fft.fft2(phi_G) * W))
    phi_G = (phi_G - phi_G.mean()) / phi_G.std()
    # Local fNL: φ = φ_G + fNL * (φ_G² − <φ_G²>) with small coupling
    phi = phi_G + 1e-4 * fNL_val * (phi_G**2 - np.mean(phi_G**2))
    return (phi - phi.mean()) / phi.std()


def euler_curve(field, nus):
    """Euler characteristic χ(ν) = β_0 − β_1 of sublevel sets {φ ≤ ν σ}."""
    chi = np.zeros_like(nus)
    for i, v in enumerate(nus):
        mask_sub = field <= v
        beta0 = connected_components(mask_sub)
        beta1 = connected_components(~mask_sub)  # holes ≈ components of complement − 1
        chi[i] = beta0 - max(beta1 - 1, 0)
    return chi


nus_grid = np.linspace(-3, 3, 41)
field_G   = generate_field(fNL_val=0.0)
field_NG  = generate_field(fNL_val=100.0)
chi_G  = euler_curve(field_G, nus_grid)
chi_NG = euler_curve(field_NG, nus_grid)

print(f"  fNL=0   : χ range = [{chi_G.min():.1f}, {chi_G.max():.1f}]")
print(f"  fNL=100 : χ range = [{chi_NG.min():.1f}, {chi_NG.max():.1f}]")
print(f"  Max |Δχ| = {np.max(np.abs(chi_NG - chi_G)):.2f}")
print()

# ── 4. Plot ──────────────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
    os.makedirs(figdir, exist_ok=True)
    outpath = os.path.join(figdir, 'D5-euler-char.pdf')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.plot(nus_grid, chi_G,  'b-',  lw=1.8, label=r'$f_{NL}=0$')
    ax1.plot(nus_grid, chi_NG, 'r--', lw=1.8, label=r'$f_{NL}=100$')
    ax1.set_xlabel(r'threshold $\nu$')
    ax1.set_ylabel(r'$\chi(\nu)=\beta_0-\beta_1$')
    ax1.set_title('Euler characteristic curve (64×64, R=3)')
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(nus_grid, chi_NG - chi_G, 'k-', lw=1.8)
    ax2.axhline(0, color='gray', lw=0.5)
    ax2.set_xlabel(r'threshold $\nu$')
    ax2.set_ylabel(r'$\Delta\chi(\nu)$')
    ax2.set_title(r'NG − G residual ($f_{NL}=100$)')
    ax2.grid(alpha=0.3)

    fig.suptitle('D5 — Persistent-homology Euler curve (SCAFFOLD demo)')
    fig.tight_layout()
    fig.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    print(f"  Plot saved: {outpath}")
except ImportError:
    print("  [matplotlib unavailable — plot skipped]")


if __name__ == "__main__":
    print()
    print("Status: SCAFFOLD — Euler-characteristic demo functional.")
    print("TODO  : Full β_0, β_1, β_2 via GUDHI SimplexTree on 3D N-body snapshot;")
    print("        numerical calibration of c_k(ν_*, R) at R ∈ {5,10,20} Mpc/h;")
    print("        Fisher matrix σ(fNL) forecast cross-checked vs Yip+24 Table 2.")
