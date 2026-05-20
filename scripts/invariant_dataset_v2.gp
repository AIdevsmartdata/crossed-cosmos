\\ === PARI: 9/10 Origin Dataset ===
default(realprecision, 30);
default(parisizemax, 2^28);

print("D,h_K,rk2,zK2,Vol,Lchi1,zeta_ratio,hK_target,FN_target");

\\ Main loop over fundamental discriminants
for(Dabs=3, 800,
    if(isfundamental(-Dabs),
        D = -Dabs;
        K = bnfinit(x^2 - D, 1);  \\ 1 = no GRH, faster
        hK = K.no;
        if(hK > 0 && hK <= 60,
            cyc = K.clgp[2];
            rk2 = 0;
            for(j=1, #cyc, if(cyc[j] % 2 == 0, rk2++));

            zK2 = lfun(K, 2);
            vol = Dabs^(3/2) * zK2 / (4*Pi^2);

            w = if(D == -3, 6, if(D == -4, 4, 2));
            Lchi1 = 2*Pi*hK / (w * sqrt(Dabs));

            zeta_ratio = zK2 / (Pi^2/6);
            FN = (9.0/10.0) * (hK^2 + 1) / hK^2;

            printf("%d,%d,%d,%.10f,%.10f,%.10f,%.10f,%d,%.10f\n",
                   D, hK, rk2, zK2, vol, Lchi1, zeta_ratio, hK, FN);
        );
    );
);

print("=== DONE ===");
