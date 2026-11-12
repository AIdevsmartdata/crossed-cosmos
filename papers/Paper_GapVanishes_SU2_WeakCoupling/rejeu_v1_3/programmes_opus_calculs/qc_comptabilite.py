# Lemme QC : vérification indépendante de la comptabilité (arithmétique en mpmath, 50 chiffres). Bac à sable seulement.
import mpmath as mp, json
mp.mp.dps = 50
cstar = mp.mpf('6e-5'); C1 = mp.mpf(124); C2 = mp.pi**2*C1/2
out = {"C2": float(C2)}
assert C2 <= 612
rows = []
for t in [1, 2, 3, 10, 100, 1000]:
    t = mp.mpf(t)
    delta = cstar**2 * t**-12 / 3888
    # n
    W = lambda n: (2*mp.floor(n/8)+1)**4
    cH = mp.mpf(512)*65536*103*1225/81
    n = mp.ceil(max(16, 8*(t+4), mp.sqrt(4*cH/delta)))
    # comptes exacts à ce n
    m_ = 2*n-1
    D = (6*n+1)*(2*n-1)**3; S = (2*n+1)**4-(2*n-1)**4; J = 4*S; Nn = D+J
    Pn = 6*(2*n)**2*(2*n-1)**2; Cn = 6*(2*n)**2*(2*n+1)**2; Wn = W(n)
    Ns = 6*n*(10*n+1)
    checks = {"D<=48n4": D <= 48*n**4, "Nn<=65n4": Nn <= 65*n**4, "Pn<=96n4": Pn <= 96*n**4, "Cn<=103n4": Cn <= 103*n**4,
              "Wn>=(3n/16)^4": Wn >= (3*n/16)**4, "Ns<=61n2": Ns <= 61*n**2}
    R2 = mp.mpf(10)**7 * n**4 * Ns**2 / delta; R = mp.sqrt(R2)
    Lam = mp.mpf('5.92e6') * n**4 / delta
    Mp2 = 168*C2*Ns**2/delta; Mp = mp.sqrt(Mp2)
    g = delta**mp.mpf(2.5) / (mp.mpf('5.677e16') * n**12)
    beta1 = 4/g**2
    CE = 2*C2 + 32*g**2*R**4
    eps = 4*g*R2*mp.sqrt(Pn*Lam) + 8*Pn*g**2*R**4 + D*g**2*R2/6
    T = ((2*D+4*Nn+J)*C2*Ns**2/R2 + 8*Ns**2*Cn*CE/R2 + (2*Pn+4*Cn)*CE/Lam
         + 12*D*mp.e**(-R2/(24*Ns**2)) + 2*mp.e**(-Lam/16))
    dQS = eps + T
    muG = Nn*C2*Ns**2/R2
    dH = muG + 512*Cn*CE/(Wn*n**2)          # forme exacte (256 r |C_n^2| C_E / (|W_n| n^2)), r = 2
    dBCH = 1125*g*Mp**3 + 14*C2*Ns**2/Mp2
    tot = dQS + dH + dBCH
    mm = mp.floor(7*n/8) - t
    sig_ok = 408/(mm-4)**2 <= cstar*t**-6/2
    conds = {"gR<=1/2": g*R <= mp.mpf(1)/2, "32g2R4<=1": 32*g**2*R**4 <= 1, "gM'<=1": g*Mp <= 1, "Lam>=24D": Lam >= 24*D,
             "n>=8(t+4)": n >= 8*(t+4), "QSigma": sig_ok, "beta>=16": beta1 >= 16}
    mbound = mp.log(1 + 324*t**12/cstar**2)/t
    rows.append({"t": int(t), "n": mp.nstr(n, 6), "log10_beta1": float(mp.log10(beta1)),
                 "log10_beta1_minus_204log10t": float(mp.log10(beta1) - 204*mp.log10(t)),
                 "eps/delta": float(eps/delta), "T/delta": float(T/delta), "dH/delta": float(dH/delta),
                 "dBCH/delta": float(dBCH/delta), "total/delta": float(tot/delta), "all_counts": all(checks.values()),
                 "all_conds": all(conds.values()), "conds": {k: bool(v) for k, v in conds.items()}, "m_bound": float(mbound)})
out["rows"] = rows
# corollaire : beta >= beta0, t = floor((beta/beta*)^(1/204)), m <= C beta^(-1/204) log beta
bstar = mp.mpf(10)**mp.mpf('374.53')
for lb in [375, 400, 500, 1000, 3000]:
    beta = mp.mpf(10)**lb
    t = mp.floor((beta/bstar)**(mp.mpf(1)/204))
    mb = mp.log(1 + 324*t**12/cstar**2)/t
    out.setdefault("corollaire", []).append({"log10beta": lb, "t": mp.nstr(t, 8), "m_bound": mp.nstr(mb, 6),
                                            "13*beta^(-1/204)*log(beta)": mp.nstr(13*beta**(-mp.mpf(1)/204)*mp.log(beta), 6)})
print(json.dumps(out, indent=0))
