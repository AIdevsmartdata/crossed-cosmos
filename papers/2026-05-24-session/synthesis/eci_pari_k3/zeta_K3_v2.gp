\\ Final identification of CM newform for Fermat quartic transcendental part

\\ Standard result from Schoen 1988 / Tate-Schiermann:
\\ The Fermat quartic K3 X has transcendental L-function L(T_X, s) corresponding
\\ to the weight-3 Hecke L-function of psi^2 on Q(i), where psi is the canonical
\\ Hecke character of Q(i) (related to E: y^2=x^3-x).
\\
\\ Equivalently, L(T_X, s) = L(Sym^2 E, s) where E: y^2=x^3-x.
\\
\\ Let's verify by direct calculation:

E_a = ellinit([0,0,0,-1,0]);
print("E_a: y^2 = x^3 - x, CM Z[i]");
print("a_p for E_a:");
{forprime(p=3, 30, print([p, ellap(E_a, p), p%4]));}

print();
print("Sym^2 of E_a gives weight 3 newform with a_p(Sym^2 E) = a_p(E)^2 - p");
print("Compare with our Fermat quartic Tr - 2p (= transcendental candidate):");
print("p, Tr(Fermat) - 2p, Sym^2 a_p");
fermat_data = [[3,6],[5,-26],[7,14],[11,22],[13,-42],[17,310],[19,38],[23,46],[29,-74],[31,62],[37,-218],[41,838],[43,86],[47,94]];
{for(i=1, #fermat_data, my(p=fermat_data[i][1], tr=fermat_data[i][2]); my(ape=ellap(E_a,p)); my(sym2=ape^2 - p); my(transcand=tr - 2*p); print([p, transcand, sym2, transcand - sym2]));}

print();
print("Conclusion: see if Tr(Frob|Fermat) - 2*p = c * sym2(E) for some c");

\\ Check ratio
{for(i=1, #fermat_data, my(p=fermat_data[i][1], tr=fermat_data[i][2]); my(ape=ellap(E_a,p)); my(sym2=ape^2 - p); my(diff=tr - 2*p); if(sym2 != 0, print(p, ": diff/sym2 = ", diff*1.0/sym2)));}
