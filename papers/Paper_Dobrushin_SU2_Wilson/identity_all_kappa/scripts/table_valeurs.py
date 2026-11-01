#!/usr/bin/env python3
"""table_valeurs.py -- table (Arb, 20 chiffres) de D_ch(kappa) = E_kappa[x2^2] = I2/(kappa I1), de Delta, de 1/4 - D_ch et de la borne kappa^2/(96 Zb) (D7, tout kappa),
et verification (CALCULEE) de : D_ch decroissante (Delta > 0), 1/4 - D_ch >= kappa^2/(96 Zb), 1/4 - D_ch >= 0.0084 kappa^2 sur [0,4/3] seulement.
"""
import json, sys, hashlib
from fractions import Fraction
from flint import arb, ctx, fmpq
ctx.prec = 200

def aq(fr):
    fr = Fraction(fr)
    return arb(fmpq(fr.numerator, fr.denominator))

def main():
    out_path = sys.argv[1]
    ks = ["1/10", "1/2", "1", "4/3", "2", "3", "4", "5", "6", "8", "10", "20", "50", "100"]
    rows = []
    ok = True
    print("| kappa | D_ch = I2/(kappa I1) | 1/4 - D_ch | kappa^2/(96 Zb) | Delta | Delta*kappa (= -kappa^2 D_ch') |")
    print("|---|---|---|---|---|---|")
    for ks_ in ks:
        k = aq(Fraction(ks_))
        I1 = k.bessel_i(1); I2 = k.bessel_i(2)
        Zb = 2 * I1 / k
        m1 = I2 / I1
        D = m1 / k
        Delta = m1 * m1 + 4 * m1 / k - 1
        reste = arb(1) / 4 - D
        borne = k * k / (96 * Zb)
        c1 = bool(reste > borne)
        c2 = bool(Delta > 0)
        ok = ok and c1 and c2
        rows.append(dict(kappa=ks_, D_ch=D.str(15, radius=False), reste=reste.str(15, radius=False), borne=borne.str(10, radius=False), Delta=Delta.str(12, radius=False),
                         reste_ge_borne=c1, Delta_pos=c2))
        print(f"| {ks_} | {D.str(12, radius=False)} | {reste.str(10, radius=False)} | {borne.str(8, radius=False)} | {Delta.str(8, radius=False)} | {(Delta * k).str(8, radius=False)} |")
    # 0.0084 kappa^2 sur [0,4/3] : 1/(96 Zb(4/3)) >= 0.0084052
    k43 = aq(Fraction(4, 3)); Z43 = 2 * k43.bessel_i(1) / k43
    c3 = bool(1 / (96 * Z43) > arb("0.0084052"))
    ok = ok and c3
    print(f"1/(96 Zb(4/3)) = {(1 / (96 * Z43)).str(10, radius=False)} > 0.0084052 : {c3} (constante de D7, valable sur [0,4/3] seulement)")
    json.dump(dict(script_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(), lignes=rows, constante_0084_ok=c3, tout_ok=ok), open(out_path, 'w'), indent=1)
    print("VERDICT : " + ("TOUT_OK" if ok else "ECHEC"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
