# Contrôle de la constante de QS (méthode de Stein) sur un cas à un lien : un lien libre, ses 6 plaquettes, agrafes = identité.
# P : densité radiale r^2 exp(-6 beta (1 - cos(g r/2))) j_g(r) sur r < 2pi/g ; Q = N(0, I/6) (E_0 = 3|a|^2).
# Borne de Stein : TV <= kappa * E_P |C^{1/2}(grad V - grad E_0)|, C = I/6, V = 6 beta (1 - cos(g r /2)) - log j_g(r).
import numpy as np, json
from math import pi, sqrt
kap = sqrt(pi/8)
res = []
for beta in [10, 30, 100, 300, 1000, 3000, 10000]:
    g = 2/np.sqrt(beta)
    rmax = 2*pi/g
    r = np.linspace(1e-9, rmax*(1-1e-12), 2000001)
    t = g*r/2
    j = (np.sin(t)/t)**2
    p = r**2*np.exp(-6*beta*(1-np.cos(t)))*j
    p /= np.trapezoid(p, r)
    q = r**2*np.exp(-3*r**2); q /= np.trapezoid(q, r)
    tv = 0.5*np.trapezoid(np.abs(p-q), r)          # les deux lois sont radiales : TV radiale = TV dans R^3
    gradV = 6*beta*(g/2)*np.sin(t) + g*(1/t - 1/np.tan(t))   # dV/dr ; -d log j / dr = g (1/t - cot t)
    gradE0 = 6*r
    stein = kap*np.trapezoid(p*np.abs(gradV-gradE0)/np.sqrt(6), r)
    res.append({"beta": beta, "TV_exact": tv, "Stein_bound": stein, "ratio": stein/tv, "beta*TV": beta*tv})
print(json.dumps(res))
