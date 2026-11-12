#!/usr/bin/env python3
r"""V2 : recalcul INDEPENDANT de c(t), c_F(t) et B(t) (methode differente de la v1 : representation de Schwinger
1/khat^2 = int_0^oo e^{-s khat^2} ds, noyau de la chaleur du reseau 1D = e^{-2s} I_n(2s) ; aucune integration en k).

  c(t)   = int d^4k/(2pi)^4 e^{i k0 t} kh1^2 (kh1^2 + kh2^2) / kh^2
         = int_0^oo ds  e^{-2s} I_t(2s) [ M2(s) G(s)^2 + M1(s)^2 G(s) ]
  c_F(t) = int d^4k/(2pi)^4 e^{i k0 t} (kh1^2 + kh2^2) / kh^2 = int_0^oo ds e^{-2s} I_t(2s) 2 M1(s) G(s)^2
avec G = e^{-2s} I_0(2s) = int dk/2pi e^{-s kh^2}, M1 = 2 e^{-2s}(I_0 - I_1) = int kh^2 e^{-s kh^2},
M2 = e^{-2s}(6 I_0 - 8 I_1 + 2 I_2) = int kh^4 e^{-s kh^2}.   (Y = F12(x) - F12(x+e1), une couleur.)
Haute precision (mpmath, 60 chiffres) : les differences I_0 - I_1, 6I_0 - 8I_1 + 2I_2 s'annulent en double precision.
Controles : c_F(0) = 1/2 exactement ; c(t) t^6 -> 8/pi^2 ; c_F(t) t^4 -> 1/pi^2 ; G, M1, M2 en s = 0 : 1, 2, 6.
Puis B(t) = (2/t) log(c(0)/c(t)).
"""
import json, time
import mpmath as mp
mp.mp.dps = 60

def G(s):  return mp.besseli(0, 2*s) * mp.e**(-2*s)
def M1(s): return 2*mp.e**(-2*s) * (mp.besseli(0, 2*s) - mp.besseli(1, 2*s))
def M2(s): return mp.e**(-2*s) * (6*mp.besseli(0, 2*s) - 8*mp.besseli(1, 2*s) + 2*mp.besseli(2, 2*s))
def Kt(t, s):
    # noyau temporel e^{-2s} I_t(2s) : aucune annulation ; pour t >= 2000 la serie de mpmath ne converge pas
    # (essai 1, job 20261111-031016-d827ab) : on utilise alors scipy.special.ive (double precision, relative ~1e-15).
    if t >= 2000:
        from scipy.special import ive
        return mp.mpf(float(ive(t, float(2*s))))
    return mp.e**(-2*s) * mp.besseli(t, 2*s)

def integrale(f, t):
    # points de coupure adaptes a l'echelle s ~ t^2 (le noyau temporel vaut ~ (4 pi s)^{-1/2} e^{-t^2/(4s)})
    T = max(1, t)
    pts = [0, mp.mpf(1)/4, 1, 4] + [mp.mpf(T)**2 * c for c in (mp.mpf(1)/64, mp.mpf(1)/16, mp.mpf(1)/4, 1, 4, 16, 64)] + [mp.inf]
    pts = sorted(set(pts))
    return mp.quad(f, pts, maxdegree=10)

def c_Y(t): return integrale(lambda s: Kt(t, s) * (M2(s)*G(s)**2 + M1(s)**2*G(s)), t)
def c_F(t): return integrale(lambda s: Kt(t, s) * 2*M1(s)*G(s)**2, t)

if __name__ == "__main__":
    t0 = time.time()
    out = {"controles_s0": [mp.nstr(G(0), 20), mp.nstr(M1(0), 20), mp.nstr(M2(0), 20)],
           "huit_sur_pi2": mp.nstr(8/mp.pi**2, 15), "un_sur_pi2": mp.nstr(1/mp.pi**2, 15), "lignes": []}
    s = c_Y(0)
    out["c0"] = mp.nstr(s, 20)
    out["cF0"] = mp.nstr(c_F(0), 20)
    print(json.dumps({"c0": out["c0"], "cF0": out["cF0"]}), flush=True)
    for t in [1, 2, 3, 5, 10, 20, 50, 100, 200, 1000, 2000, 10000]:
        c = c_Y(t); cf = c_F(t)
        B = 2*mp.log(s/c)/t
        out["lignes"].append({"t": t, "c": mp.nstr(c, 15), "c_t6": mp.nstr(c*mp.mpf(t)**6, 12),
                              "cF": mp.nstr(cf, 15), "cF_t4": mp.nstr(cf*mp.mpf(t)**4, 12),
                              "B": mp.nstr(B, 12), "log2_sur_B": mp.nstr(mp.log(2)/B, 8),
                              "B_asympt_12logt_0p6774": mp.nstr((12*mp.log(t) + 2*mp.log(s*mp.pi**2/8))/t, 12)})
        out["temps_s"] = round(time.time() - t0, 1)
        print(json.dumps(out["lignes"][-1]), flush=True)
    print(json.dumps(out, indent=1))
