\\ Fermat quartic K3 : x^4 + y^4 + z^4 + w^4 = 0 in P^3
\\ Count projective points by chart decomposition.

count_FQ_chart_w1(p) = my(n=0); for(x=0,p-1, for(y=0,p-1, for(z=0,p-1, if(Mod(x^4+y^4+z^4+1,p)==0, n+=1)))); n;

count_FQ_chart_w0z1(p) = my(n=0); for(x=0,p-1, for(y=0,p-1, if(Mod(x^4+y^4+1,p)==0, n+=1))); n;

count_FQ_chart_w0z0y1(p) = my(n=0); for(x=0,p-1, if(Mod(x^4+1,p)==0, n+=1)); n;

count_FQ_total(p) = count_FQ_chart_w1(p) + count_FQ_chart_w0z1(p) + count_FQ_chart_w0z0y1(p);

trace_frob_h2(p) = my(N); N=count_FQ_total(p); [p, N, N-1-p^2, (N-1-p^2)*1.0/p];

print("Fermat quartic Frobenius trace computation");
print("Columns: p, #X(F_p), Tr(Frob|H^2), Tr/p (|.|<22 by Sato-Tate)");
{forprime(p=3, 30, my(r = trace_frob_h2(p)); print(r));}
