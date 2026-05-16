\\ HSH-nuDM STRICT v2: odd torsion detected as Z/n with n having odd prime factor
\\ Per Rubin 1991 + memory VINDICATED: Cl 2-group iff ALL cyclic factors are powers of 2

\\ Helper: is_2power(n) = n is a power of 2
is_2power(n) = if(n==1, 1, if(n%2==1, 0, is_2power(n/2)));

\\ Helper: has_odd_torsion = ANY cyclic factor n has odd prime divisor (i.e. n is not a 2-power)
has_odd_tor(cyc) = sum(j=1, #cyc, if(is_2power(cyc[j]), 0, 1)) > 0;

print("=== HSH-nuDM STRICT v2 (correct odd-torsion test) ===");
print("D | K_disc | Cl_cyc | h_K | rk_2 | |Cl[2]| | has_odd | rats_strict | nu_strict");

D_all = [-3, -4, -7, -8, -11, -19, -43, -67, -163, -15, -20, -24, -35, -40, -51, -52, -88, -91, -115, -123, -148, -187, -232, -235, -267, -403, -427, -23, -31, -59, -83, -107, -139, -211, -283, -307, -331, -379, -499, -547, -643, -883, -907];

for(i=1, #D_all, D = D_all[i]; K_disc = quaddisc(D); Cl = quadclassunit(K_disc); cyc = Cl[2]; h = Cl[1]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); cl2 = prod(j=1, #cyc, if(cyc[j]%2==0, 2, 1)); ot = has_odd_tor(cyc); rats = if(ot, 0, cl2); nu = if(rk_2==0, "DIRAC", if(ot, "DIRAC-strict-Rubin", "MAJORANA")); print(D, " | ", K_disc, " | ", cyc, " | h=", h, " | rk_2=", rk_2, " | |Cl[2]|=", cl2, " | odd_tor=", ot, " | rats=", rats, " | ", nu));

print("");
print("=== Anchor cross-check (memory VINDICATED 5 anchors) ===");
D_anchors = [-23, -260, -420, -924, -5460];
exp_rats = [0, 4, 8, 0, 16];
for(i=1, #D_anchors, D = D_anchors[i]; K_disc = quaddisc(D); Cl = quadclassunit(K_disc); cyc = Cl[2]; h = Cl[1]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); cl2 = prod(j=1, #cyc, if(cyc[j]%2==0, 2, 1)); ot = has_odd_tor(cyc); rats = if(ot, 0, cl2); match = if(rats == exp_rats[i], "OK", "MISMATCH"); print(D, " : Cl=", cyc, " rk_2=", rk_2, " |Cl[2]|=", cl2, " odd_tor=", ot, " rats=", rats, " expected=", exp_rats[i], " ", match));

print("");
print("=== Note D=-924 ===");
print("D=-924 is NON-fundamental (quaddisc(-924) = ", quaddisc(-924), ")");
print("Analysis pulls back to fund disc -231 = Q(sqrt(-231)), Cl([6,2]) -> 3 in 6 gives odd torsion");

quit;
