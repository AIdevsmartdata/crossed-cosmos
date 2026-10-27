"""G5b : l'écart U_arb − U_grille de G5 à α = π/2 vient-il de la grille ? On raffine la grille polaire d'explore.py
(nr×nphi = 400×800 → 800×1600 → 1600×3200) : si c'est la grille, l'écart doit décroître vers ~|U_16 − U_40| ≈ 1e-11."""
import io, contextlib, numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    import explore
U_arb = {(1.5707963267948966, 1.18): 0.2685970826554730, (2.2, 1.18): 0.2610903856027070}   # G5 / G3 (N=16, mid Arb)
for nr, nphi in ((400, 800), (800, 1600), (1600, 3200)):
    gr, wr = np.polynomial.legendre.leggauss(nr); r = (gr + 1) / 2; wr = wr / 2
    phi = (np.arange(nphi) + 0.5) * 2 * np.pi / nphi; wphi = 2 * np.pi / nphi
    R, PH = np.meshgrid(r, phi, indexing='ij')
    explore.X = R * np.cos(PH); explore.Y = R * np.sin(PH); explore.W = (wr * r)[:, None] * wphi * np.ones_like(R)
    for (al, k), ua in U_arb.items():
        C, U = explore.quantities(k, al)
        print(f"G5b grille {nr}x{nphi} α={al:.4f} κ={k} U_grille={U:.13f} écart={abs(U-ua):.2e}", flush=True)
