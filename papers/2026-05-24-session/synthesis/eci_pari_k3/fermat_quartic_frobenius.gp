\\ Fermat quartic K3 : x^4 + y^4 + z^4 + w^4 = 0 in P^3
\\ Compute #X(F_p) and trace of Frobenius for small primes
\\ For K3 of degree 4 in P^3, the Lefschetz formula gives:
\\   #X(F_p) = 1 + p + p^2 + Tr(Frob_p | H^2_et) * p^0    (NO -- careful, weights)
\\ Correct formula for K3 over F_p:
\\   #X(F_p) = 1 + a_p + p^2  where a_p = Tr(Frob_p | H^2_{prim}) * p
\\ Actually for K3: H^0=Q_l, H^2_et 22-dim of pure weight 2,
\\   so eigenvalues of Frob on H^2 have absolute value p.
\\   #X(F_p) = sum_i (-1)^i Tr(Frob | H^i) = 1 + Tr(Frob|H^2) + p^2
\\   where Tr(Frob|H^2) = sum of 22 eigenvalues, each of abs val p.
\\   So |Tr - 22*p| <= 0 only if all signs cancel; max |Tr| = 22*p.

\\ Count points on Fermat quartic over F_p using direct enumeration.
\\ Use projective points: (x:y:z:w) with not all zero, mod scaling.

count_fermat_quartic_Fp(p) = {
    my(n = 0, t);
    \\ Affine charts: w != 0 (set w=1) gives x^4+y^4+z^4+1 == 0
    \\ But we also need to add points at infinity (w=0)
    \\ Easier: count ALL solutions in F_p^4 then handle scaling
    \\ Total in F_p^4 minus (0,0,0,0): then divide by (p-1) for projective
    n = 0;
    for(x=0,p-1, for(y=0,p-1, for(z=0,p-1, for(w=0,p-1,
        if(Mod(x^4+y^4+z^4+w^4, p) == 0, n += 1)
    ))));
    \\ subtract (0,0,0,0) which we don't want as projective point
    n -= 1;
    \\ each projective point counted (p-1) times
    return(n/(p-1));
}

\\ Faster: count using affine charts
\\ Chart w=1: x^4+y^4+z^4 = -1 (mod p)
\\ Chart w=0, z=1: x^4+y^4 = -1 (mod p)
\\ Chart w=0, z=0, y=1: x^4 = -1 (mod p)
\\ Chart w=0, z=0, y=0: x^4 = 0, so x=0 -- not a projective point
\\ Union: count = #{x^4+y^4+z^4 = -1} + #{x^4+y^4 = -1 mod p in F_p^2} + #{x : x^4 = -1}

count_fermat_quartic_fast(p) = {
    my(n_w1 = 0, n_w0z1 = 0, n_w0z0 = 0);
    \\ Chart w=1: 3 variables
    for(x=0,p-1, for(y=0,p-1, for(z=0,p-1,
        if(Mod(x^4+y^4+z^4+1, p) == 0, n_w1 += 1)
    )));
    \\ Chart w=0, z=1: 2 variables
    for(x=0,p-1, for(y=0,p-1,
        if(Mod(x^4+y^4+1, p) == 0, n_w0z1 += 1)
    ));
    \\ Chart w=0, z=0, y=1: 1 variable
    for(x=0,p-1,
        if(Mod(x^4+1, p) == 0, n_w0z0 += 1)
    );
    return(n_w1 + n_w0z1 + n_w0z0);
}

\\ Trace of Frobenius on H^2:
\\ # X(F_p) = 1 + Tr(Frob|H^2) + p^2
\\ => Tr(Frob|H^2) = #X(F_p) - 1 - p^2
trace_frob_h2(p) = {
    my(N);
    N = count_fermat_quartic_fast(p);
    return([p, N, N - 1 - p^2, (N-1-p^2)*1.0/p, 22*p]);
}

\\ Test for bad primes: Fermat quartic over F_p has good reduction
\\ except at p=2 (and possibly p where x^4+y^4+z^4+w^4 becomes singular)
\\ For Fermat quartic: bad reduction at p=2 only.

\\ MAIN COMPUTATION
print("Fermat quartic Frobenius trace computation");
print("p, #X(F_p), Tr(Frob|H^2), Tr/p (Sato-Tate bound 22), 22*p (Weil bound)");
forprime(p=3, 30,
    my(r = trace_frob_h2(p));
    print(r);
);
