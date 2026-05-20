\\ === PARI: 9/10 Origin Dataset — Fixed ===
default(realprecision, 50);
default(parisizemax, 2^28);

print("D,h_K,rk2,zK2,Vol,Lchi1,zeta_ratio,hK_target,FN_target");
print("-------------------------------------------------------");

\\ Generate fundamental discriminants D in [-3, -1000]
for(Dabs=3, 1000,
    if(issquarefree(Dabs) && (Dabs % 4 == 3 || (Dabs % 4 == 1 && Dabs % 8 != 5)),
        D = -Dabs;
        \\ Fundamental discriminant check
        if(D == -4 || kronecker(D, 2) != 0 || Dabs % 4 == 0,
            \\ simplified: skip messy checks, just use issquarefree
            if(isfundamental(D),
                K = bnfinit(x^2 - D);
                hK = K.no;
                if(hK <= 50 && hK > 0,
                    \\ 2-rank
                    cyc = K.clgp[2];
                    rk2 = 0;
                    for(j=1,#cyc, if(cyc[j] % 2 == 0, rk2++));

                    \\ Dedekind zeta
                    zK2 = lfun(K, 2);

                    \\ Volume
                    vol = Dabs^(3/2) * zK2 / (4*Pi^2);

                    \\ L(chi, 1)
                    w = if(D == -3, 6, if(D == -4, 4, 2));
                    Lchi1 = 2*Pi*hK / (w * sqrt(Dabs));

                    \\ zeta ratio
                    zeta_ratio = zK2 / (Pi^2/6);

                    \\ F(N) target
                    FN = (9.0/10.0) * (hK^2 + 1) / hK^2;

                    printf("%d,%d,%d,%.10f,%.10f,%.10f,%.10f,%d,%.10f\n",
                           D, hK, rk2, zK2, vol, Lchi1, zeta_ratio, hK, FN);
                );
            );
        );
    );
);

print("=== DONE ===");
print("=== EXTENDED KEY DISCRIMINANTS ===");
keydiscs = [-5460, -9240, -1155, -1995, -3003, -3315, -4389, -5313, -7917, -10379,
            -12075, -14235, -16555, -19019, -21755, -24735, -27963, -31435];
for(i=1, #keydiscs,
    Dabs = keydiscs[i];
    D = -Dabs;
    if(isfundamental(D),
        K = bnfinit(x^2 - D);
        hK = K.no;
        if(hK > 0,
            cyc = K.clgp[2];
            rk2 = 0;
            for(j=1,#cyc, if(cyc[j] % 2 == 0, rk2++));
            zK2 = lfun(K, 2);
            vol = Dabs^(3/2) * zK2 / (4*Pi^2);
            w = 2;
            Lchi1 = 2*Pi*hK / (w * sqrt(Dabs));
            zeta_ratio = zK2 / (Pi^2/6);
            FN = (9.0/10.0) * (hK^2 + 1) / hK^2;
            printf("%d,%d,%d,%.10f,%.10f,%.10f,%.10f,%d,%.10f\n",
                   D, hK, rk2, zK2, vol, Lchi1, zeta_ratio, hK, FN);
        );
        print("D=", D, " not fundamental or error");
    );
);
print("=== FINAL DONE ===");
