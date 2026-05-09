default(realprecision, 100)

G4 = znstar(4, 1)
mf4 = mfinit([4, 5, [G4, znconreychar(G4, 3)]], 0)
nfeig4 = mfeigenbasis(mf4)
L4 = lfuninit(lfunmf(mf4, nfeig4[1]), [3])

G36 = znstar(36, 1)
mf36 = mfinit([36, 5, [G36, znconreychar(G36, 19)]], 0)
nfeig36 = mfeigenbasis(mf36)
target = 0
for(i=1, #nfeig36, if(mfcoef(nfeig36[i], 2) == 4, target = i))
L36 = lfuninit(lfunmf(mf36, nfeig36[target]), [3])

L4at2 = lfun(L4, 2)
L36at2 = lfun(L36, 2)

E = ellinit([0, 0, 0, -1, 0])
om_E = E.omega[1]

a4 = L4at2 * Pi^2 / om_E^4
a36 = L36at2 * Pi^2 / om_E^4

print("alpha_2(4.5.b.a) = ", a4)
print("alpha_2(36.5.d.a) = ", a36)
print("alpha_2(36) * 9 = ", a36 * 9)
print("4*sqrt(3) = ", 4*sqrt(3))
print("alpha_2(36) * 9 - 4*sqrt(3) = ", a36 * 9 - 4*sqrt(3))

\\ Check if a36 = 4*sqrt(3)/9 or some related sqrt(3) / rational
print("=== Check alpha_2(36) involving sqrt(3) ===")
print("a36 / sqrt(3) = ", a36 / sqrt(3))
print("a36 * sqrt(3) = ", a36 * sqrt(3))
print("algdep(a36, 2, 30) = ", algdep(a36, 2, 30))
print("algdep(a36 / sqrt(3), 1, 30) = ", algdep(a36 / sqrt(3), 1, 30))
print("algdep(a36 * sqrt(3), 1, 30) = ", algdep(a36 * sqrt(3), 1, 30))

\\ sqrt(3) might come from disc(Q(zeta_3)) = -3
\\ The twist by chi_3 introduces a factor of sqrt(3) (the conductor of chi_3)
\\ Standard formula: L(f tensor chi, k-1) involves Gauss sum tau(chi) of chi
\\ tau(chi_3) = sqrt(3) (real Gauss sum for the Legendre symbol)
\\ So the "rational" alpha_2(36) in the natural twist normalization would be:
\\   alpha_2(36) := L(36.5.d.a, 2) * tau(chi_3) * Pi^2 / Omega_E^4 = sqrt(3) * a36
\\ Check this:
print("alpha_2(36) * sqrt(3) = ", a36 * sqrt(3))
print("12 * a36 * sqrt(3) = ", 12 * a36 * sqrt(3))
print("9 * a36 / sqrt(3) = ", 9 * a36 / sqrt(3))
print("4 / 3 = ", 4.0/3)

\\ Hmm. Let me try a36 = c * sqrt(3) for various rationals c
v = a36 / sqrt(3)
for(d = 1, 100, n = round(v * d); err = abs(n*1.0/d - v); if(err < 1e-30, print("a36 = (", n, "/", d, ") * sqrt(3); err = ", err)))

\\ Also check a36 = c / sqrt(3)
v2 = a36 * sqrt(3)
for(d = 1, 100, n = round(v2 * d); err = abs(n*1.0/d - v2); if(err < 1e-30, print("a36 = (", n, "/", d, ") / sqrt(3); err = ", err)))

\\ Maybe a36 = c * 3^(k/2) for some half-integer k
\\ 3^(0.5) = 1.732
\\ 3^(1.5) = 5.196
\\ 3^(2.5) = 15.588
\\ a36 = 0.7698
print("a36 / 3^(1/2) = ", a36 / 3^(1/2))
print("a36 / 3^(-1/2) = ", a36 * 3^(1/2))
print("a36 * 3 = ", a36 * 3)
print("a36 * 9 = ", a36 * 9)
print("a36 * 9 / 4 = ", a36 * 9 / 4)
print("4 * sqrt(3) / 9 = ", 4 * sqrt(3) / 9)

\\ So a36 = 4 * sqrt(3) / 9 ?
expected = 4 * sqrt(3) / 9
print("a36 - 4*sqrt(3)/9 = ", a36 - expected)
print("a36 / (4*sqrt(3)/9) = ", a36 / expected)

\\ Maybe the precise rational involves more factors
\\ Let's algdep at higher degree
print("algdep(a36, 4, 100) = ", algdep(a36, 4, 100))

quit
