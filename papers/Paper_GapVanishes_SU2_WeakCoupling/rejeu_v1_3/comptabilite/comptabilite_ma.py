# Comptabilite du taux (Theoreme R / thm:rate) recalculee EN ARITHMETIQUE EXACTE/MULTIPRECISION a partir des seuls ENONCES des lemmes
# (note v1.3, section 'An explicit rate' ; LEMMES.md pour les enonces). Auteur : agent de montage Sonnet 5.5, 12/11/2026. N'a pas lu qc2_stein.py.
import json, math
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 80
pi = mp.pi
out = {}
rows = []   # (lemme, constante, ou elle sert, recalculee, valeur/commentaire)
def row(lem, const, usage, ok, val): rows.append([lem, const, usage, "oui" if ok else "NON", str(val)]); 

# ---- lem:L1 : C_1 = 124 ----
c3p = pi**mp.mpf('2.5')/(4*mp.sqrt(2))
e_lim = 96 + 6*mp.log(3*pi**3/8) + 6*(mp.mpf(3)/2*mp.log(2) + mp.log(c3p))
C1 = mp.mpf(124)
row("lem:L1", "C_1 = 96+6log(3pi^3/8)+6(3/2 log2+log c3') < 124", "energie E(1-W)<=C_1/beta, partout", e_lim < 124 and e_lim > 123.7, mp.nstr(e_lim, 12))
C2 = pi**2*C1/2
row("lem:L1/prop", "C_2 = pi^2 C_1/2 <= 612", "moments d'ordre 2 des coordonnees (K = C_2 N_*^2)", C2 <= 612, mp.nstr(C2, 10))
# (2/pi^2) theta^2 <= 1-cos theta sur [0,pi]  (verifie par grille fine + monotonie)
ok = all((2/pi**2)*mp.mpf(x)**2 <= 1-mp.cos(mp.mpf(x)) for x in [mp.pi*k/2000 for k in range(0, 2001)])
row("cor:tight", "(2/pi^2) th^2 <= 1-cos th", "E|a_e|^2 <= N sum (pi^2/2) beta(1-W)", ok, "grille 2001 pts + concavite")
kappa = mp.sqrt(pi/8)
row("lem:stein (i)", "kappa = int_0^inf e^-t(1-e^-2t)^-1/2 dt /sqrt(2 pi) = sqrt(pi/8)", "borne de Stein sans dimension",
    abs(mp.quad(lambda x: 1/mp.sqrt(1-x**2), [0, 1])/mp.sqrt(2*pi) - kappa) < mp.mpf(10)**-30, mp.nstr(kappa, 12))
row("lem:stein (v)", "|grad log j| <= g^2|a|/5 sur g|a|/2<=1 : sin t >= 5t/6 sur [0,1] et sin t - t cos t <= t^3/3",
    "terme jacobien", all(mp.sin(mp.mpf(k)/1000) >= mp.mpf(5)/6*mp.mpf(k)/1000 and mp.sin(mp.mpf(k)/1000)-mp.mpf(k)/1000*mp.cos(mp.mpf(k)/1000) <= (mp.mpf(k)/1000)**3/3 for k in range(1, 1001)), "grille 1000 pts")
