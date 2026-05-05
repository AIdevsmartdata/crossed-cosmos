"""A62 — final headline candidates with full PDG context."""
from mpmath import mp, mpf, sqrt, pi, fabs

mp.dps = 60

a1, a2, a3, a4 = mpf(1)/10, mpf(1)/12, mpf(1)/24, mpf(1)/60

PDG = {
    "|V_us|":          (mpf("0.22501"),    mpf("0.00068")),
    "|V_cb|":          (mpf("0.04183"),    mpf("0.00079")),
    "|V_ub|":          (mpf("0.003820"),   mpf("0.00020")),
    "|V_td|":          (mpf("0.00858"),    mpf("0.00026")),
    "|V_tb|":          (mpf("1.0140"),     mpf("0.0290")),
    "|V_cb|^2":        (mpf("0.04183")**2, 2*mpf("0.04183")*mpf("0.00079")),
    "|V_ub|^2":        (mpf("0.003820")**2, 2*mpf("0.003820")*mpf("0.00020")),
    "|V_td|^2":        (mpf("0.00858")**2, 2*mpf("0.00858")*mpf("0.00026")),
    "|V_tb|^2":        (mpf("1.0140")**2, 2*mpf("1.0140")*mpf("0.0290")),
    "|V_us|^2+|V_cb|^2":(mpf("0.22501")**2+mpf("0.04183")**2,
                         sqrt((2*mpf("0.22501")*mpf("0.00068"))**2
                              + (2*mpf("0.04183")*mpf("0.00079"))**2)),
    "|V_ub/V_cb|":     (mpf("0.003820")/mpf("0.04183"),
                         (mpf("0.003820")/mpf("0.04183"))*
                         sqrt((mpf("0.00020")/mpf("0.003820"))**2 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_cb|":     (mpf("0.00858")/mpf("0.04183"),
                         (mpf("0.00858")/mpf("0.04183"))*
                         sqrt((mpf("0.00026")/mpf("0.00858"))**2 + (mpf("0.00079")/mpf("0.04183"))**2)),
    "|V_td/V_ts|":     (mpf("0.2050"), mpf("0.0070")),
    "J_CKM":           (mpf("3.18e-5"), mpf("0.15e-5")),
}


def show(name, formula_str, pred, target):
    val, sig = PDG[target]
    rel = float(fabs(pred - val) / fabs(val)) * 100
    sig_d = float(fabs(pred - val) / sig)
    line = (f"  {name:<28} = {formula_str:<30} = {float(pred):.10g}  "
            f"vs PDG {target} = {float(val):.6g} ({float(sig):.2e})  "
            f"rel={rel:.4f}%  sigma={sig_d:.4f}")
    print(line)
    return {"name": name, "formula": formula_str,
            "value": float(pred), "target": target,
            "PDG": float(val), "PDG_sigma": float(sig),
            "rel_err_pct": rel, "sigma_dist": sig_d}


print("=" * 110)
print("A62 — HEADLINE Q(i)-Damerell-ladder CKM candidates (parsimonious q + small-degree expression)")
print("=" * 110)
print()
print("--- A17 baseline (re-evaluation with current PDG values) ---")
out = []
out.append(show("A17 |V_us| = (9/4)*a1",       "9/40",          mpf(9)/4 * a1, "|V_us|"))
out.append(show("A17 |V_cb|^2 = a1*a4",        "1/600",         a1*a4,         "|V_cb|^2"))
print()
print("[ A17's 1/600 hit no longer survives <0.1sigma vs PDG-2024 |V_cb|=0.04183;")
print("  it sat fine vs HFLAV-2024 |V_cb|=0.04085 used in A17.  See replacement (7/4)*a1^3 below. ]")
print()
print("--- A62 NEW headline candidates ---")
out.append(show("|V_ub| = (6/5)*a1^2/pi",      "6/(500*pi)",    mpf(6)/5 * a1**2 / pi, "|V_ub|"))
out.append(show("|V_cb|^2 = (7/4)*a1^3",       "7/4000",        mpf(7)/4 * a1**3,       "|V_cb|^2"))
out.append(show("|V_td|^2 = 2*a2^2*a4/pi",     "1/(4320*pi)",   mpf(2) * a2**2 * a4 / pi, "|V_td|^2"))
out.append(show("|V_td| = (1/2)*a3^2*pi^2",   "pi^2/1152",      mpf(1)/2 * a3**2 * pi**2, "|V_td|"))
out.append(show("|V_ub|^2 = a4^3*pi",         "pi/216000",      a4**3 * pi,             "|V_ub|^2"))
out.append(show("J_CKM = (3/5)*a1^2*a4/pi",   "1/(100000*pi)",  mpf(3)/5 * a1**2 * a4 / pi, "J_CKM"))
out.append(show("|V_us|^2+|V_cb|^2 = a4*pi",  "pi/60",          a4 * pi,                "|V_us|^2+|V_cb|^2"))
out.append(show("|V_us|^2+|V_cb|^2 = (22/7)*a4","11/210",       mpf(22)/7 * a4,         "|V_us|^2+|V_cb|^2"))
out.append(show("|V_tb|^2 = (5/4)*a2*pi^2",   "5*pi^2/48",     mpf(5)/4 * a2 * pi**2, "|V_tb|^2"))

print()
print("--- pure-rational Q(i) hits (most structurally clean: q in tiny denominators) ---")
out.append(show("|V_us| = (9/4)*a1",          "9/40",          mpf(9)/4 * a1,           "|V_us|"))
out.append(show("|V_td/V_cb| = (16/13)*a4/a1","8/39",          mpf(16)/13 * a4 / a1,    "|V_td/V_cb|"))
out.append(show("|V_us|^2+|V_cb|^2 (22/7)*a4","11/210",        mpf(22)/7 * a4,          "|V_us|^2+|V_cb|^2"))

print()
print("--- ratios ---")
out.append(show("|V_ub/V_cb| = (4/3)*a2^2*pi^2","pi^2/108",     mpf(4)/3 * a2**2 * pi**2, "|V_ub/V_cb|"))
out.append(show("|V_td/V_ts| = (11/12)*a1*sqrt(5)","11*sqrt5/120", mpf(11)/12 * a1 * sqrt(5), "|V_td/V_ts|"))

# Save
import json
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/A62_CKM_SYSTEMATIC/ckm_headline.json', 'w') as fh:
    json.dump({
        "metadata": {"agent": "A62", "mp_dps": int(mp.dps)},
        "candidates": out,
    }, fh, indent=2, default=str)
print("\nWritten ckm_headline.json")
