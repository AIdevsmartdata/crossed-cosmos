"""A62 — verify the top-ranked hits explicitly + check what A17 found."""
from mpmath import mp, mpf, sqrt, pi, fabs

mp.dps = 60

# K=Q(i) Damerell ladder
a1, a2, a3, a4 = mpf(1)/10, mpf(1)/12, mpf(1)/24, mpf(1)/60

PDG = {
    "|V_us|":           (mpf("0.22501"),    mpf("0.00068")),
    "|V_cb|":           (mpf("0.04183"),    mpf("0.00079")),
    "|V_ub|":           (mpf("0.003820"),   mpf("0.00020")),
    "|V_td|":           (mpf("0.00858"),    mpf("0.00026")),
    "|V_tb|":           (mpf("1.0140"),     mpf("0.0290")),
    "|V_cb|^2":         (mpf("0.04183")**2, 2 * mpf("0.04183") * mpf("0.00079")),
    "|V_ub|^2":         (mpf("0.003820")**2, 2 * mpf("0.003820") * mpf("0.00020")),
    "|V_td|^2":         (mpf("0.00858")**2, 2 * mpf("0.00858") * mpf("0.00026")),
    "|V_tb|^2":         (mpf("1.0140")**2,  2 * mpf("1.0140") * mpf("0.0290")),
    "|V_ub/V_cb|":      (mpf("0.003820")/mpf("0.04183"),
                          (mpf("0.003820")/mpf("0.04183"))
                          * sqrt((mpf("0.00020")/mpf("0.003820"))**2
                                 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_cb|":      (mpf("0.00858")/mpf("0.04183"),
                          (mpf("0.00858")/mpf("0.04183"))
                          * sqrt((mpf("0.00026")/mpf("0.00858"))**2
                                 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_ts|":      (mpf("0.2050"),     mpf("0.0070")),
    "|V_us|*|V_cb|":    (mpf("0.22501")*mpf("0.04183"),
                          mpf("0.22501")*mpf("0.04183")
                          * sqrt((mpf("0.00068")/mpf("0.22501"))**2
                                 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_us|^2+|V_cb|^2": (mpf("0.22501")**2 + mpf("0.04183")**2,
                          sqrt((2*mpf("0.22501")*mpf("0.00068"))**2
                               + (2*mpf("0.04183")*mpf("0.00079"))**2)),
    "J_CKM":            (mpf("3.18e-5"),    mpf("0.15e-5")),
}


def report(name, expr_str, pred, target_key):
    val, sig = PDG[target_key]
    rel = float(fabs(pred - val) / fabs(val)) * 100
    sigma = float(fabs(pred - val) / sig)
    print(f"  {name:<32} = {expr_str:<28} = {float(pred):>16.10g}  vs  "
          f"{target_key}={float(val):>10.6g}({float(sig):>9.2e})  "
          f"rel={rel:.4f}%  sigma={sigma:.4f}")


print("=" * 100)
print("A62 — VERIFICATION OF TOP HITS  (mp.dps=60)")
print("=" * 100)

# A17 reference (pure-alpha)
print("\n--- A17 reference ---")
report("A17 |V_us|", "(9/4)*a1", mpf(9)/4 * a1, "|V_us|")
report("A17 |V_cb|^2 (=a1*a4)", "a1*a4", a1*a4, "|V_cb|^2")
report("A17 |V_cb| (=sqrt(a1*a4))", "sqrt(a1*a4)", sqrt(a1*a4), "|V_cb|")

# Top irrational (pi-involving)
print("\n--- Top irrational (pi/sqrt-involving) ---")
report("|V_ub| (6/5)*a1^2/pi", "6/(500*pi)", mpf(6)/5 * a1**2 / pi, "|V_ub|")
report("|V_tb|^2 (5/2)*a3*pi^2", "5*pi^2/48", mpf(5)/2 * a3 * pi**2, "|V_tb|^2")
report("|V_us|^2+|V_cb|^2 (4/9)*a2*sqrt2", "sqrt2/27", mpf(4)/9 * a2 * sqrt(2), "|V_us|^2+|V_cb|^2")
report("|V_td/V_ts| (11/12)*a1*sqrt5", "11*sqrt5/120", mpf(11)/12 * a1 * sqrt(5), "|V_td/V_ts|")
report("|V_cb|^2 (19/6)*a3^2/pi", "19/(3456*pi)", mpf(19)/6 * a3**2 / pi, "|V_cb|^2")

# Pure-alpha extra
print("\n--- Pure-alpha simplest per target ---")
report("|V_td/V_cb| (16/13)*a4/a1", "8/39", mpf(16)/13 * a4 / a1, "|V_td/V_cb|")
report("|V_us|^2+|V_cb|^2 (22/7)*a4", "11/210", mpf(22)/7 * a4, "|V_us|^2+|V_cb|^2")
report("|V_ub| (11/5)*a3^2", "11/2880", mpf(11)/5 * a3**2, "|V_ub|")
report("|V_cb|^2 (21/2)*a1^2*a4", "7/4000", mpf(21)/2 * a1**2 * a4, "|V_cb|^2")
report("|V_td|^2 (14/11)*a2*a3*a4", "7/95040", mpf(14)/11 * a2 * a3 * a4, "|V_td|^2")
report("|V_ub|^2 (1/19)*a4^2", "1/68400", mpf(1)/19 * a4**2, "|V_ub|^2")

# Special: |V_us|^2 + |V_cb|^2 = first row deficit / unitarity
# 22/7 is the famous pi approximation. Check (1/pi) * a4 vs target:
print("\n--- pi-related coincidences ---")
report("|V_us|^2+|V_cb|^2 a4*pi", "pi/60", a4 * pi, "|V_us|^2+|V_cb|^2")
report("|V_us|^2+|V_cb|^2 (22/7)*a4 vs pi*a4", "11/210 vs pi/60",
       mpf(22)/7 * a4, "|V_us|^2+|V_cb|^2")
print(f"      Ratio (22/7)/(pi) = {float(mpf(22)/7 / pi):.10f}  (= ~1.00040)")

# |V_tb|^2 = (5/2)*a3*pi^2 = 5*pi^2/48 -- this is significant since pi^2 = 6*zeta(2)
# Also = (15/1)*a2^2*pi^2 -- equivalent. Check both:
print("\n--- |V_tb|^2 alternative forms ---")
report("|V_tb|^2 (5/4)*a2*pi^2", "5*pi^2/48", mpf(5)/4 * a2 * pi**2, "|V_tb|^2")
report("|V_tb|^2 (5/2)*a3*pi^2", "5*pi^2/48", mpf(5)/2 * a3 * pi**2, "|V_tb|^2")
report("|V_tb|^2 (15/1)*a2^2*pi^2", "5*pi^2/48", mpf(15) * a2**2 * pi**2, "|V_tb|^2")
# All equal! 5*pi^2/48 = 5/4 * 1/12 * pi^2 = 5/2 * 1/24 * pi^2 = 15 * 1/144 * pi^2
print(f"  Check: 5*pi^2/48 = {float(5 * pi**2 / 48):.10f}")
print(f"  Note |V_tb|^2 PDG ~ 1.014^2 = {float(mpf('1.014')**2):.6f} -- but unitarity says |V_tb|=1.")
print("   The PDG value comes from FCC top unitarity fits; pure SM unitarity gives |V_tb|^2 = 1 - |V_td|^2 - |V_ts|^2.")

# Compute SM unitarity prediction for |V_tb|^2:
Vtd = mpf("0.00858")
Vts = mpf("0.04183")  # |V_ts| ~ |V_cb|
Vtb_unit = sqrt(1 - Vtd**2 - Vts**2)
print(f"   SM unitarity |V_tb| = sqrt(1 - |V_td|^2 - |V_ts|^2) = {float(Vtb_unit):.6f}")
print(f"   SM unitarity |V_tb|^2 = {float(Vtb_unit**2):.6f}")
print(f"   5*pi^2/48 = {float(5*pi**2/48):.6f}  -- DOES NOT MATCH unitarity (1.014 PDG is direct top decay)")

# |V_ub| more explicit verification
print("\n--- |V_ub| ladder hit ---")
val = mpf(6)/5 * a1**2 / pi
print(f"  |V_ub| = (6/5) * a1^2 / pi = (6/5) * (1/100) / pi = 6/(500*pi)")
print(f"        = {float(val):.10f}")
print(f"  PDG    = {float(PDG['|V_ub|'][0]):.10f} ± {float(PDG['|V_ub|'][1]):.6f}")
print(f"  rel err = {float(fabs(val - PDG['|V_ub|'][0])/PDG['|V_ub|'][0])*100:.4f}%")
print(f"  sigma   = {float(fabs(val - PDG['|V_ub|'][0])/PDG['|V_ub|'][1]):.4f}")
print(f"  Equivalently: 6/(500*pi) = 3/(250*pi)")

# Cross-K test for the top irrational hits at |V_ub| = 6/(500*pi)
print("\n--- |V_ub| cross-K test for (6/5)*alpha_1^2/pi ---")
# Need alpha_1 at each K (load from json)
import json
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/A62_CKM_SYSTEMATIC/ckm_hits.json') as fh:
    d = json.load(fh)
# We need alpha tables. The json saved alpha_Qi but not at other K.
# We need to recompute. Let's just import from the JSON cross_K_results which
# has the (6/5)*a1*a1*pi^-1 hit:
target = "|V_ub|"
for row in d['cross_K_results']:
    if row['CKM_target'] == target and row['expr_label'] == 'a1*a1*pi^-1' and row['q'] == '6/5':
        print(f"  expr: a1*a1*pi^-1, q=6/5")
        for b in row['by_K']:
            print(f"    {b['K']:<14}  pred={float(b['pred']):.6e}  rel={b['rel_err']*100:.2f}%  sigma={b['sigma_dist']:.2f}")
        break

# Cross-K for |V_tb|^2 hit
print("\n--- |V_tb|^2 cross-K test for (5/4)*alpha_2*pi^2 ---")
for row in d['cross_K_results']:
    if row['CKM_target'] == "|V_tb|^2" and row['expr_label'] == 'a2*pi^2' and row['q'] == '5/4':
        for b in row['by_K']:
            print(f"    {b['K']:<14}  pred={float(b['pred']):.6e}  rel={b['rel_err']*100:.2f}%  sigma={b['sigma_dist']:.2f}")
        break