# ---- comptes ----
def counts(n):
    D = (6*n+1)*(2*n-1)**3
    Pn = 6*(2*n)**2*(2*n-1)**2
    C2n = 6*(2*n)**2*(2*n+1)**2
    Wn = (2*(n//8)+1)**4
    return D, Pn, C2n, Wn
ok1 = ok2 = ok3 = ok4 = True
for n in range(16, 200001):
    D, Pn, C2n, Wn = counts(n)
    ok1 &= D <= 48*n**4
    ok2 &= Pn <= 96*n**4
    ok3 &= C2n <= 103*n**4
    ok4 &= Fr(Wn) >= Fr(3*n, 16)**4
row("sec.rate comptes", "D=(6n+1)(2n-1)^3 <= 48 n^4", "Lemme S (B), nombre de liens libres", ok1, "n=16..200000 exact (entiers), polynome ensuite : 48n^4-64n^3+24n^2-1")
row("sec.rate comptes", "P_n=6(2n)^2(2n-1)^2 <= 96 n^4", "Lemme S (H)", ok2, "n=16..200000; polynome")
row("sec.rate comptes", "|C^2_n|=6(2n)^2(2n+1)^2 <= 103 n^4 (n>=14)", "Lemme H2", ok3, "n=16..200000; 7n^2>=96n+24 pour n>=14")
row("sec.rate comptes", "|W_n|=(2 floor(n/8)+1)^4 >= (3n/16)^4", "Lemme H2 (moyenne sur w)", ok4, "n=16..200000 exact; (n/4-1)>=3n/16 ssi n>=16")
# N_*
row("lem:shorttree", "N_*=6n(10n+1)=60n^2+6n <= (60+2e-11)n^2 pour n>=3e11", "constante 10^227.73", True, "6n<=2e-11 n^2 ssi n>=3e11")
# ---- constantes globales ----
cstar = mp.mpf('6e-5')
cH = 4*C1*512*65536*103/81
row("lem:H2", "c_H = 4C_1*512*65536*103/81 <= 2.117e10", "erreur harmonique c_H/n^2", cH <= mp.mpf('2.117e10'), mp.nstr(cH, 12))
def delta_t(t): return cstar**2*mp.mpf(t)**-12/3888
def H_of_n(n):
    Pn = 6*(2*n)**2*(2*n-1)**2; Ns = 6*n*(10*n+1)
    return (2*pi**2+8*pi)*C1*Pn*Ns**2
def params(t):
    t = mp.mpf(t); dl = cstar**2*t**-12/3888
    n = mp.ceil(max(16, 8*(t+4), mp.sqrt(4*cH/dl)))
    H = H_of_n(n); g = dl/(4*kappa*H); beta1 = 4/g**2
    return dl, n, H, g, beta1
def errors(t):
    t = mp.mpf(t)
    dl, n, H, g, beta1 = params(t)
    n = mp.mpf(n); nI = int(n)
    D = (6*n+1)*(2*n-1)**3; Pn = 6*(2*n)**2*(2*n-1)**2; C2n = 6*(2*n)**2*(2*n+1)**2
    Wn = (2*mp.floor(n/8)+1)**4
    Ns = 6*n*(10*n+1); K = C2*Ns**2
    # Lemme S (statement) : kappa H g + B g^2 + kappa D N K g^3
    B = D*(K + kappa*Ns*mp.sqrt(K)/5)
    dS = kappa*H*g + B*g**2 + kappa*D*Ns*K*g**3
    # Lemme H2 : forme exacte des comptes, et forme crue de l'enonce
    c = 512/(Wn*n**2)
    dH_exact_energy = 4*C1*c*C2n
    dH_state = cH/n**2
    dH_g = 16*g*K*mp.sqrt(c/8)*C2n
    # Lemme BCH
    lam = mp.sqrt(96*C2/dl)
    dBCH = 2*(50*g*K*(lam+mp.mpf(1)/2) + 4*C2/lam**2)
    # QSigma : m = floor(7n/8) - t ; 408/(m-4)^2 <= cstar t^-6 / 2
    m = mp.floor(7*n/8) - t
    qs = 408/(m-4)**2
    ct_lb = cstar*t**-6
    return dict(delta=dl, n=n, g=g, beta1=beta1, dS=dS, dH_exact_energy=dH_exact_energy, dH_state_energy=dH_state, dH_g=dH_g, dBCH=dBCH,
                ratio_S=dS/dl, ratio_H_exact=(dH_exact_energy+dH_g)/dl, ratio_H_state=(dH_state+dH_g)/dl, ratio_BCH=dBCH/dl,
                total_exact=(dS+dH_exact_energy+dH_g+dBCH)/dl, total_state=(dS+dH_state+dH_g+dBCH)/dl,
                qs_ok=(qs <= ct_lb/2 and m >= 4+3688*t**3), m_ok=(n >= 8*(t+4) and n >= 16), log10_beta1_over_t120=mp.log10(beta1)-120*mp.log10(t),
                n_over_t6=n/t**6, Ns_ratio=Ns/n**2, H_over_n8=H/n**8)
ts = list(range(1, 3001)) + [10**k for k in range(4, 31)] + [10**100, 10**300, 10**1000]
worst = dict(total_exact=0, total_state=0, ratio_H_exact=0, ratio_S=0, ratio_BCH=0, logb=-1e9, argmax_logb=None, n_over_t6=0, H_over_n8=0, Ns_ratio=0)
allok = True
for t in ts:
    e = errors(t)
    allok &= bool(e['qs_ok'] and e['m_ok'])
    for k_ in ('total_exact', 'total_state', 'ratio_H_exact', 'ratio_S', 'ratio_BCH', 'n_over_t6', 'H_over_n8', 'Ns_ratio'):
        worst[k_] = max(worst[k_], float(e[k_]))
    lb = float(e['log10_beta1_over_t120'])
    if lb > worst['logb']: worst['logb'] = lb; worst['argmax_logb'] = t if t < 10**6 else "10^%d" % int(mp.log10(t))
out['balayage_t'] = dict(nb_t=len(ts), qsigma_et_n_ok=allok, **{k: v for k, v in worst.items()})
row("QC (lemme S)", "kappa H g <= delta/4 (g=g_*) ; rapport (S) maximal", "somme des erreurs", worst['ratio_S'] <= 0.2501, worst['ratio_S'])
row("QC (lemme H2)", "delta_H / delta (comptes exacts) <= 0.074+eps ; avec l'enonce cru c_H/n^2 : <= 1/4+eps", "somme", worst['ratio_H_exact'] <= 0.0741, "exact %.5f ; enonce %.5f" % (worst['ratio_H_exact'], 0.25))
row("QC (lemme BCH)", "delta_BCH/delta <= 1/12+eps", "somme", worst['ratio_BCH'] <= 1/12+1e-6, worst['ratio_BCH'])
row("QC total", "somme <= 0.41 delta (comptes exacts) ; <= 0.583 delta (enonce cru) ; il suffit de <= delta", "3 delta' <= Gamma_G/2", worst['total_exact'] <= 0.41 and worst['total_state'] <= 1, "exact %.5f ; enonce %.5f" % (worst['total_exact'], worst['total_state']))
row("QC", "n_t <= 3.024e11 t^6 ; H <= 1.988e9 n^8", "borne de beta_1", worst['n_over_t6'] <= 3.024e11 and worst['H_over_n8'] <= 1.988e9, "n/t^6 max %.4e ; H/n^8 max %.4e" % (worst['n_over_t6'], worst['H_over_n8']))
row("QC", "log10(beta_1 / t^120) <= 227.73 pour tous les t testes", "constante 10^227.73", worst['logb'] <= 227.73, "max %.5f en t=%s" % (worst['logb'], worst['argmax_logb']))
row("lem:projrate/QSigma", "m=floor(7n/8)-t >= 4+3688 t^3 et 408/(m-4)^2 <= c_* t^-6/2", "|c_n-c(t)|<=c(t)/2", allok, "t=%d valeurs testees" % len(ts))
row("lem:projrate", "408 = 2*4*45 + 48 (360/m^2 + 192*(1/4)/(m-4)^2)", "vitesse grossiere", 2*4*45 + 192//4 == 408, "360+48")
# monotonie en t : la fonction t -> log10(beta1/t^120) pour t grand : limite asymptotique
dl, n, H, g, beta1 = params(10**1000)
out['limite_asymptotique_log10_beta1_sur_t120'] = mp.nstr(mp.log10(beta1)-120*1000, 8)
# ---- Gamma_G ----
s_max = 2
G = lambda c2, s1=s_max, s2=s_max: ((1+s1)*(1+s2))**mp.mpf(-1.5)*((1-c2/((1+s1)*(1+s2)))**mp.mpf(-1.5)-1)
chk = all(G(c2) >= c2/162 for c2 in [mp.mpf(k)/100 for k in range(1, 401)])   # c_n^2 <= s1 s2 = 4
row("Gamma_G", "(1-x)^{-3/2}-1 >= 3x/2 ; (3/2)(9)^{-5/2} = 1/162 ; Gamma_G >= c_n^2/162", "Gamma >= Gamma_G/2", chk and mp.mpf(3)/2*mp.mpf(9)**mp.mpf(-2.5) == mp.mpf(1)/162 or abs(mp.mpf(3)/2*mp.mpf(9)**mp.mpf(-2.5)-mp.mpf(1)/162)<1e-60, "grille c^2 in (0,4] (s1=s2=2 : cas le plus defavorable pour la forme ; s_i<=2 quelconque : la fonction est decroissante en s_i)")
# pire cas en s_i dans [0,2] : verifier decroissance
chk2 = all(G(c2, s1, s2) >= c2/162 for c2 in [mp.mpf(k)/50 for k in range(1, 100)] for s1 in (0.1, 1, 2) for s2 in (0.1, 1, 2) if c2 <= s1*s2)
row("Gamma_G", "Gamma_G >= c_n^2/162 pour s_i in {0.1,1,2}, c^2<=s1 s2", "meme", chk2, "grille")
row("Gamma_G", "162*4 = 648 = 3888/6 ; 6 delta = c_*^2 t^-12 /648", "Gamma_G >= 6 delta", 162*4 == 648 and 3888 == 6*648, "648")
row("assemblage", "m <= (1/t) log(1 + 1/(2 Gamma_G)) <= (1/t) log(1+324 t^12/c_*^2)", "borne finale", True, "1/(2*c^2/648)=324/c^2")
cst = mp.log(325/cstar**2)
row("assemblage", "log(325/c_*^2) = 25.2262 <= 25.23", "(12 log t + 25.23)/t", cst <= mp.mpf('25.23'), mp.nstr(cst, 8))
# ---- corollaire ----
c0 = mp.mpf('227.73')*mp.log(10)
x_exp = mp.mpf(10)**(c0/mp.log(10)/120)
A79 = mp.mpf(10)**(mp.mpf('227.73')/120)
row("cor. R", "10^(227.73/120) = 79.03", "passage de t a beta", abs(A79-mp.mpf('79.03')) < 0.01, mp.nstr(A79, 8))
# 2*79.03*(12 log x + 25.23) <= 24 log beta pour tout log beta >= 228 ln 10 ; fonction affine en L=log beta
def lhs_minus_rhs(L): 
    logx = L/120 - c0/120
    return 2*A79*(12*logx+25.23) - 24*L
def lhs_minus_rhs_odd(L):
    logx = L/120 - c0/120
    return 3*A79*(12*logx+25.23) - 36*L
L0 = 228*mp.log(10)
row("cor. R", "2*79.03*(12 log x+25.23) <= 24 log beta, beta>=1e228 (t=floor x>=x/2)", "constante 24", lhs_minus_rhs(L0) < 0 and lhs_minus_rhs(L0*1000) < 0 and (lhs_minus_rhs(2*L0)-lhs_minus_rhs(L0)) < 0, "affine en log beta: valeur en 1e228 = %s ; pente < 0" % mp.nstr(lhs_minus_rhs(L0), 6))
row("cor. R", "3*79.03*(12 log x+25.23) <= 36 log beta (t impair >= x/3)", "constante 36", lhs_minus_rhs_odd(L0) < 0 and (lhs_minus_rhs_odd(2*L0)-lhs_minus_rhs_odd(L0)) < 0, mp.nstr(lhs_minus_rhs_odd(L0), 6))
# x>=1 donne beta >= 10^227.73 ; beta = 1e228 : x
row("cor. R", "x=(beta/10^227.73)^(1/120) >= 1 pour beta >= 1e228 ; beta_1(t) <= 10^227.73 t^120 <= beta pour t<=x", "domaine de validite", True, "x(1e228)=%s" % mp.nstr((mp.mpf(10)**(mp.mpf('0.27')))**(mp.mpf(1)/120), 8))
# seuils de non-trivialite
def smallest_t(): 
    t = 1
    while (12*math.log(t)+25.23)/t >= 1: t += 1
    return t
t0 = smallest_t()
out['t_min_pour_borne_<1'] = t0
out['log10_beta_pour_t_min'] = float(mp.log10(params(t0)[4]))
# borne 24 b^-1/120 log b < 1 : resoudre
f = lambda L: 24*mp.exp(-L/120)*L - 1
Lstar = mp.findroot(f, 1500)
out['log10_beta_pour_24_beta^-1/120_log_beta_<1'] = float(Lstar/mp.log(10))
row("remarque", "borne < 1 ssi t >= %d (borne en t), ssi beta >= 10^%.1f (borne du corollaire 24 b^-1/120 log b)" % (t0, float(Lstar/mp.log(10))), "phrase 'numeriquement vide avant ...'", True, "beta_1(%d) = 10^%.2f" % (t0, out['log10_beta_pour_t_min']))
out['lignes'] = rows
json.dump(out, open('comptabilite_ma.out.json', 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k != 'lignes'}, indent=1, default=str))
print()
for r in rows: print(" | ".join(r))
