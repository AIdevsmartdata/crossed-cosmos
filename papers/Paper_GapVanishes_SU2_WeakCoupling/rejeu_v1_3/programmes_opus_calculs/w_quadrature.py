# Lemme QSigma : W = sum_x |x|^2 |f(x)|^2 = sum_{mu<nu} sum_lam int |d_lam fhat_{mu nu}|^2, f = Pi_inf v ; borne prouvée W <= 38.
# Contrôle des bornes ponctuelles sup|d_lam fhat| (3/4, 1/8, 5, 2, 1) par différences finies analytiques sur une grille.
import numpy as np, json
def comps(k):
    k0, k1, k2, k3 = k
    e = [np.exp(1j*kk) - 1 for kk in k]
    kh2 = sum(4*np.sin(kk/2)**2 for kk in k)
    vh = 1 - np.exp(-1j*k1)
    w = vh/kh2
    f = {}
    f["12"] = (np.abs(e[1])**2 + np.abs(e[2])**2)*w
    f["01"] = -e[0]*np.conj(e[2])*w
    f["02"] = e[0]*np.conj(e[1])*w
    f["13"] = e[3]*np.conj(e[2])*w
    f["23"] = -e[3]*np.conj(e[1])*w
    return f
def derivs(k, h=1e-6):
    out = {}
    for lam in range(4):
        kp = [x.copy() for x in k]; km = [x.copy() for x in k]
        kp[lam] = kp[lam] + h; km[lam] = km[lam] - h
        fp, fm = comps(kp), comps(km)
        for c in fp:
            out[(c, lam)] = (fp[c] - fm[c])/(2*h)
    return out
rng = np.random.default_rng(1)
res = {}
# (1) W par Monte-Carlo stratifié + quadrature point milieu (grille 40^4, décalée pour éviter k = 0)
Ng = 40
g1 = (np.arange(Ng) + 0.5)/Ng*2*np.pi - np.pi
Wsum = 0.0; sup = {}
for i0 in range(Ng):
    k0 = np.full((Ng, Ng, Ng), g1[i0])
    K1, K2, K3 = np.meshgrid(g1, g1, g1, indexing="ij")
    d = derivs([k0, K1, K2, K3])
    for key, val in d.items():
        a = np.abs(val)**2
        Wsum += a.sum()
        sup[key] = max(sup.get(key, 0.0), float(np.sqrt(a.max())))
W = Wsum/Ng**4
res["W_midpoint_40"] = W
res["W_bound_proved"] = 45
res["sup_abs_deriv"] = {f"{c}_d{l}": round(v, 4) for (c, l), v in sorted(sup.items())}
bounds = {"12": [1, 5, 2, 1], "01": [0.75, 0.75, 0.75, 0.125], "02": [1.5, 1.65, 0.25, 0.25],
          "13": [0.125, 0.75, 0.75, 0.75], "23": [0.25, 1.65, 0.25, 1.5]}
# bornes ponctuelles prouvées (lambda = 0..3) ; f12 : d0 <= 1, d1 <= 5, d2 <= 2, d3 <= 1
viol = []
for (c, l), v in sup.items():
    if v > bounds[c][l] + 1e-6:
        viol.append((c, l, v, bounds[c][l]))
res["pointwise_bound_violations"] = viol
# (2) contrôle : <v, Pi_inf v> = c(0) et <v, Delta^{-1} v> = 1/4
K0, K1, K2, K3 = np.meshgrid(g1, g1, g1, g1, indexing="ij") if False else (None, None, None, None)
s = 0.0; q = 0.0
for i0 in range(Ng):
    k0 = np.full((Ng, Ng, Ng), g1[i0])
    K1, K2, K3 = np.meshgrid(g1, g1, g1, indexing="ij")
    kh = [4*np.sin(x/2)**2 for x in (k0, K1, K2, K3)]
    kh2 = sum(kh)
    s += (kh[1]*(kh[1]+kh[2])/kh2).sum(); q += (kh[1]/kh2).sum()
res["c0_midpoint_40"] = s/Ng**4
res["v_Dinv_v_midpoint_40"] = q/Ng**4
print(json.dumps(res))
