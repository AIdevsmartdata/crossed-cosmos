# Lemme QC, version 2 (QS par la méthode de Stein). Arithmétique mpmath 50 chiffres. Bac à sable seulement.
import mpmath as mp, json
mp.mp.dps = 50
cstar = mp.mpf('6e-5'); C1 = mp.mpf(124); C2 = mp.pi**2*C1/2; kap = mp.sqrt(mp.pi/8)
out = {"C2": float(C2), "kappa": float(kap), "(2pi^2+8pi)C1": float((2*mp.pi**2+8*mp.pi)*C1)}
cH = 4*C1*mp.mpf(512)*65536*103/81
out["c_H"] = float(cH)
rows = []
for t in [1, 2, 3, 10, 100, 1000]:
    t = mp.mpf(t)
    delta = cstar**2*t**-12/3888
    n = mp.ceil(max(16, 8*(t+4), mp.sqrt(4*cH/delta)))
    D = (6*n+1)*(2*n-1)**3; S = (2*n+1)**4-(2*n-1)**4; J = 4*S; Nn = D+J
    Pn = 6*(2*n)**2*(2*n-1)**2; Cn = 6*(2*n)**2*(2*n+1)**2; Wn = (2*mp.floor(n/8)+1)**4
    Ns = 6*n*(10*n+1); K = C2*Ns**2
    H = (2*mp.pi**2+8*mp.pi)*C1*Pn*Ns**2
    B = D*(K + kap*Ns*mp.sqrt(K)/5)
    g = delta/(4*kap*H)
    beta1 = 4/g**2
    dQS = kap*H*g + B*g**2 + kap*D*Ns*K*g**3
    c = 512/(Wn*n**2)
    dH = 2*c*Cn*2*C1 + 16*g*K*mp.sqrt(c/8)*Cn
    lam = mp.sqrt(96*C2/delta)
    dBCH = 2*(50*g*K*(lam+mp.mpf(1)/2) + 4*C2/lam**2)
    tot = dQS + dH + dBCH
    mm = mp.floor(7*n/8) - t
    conds = {"n>=8(t+4)": n >= 8*(t+4), "QSigma": 408/(mm-4)**2 <= cstar*t**-6/2, "beta>=2": beta1 >= 2,
             "counts": (D <= 48*n**4) and (Nn <= 65*n**4) and (Pn <= 96*n**4) and (Cn <= 103*n**4) and (Wn >= (3*n/16)**4) and (Ns <= 61*n**2)}
    rows.append({"t": int(t), "n": mp.nstr(n, 6), "log10_beta1": float(mp.log10(beta1)),
                 "log10_beta1_minus_120log10t": float(mp.log10(beta1) - 120*mp.log10(t)),
                 "dQS/delta": float(dQS/delta), "dH/delta": float(dH/delta), "dBCH/delta": float(dBCH/delta),
                 "total/delta": float(tot/delta), "all_conds": all(conds.values()),
                 "m_bound": float(mp.log(1 + 324*t**12/cstar**2)/t)})
out["rows"] = rows
bstar = max(mp.mpf(10)**mp.mpf(r["log10_beta1_minus_120log10t"]) for r in rows)
out["log10_beta_star"] = float(mp.log10(bstar))
cor = []
for lb in [229, 240, 300, 500, 1000, 3000]:
    beta = mp.mpf(10)**lb
    t = mp.floor((beta/bstar)**(mp.mpf(1)/120))
    if t < 1:
        cor.append({"log10beta": lb, "t": 0}); continue
    mb = mp.log(1 + 324*t**12/cstar**2)/t
    cor.append({"log10beta": lb, "t": mp.nstr(t, 8), "m_bound": mp.nstr(mb, 6),
                "24*beta^(-1/120)*log(beta)": mp.nstr(24*beta**(-mp.mpf(1)/120)*mp.log(beta), 6),
                "ok": bool(mb <= 24*beta**(-mp.mpf(1)/120)*mp.log(beta))})
out["corollaire"] = cor
print(json.dumps(out, indent=0))
