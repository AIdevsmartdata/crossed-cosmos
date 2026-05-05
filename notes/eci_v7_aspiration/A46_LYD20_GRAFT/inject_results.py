"""Inject numerical chi^2 results from lyd20_pinned_results.json into
v75_section4.tex (replace placeholders). Run after fit completes."""
import json, sys

PATH = "/root/crossed-cosmos/notes/eci_v7_aspiration/A46_LYD20_GRAFT"

with open(f"{PATH}/lyd20_pinned_results.json") as f:
    data = json.load(f)

c_i = data["comparison"]["chi2_tau_i"]
c_LYD = data["comparison"]["chi2_tau_LYD"]
c_W1 = data["comparison"]["chi2_tau_W1"]
pen_i = data["comparison"]["penalty_tau_i_vs_LYD"]
pen_W1 = data["comparison"]["penalty_tau_W1_vs_LYD"]

# Build the chi^2 comparison table snippet
table_tex = f"""\\begin{{table}}[ht]
\\centering
\\begin{{tabular}}{{l c c c}}
\\toprule
Scenario & $\\tau$ & $\\chi^2_{{\\min}}$ (19 obs, 11 params) & Penalty vs LYD-best \\\\
\\midrule
(A) $\\tau=i$ pinned (this paper) & $0.00 + 1.00\\,i$ & {c_i:.2f} & {pen_i:.2f}$\\times$ \\\\
(B) LYD20 \\cite{{LYD20}} published joint best & $-0.21 + 1.52\\,i$ & {c_LYD:.2f} & 1.00 \\\\
(C) W1 attractor & $-0.19 + 1.00\\,i$ & {c_W1:.2f} & {pen_W1:.2f}$\\times$ \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{$\\chi^2$ comparison for the LYD20 unified $Q+L$ scaffold at three pinned values of $\\tau$. The penalty for fixing $\\tau=i$ is the structural-anchoring cost.}}
\\label{{tab:v75_chi2}}
\\end{{table}}
"""

with open(f"{PATH}/table_v75_chi2.tex", "w") as fh:
    fh.write(table_tex)
print(f"Wrote {PATH}/table_v75_chi2.tex")

# Patch the v75_section4.tex placeholders
with open(f"{PATH}/v75_section4.tex") as fh:
    tex = fh.read()
tex = tex.replace("\\providecommand{\\PenaltyTauI}{[NUMERICAL: see lyd20\\_pinned\\_results.json]}",
                  f"\\providecommand{{\\PenaltyTauI}}{{{pen_i:.2f}\\times}}")
tex = tex.replace("\\providecommand{\\PenaltyTauW}{[NUMERICAL: see lyd20\\_pinned\\_results.json]}",
                  f"\\providecommand{{\\PenaltyTauW}}{{{pen_W1:.2f}\\times}}")
with open(f"{PATH}/v75_section4.tex", "w") as fh:
    fh.write(tex)
print(f"Updated {PATH}/v75_section4.tex placeholders")

# Print verdict
print()
print(f"chi^2 summary:")
print(f"  tau = i pinned :  {c_i:.2f}")
print(f"  LYD20-best     :  {c_LYD:.2f}")
print(f"  W1 attractor   :  {c_W1:.2f}")
print(f"PENALTIES:")
print(f"  tau=i / LYD = {pen_i:.2f}x")
print(f"  W1*  / LYD = {pen_W1:.2f}x")
print()
if pen_i < 5:
    verdict = "GRAFT VIABLE -- penalty within A42 acceptance threshold"
elif pen_i < 20:
    verdict = "GRAFT MARGINAL -- structural cost flagged; consider Kahler extension (dMVP26)"
else:
    verdict = "GRAFT REJECTED -- penalty too high; consider W1 tau* attractor instead"
print(f"VERDICT: {verdict}")
