\\ Kummer K3 from E_a : y^2 = x^3 - x  (CM by Z[i])
\\ Km(E x E) is K3, but easier to work with the transcendental L-function
\\ via the elliptic curve.

\\ For E : y^2 = x^3 - x:
\\   Cremona label : 32.a3 (LMFDB), conductor 32, CM by Z[i]
\\   a_p = 0 for p ≡ 3 mod 4 (inert in Q(i))
\\   a_p = 2*Re(pi_p) for p ≡ 1 mod 4, where p = pi_p * conj(pi_p) in Z[i]

\\ For K3 = Km(E x E), the transcendental part has rank 3 (or 4?)
\\ Actually: Km(E x E') has Picard rank 18 + corank(Hom(E,E'))
\\ If E = E' (same curve), Hom has rank 2 (for non-CM) or 4 (for CM E)
\\ For CM curve E_a, Km(E_a x E_a) has Picard rank 20, transcendental rank 2.

\\ Direct: count points on E_a over F_p for various p
E_a = ellinit([0,0,0,-1,0]); \\ y^2 = x^3 - x

print("Elliptic curve E_a: y^2 = x^3 - x (CM by Z[i])");
print("Conductor: ", ellglobalred(E_a)[1]);
print("Cremona label area: ", ellidentify(E_a)[1][1]);
print();
print("a_p for E_a (p ≡ 3 mod 4 should give a_p = 0):");
print("p, a_p, p mod 4");
{forprime(p=3, 50, if(p != 2, my(ap = ellap(E_a, p)); print([p, ap, p%4])));}

print();
print("--- Now for K3 = Km(E_a x E_a) ---");
print("The L-function L(K3, s) = zeta(s)^a * zeta(s-1)^b * zeta(s-2)^c * L(E_a, s-1)^2 * L(Sym^2 E_a, s)");
print("(with appropriate Tate twists)");
print();
print("In particular: TRANSCENDENTAL Frob trace on K3 = Tr(Frob)_{T_X}");
print("For Km(E x E) with E CM: T_X is 2-dim, gives weight 3 CM newform on Q(i)");
print();

\\ The transcendental L-function of Km(E_a x E_a) is L(f, s) where f is a CM newform
\\ of weight 3 on Q(i), with level 64 typically.
\\ Coefficients of f: a_p(f) = (a_p(E_a))^2 - 2p for p ≡ 1 mod 4, 0 for p ≡ 3 mod 4

print("a_p of transcendental (weight 3 newform from Sym^2 E_a):");
print("p, a_p_K3, p mod 4");
{forprime(p=3, 50, if(p != 2, my(ape = ellap(E_a, p)); my(apk3 = ape^2 - 2*p); print([p, apk3, p%4])));}

\\ This is the rationally-defined weight-3 CM modular form
\\ Compare with ECI hypothesis

print();
print("--- Sum a_p of transcendental ---");
{my(s = 0, sa = 0); forprime(p=3, 50, my(ape = ellap(E_a, p)); my(apk3 = ape^2 - 2*p); s += apk3; sa += abs(apk3)); print("sum a_p (p=3..50): ", s); print("sum |a_p|: ", sa);}
{my(s = 0); forprime(p=3, 100, my(ape = ellap(E_a, p)); my(apk3 = ape^2 - 2*p); s += apk3); print("sum a_p (p=3..100): ", s);}
