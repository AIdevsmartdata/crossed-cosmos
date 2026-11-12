"""Constantes de la chaine de doublement avec la majoration POLYNOMIALE e^x - 1 <= x + x^2 (0 <= x <= 1),
celle qui sera utilisee en Lean (Mathlib : Real.abs_exp_sub_one_sub_id_le). Arithmetique rationnelle exacte.
f(x) = 2 (e^x - 1)^2 <= fp(x) := 2 (x + x^2)^2.
Chaine (CRITERE.md T-A §4) : g0 = D, A_j <= fp(g_j), g_{j+1} = 2 g_j + fp(g_j), Delta(2n) <= sum_j 2^{d-1-j} fp(g_j).
On imprime C_d(eta) = Phi_d(eta)/eta^2 (exact), la condition C*eta <= 1/2, et les majorants lineaires g_j <= c_j D utilises en Lean.
"""
from fractions import Fraction as Fr

def fp(x):
    return 2 * (x + x * x) ** 2

def chaine(d, D):
    g = D
    gs, As = [], []
    for j in range(d):
        gs.append(g)
        A = fp(g)
        As.append(A)
        g = 2 * g + A
    Phi = sum(2 ** (d - 1 - j) * As[j] for j in range(d))
    return gs, As, Phi

for d, eta, Ccible in [(4, Fr(1, 512), 256), (3, Fr(1, 128), 64), (4, Fr(1, 4096), 256), (2, Fr(1, 32), 16)]:
    gs, As, Phi = chaine(d, eta)
    C = Phi / eta ** 2
    print(f"d={d} eta=1/{1/eta} : C_poly(eta) = {float(C):.6f}  (cible {Ccible}) ; C*eta = {float(C*eta):.6f} ; "
          f"C <= cible : {C <= Ccible}")
    print("   g_j/eta =", [f"{float(g/eta):.6f}" for g in gs], " max g_j =", float(max(gs)), "(<= 1 requis)")
    # monotonie : Phi(x)/x^2 croissante => C(x) <= C(eta) pour x <= eta (verifie sur une grille rationnelle)
    ok = all(chaine(d, eta * Fr(i, 50))[2] / (eta * Fr(i, 50)) ** 2 <= C for i in range(1, 51))
    print("   C(x) <= C(eta) pour x = eta*i/50 :", ok)
