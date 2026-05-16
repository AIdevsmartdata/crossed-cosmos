\\ HSH-nuDM Falsifier — 9 Heegner h=1 + extensions h=2 and h=3
\\ rk_2(Cl(K))=0 -> Dirac ; rk_2(Cl(K))>=1 -> Majorana
\\ Ref: project_HSH_v3_OPUS_VINDICATED.md (Gauss 1801 genus theory + Rubin 1991)

print("=== HSH-nuDM 9 Heegner h=1 ===");
print("D | K_disc | Cl_cyc | h_K | rk_2 | nu_predict");
D_list_h1 = [-3, -4, -7, -8, -11, -19, -43, -67, -163];
for(i=1, #D_list_h1, D = D_list_h1[i]; K_disc = quaddisc(D); Cl = quadclassunit(K_disc); cyc = Cl[2]; h = Cl[1]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); nu = if(rk_2==0, "DIRAC", "MAJORANA"); print(D, " | ", K_disc, " | ", cyc, " | h=", h, " | rk_2=", rk_2, " | ", nu));

print("");
print("=== HSH-nuDM extension h=2 ===");
print("D | K_disc | Cl_cyc | h_K | rk_2 | nu_predict");
D_list_h2 = [-15, -20, -24, -35, -40, -51, -52, -88, -91, -115, -123, -148, -187, -232, -235, -267, -403, -427];
for(i=1, #D_list_h2, D = D_list_h2[i]; K_disc = quaddisc(D); Cl = quadclassunit(K_disc); cyc = Cl[2]; h = Cl[1]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); nu = if(rk_2==0, "DIRAC", "MAJORANA"); print(D, " | ", K_disc, " | ", cyc, " | h=", h, " | rk_2=", rk_2, " | ", nu));

print("");
print("=== HSH-nuDM extension h=3 ===");
print("D | K_disc | Cl_cyc | h_K | rk_2 | nu_predict");
D_list_h3 = [-23, -31, -59, -83, -107, -139, -211, -283, -307, -331, -379, -499, -547, -643, -883, -907];
for(i=1, #D_list_h3, D = D_list_h3[i]; K_disc = quaddisc(D); Cl = quadclassunit(K_disc); cyc = Cl[2]; h = Cl[1]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); nu = if(rk_2==0, "DIRAC", "MAJORANA"); print(D, " | ", K_disc, " | ", cyc, " | h=", h, " | rk_2=", rk_2, " | ", nu));

print("");
print("=== D=-67 FOCUS ===");
D = -67; K_disc = quaddisc(D); Cl = quadclassunit(K_disc); cyc = Cl[2]; h = Cl[1]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); nu = if(rk_2==0, "DIRAC", "MAJORANA");
print("D=-67: K_disc=", K_disc, " Cl_cyc=", cyc, " h=", h, " rk_2=", rk_2);
print("  -> nu nature predicted = ", nu);

print("");
print("=== SUMMARY h=1 ===");
ct_dirac = 0; ct_maj = 0;
for(i=1, #D_list_h1, D = D_list_h1[i]; Cl = quadclassunit(quaddisc(D)); cyc = Cl[2]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); if(rk_2==0, ct_dirac++, ct_maj++));
print("Heegner h=1 (", #D_list_h1, " D): Dirac=", ct_dirac, " Majorana=", ct_maj);

print("=== SUMMARY h=2 ===");
ct_dirac = 0; ct_maj = 0;
for(i=1, #D_list_h2, D = D_list_h2[i]; Cl = quadclassunit(quaddisc(D)); cyc = Cl[2]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); if(rk_2==0, ct_dirac++, ct_maj++));
print("h=2 extension (", #D_list_h2, " D): Dirac=", ct_dirac, " Majorana=", ct_maj);

print("=== SUMMARY h=3 ===");
ct_dirac = 0; ct_maj = 0;
for(i=1, #D_list_h3, D = D_list_h3[i]; Cl = quadclassunit(quaddisc(D)); cyc = Cl[2]; rk_2 = sum(j=1, #cyc, if(cyc[j]%2==0, 1, 0)); if(rk_2==0, ct_dirac++, ct_maj++));
print("h=3 extension (", #D_list_h3, " D): Dirac=", ct_dirac, " Majorana=", ct_maj);

quit;
