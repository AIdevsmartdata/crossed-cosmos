from fractions import Fraction as Fr
import math
# (b)
D=Fr(1,512)
seq=[D]
for _ in range(4): seq.append(256*seq[-1]**2)
print('Delta_j <= ', [str(x) for x in seq], 'attendu 2^-9..2^-24:', seq[-1]==Fr(1,2**24))
gT3 = Fr(1,31*2**23)               # gamma*T0^3
y0 = 2*gT3*96**3
print('y0 =',y0, y0==Fr(27,3968), float(y0), y0<Fr(1,20))
print('T0=8n: Delta(8n)<=2^-16 ->', end=' ')
g8=Fr(2,31)*Fr(1,2**16); print('y0=',2*g8*96**3, float(2*g8*96**3))
# telescoping
print('sum 32^-k =',Fr(32,31))
# (c) 
print('16/31/256 =',Fr(16,31*256), 'vs 1/496:',Fr(1,496), Fr(16,31*256)==Fr(1,496))
# (d)
print('576*8=',576*8, '9216/(31*256)=',Fr(9216,31*256),'=36/31:',Fr(9216,31*256)==Fr(36,31))
th=math.exp(18/31)-1; print('theta=',th,'-log theta=',-math.log(th))
# check 2^{1-p} <= theta^{p-1} for p=1..40
print(all(2.0**(1-p)<=th**(p-1)+1e-15 for p in range(1,40)))
# example Delta<0 
for r in (0.1,0.5,0.9):
  for n in (3,5):
    print(r,n,64*n**3*math.log(1-r**n)-32*n**3*math.log(1+r**(2*n)))
# 2gamma(96T0)^3 closed form
print(2*96**3/(31*2**23), 27/3968, 54/31)
