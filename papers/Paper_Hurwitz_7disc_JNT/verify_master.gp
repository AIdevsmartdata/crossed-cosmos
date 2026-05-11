default(realprecision, 50);
B2chi(D) = {my(s = 0, B2); for(a = 1, D - 1, if(gcd(a, D) == 1, B2 = (a/D)^2 - (a/D) + 1/6; s += kronecker(D, a) * B2)); return(D * s);}
verify_hurwitz(D) = {my(B, L_formula, L_pari, diff); B = B2chi(D); L_formula = Pi^2 * B / D^(3/2); L_pari = lfun(D, 2); diff = abs(L_formula - L_pari); return([B, L_formula, L_pari, diff]);}
print("=== A. Hurwitz formula verification ===");
print("D  | B_{2,chi_D} | L_formula                | L_PARI                   | diff");
fund_D = [5, 8, 12, 13, 17, 21, 24, 28, 29, 33, 37, 40, 41, 44, 53, 56, 57, 60, 61, 65, 73, 76, 77, 88, 89, 92, 93, 97, 101, 104, 105, 109, 113, 120, 124, 129, 133, 136, 137, 140, 141, 145, 149, 152, 156, 157, 161, 165, 168, 172, 173, 177, 181, 184, 185, 188, 193, 197];
for(i = 1, #fund_D, D = fund_D[i]; if(isfundamental(D), res = verify_hurwitz(D); printf("%4d | %-12s | %.22s | %.22s | %.2e\n", D, res[1], res[2], res[3], res[4])));
print();
print("=== B. The 7 integer-k discriminants ===");
print("D    | k(D) | B_{2,chi} | factor(D)     | factor(k)     | zeta_K(-1) = B/24");
seven_D = [8, 12, 24, 28, 60, 76, 156];
for(i = 1, #seven_D, D = seven_D[i]; B = B2chi(D); k = D^2 / B; printf("%4d | %4s | %-9s | %-13s | %-13s | %s\n", D, k, B, factor(D), factor(numerator(k)), B/24));
print();
print("=== C. Sweep D <= 5000 to confirm only 7 ===");
count = 0;
for(D = 2, 5000, if(isfundamental(D) && D > 0, B = B2chi(D); if(B != 0, ratio = D^2 / B; if(denominator(ratio) == 1, count++; printf("  D=%4d : k=%s integer (B=%s)\n", D, ratio, B)))));
printf("Total integer-k cases up to D=5000 : %d\n", count);
print();
print("=== END ===");
quit;
