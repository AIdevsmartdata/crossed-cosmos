import math
# anneau a un niveau (g=1): phi(L)=log1p(x^(L/n)), x=r^n ; Delta=32 n^3 (2 phi(n)-phi(2n)) = 2^-9 -> x*(n)
def D(n,x): return 32*n**3*(2*math.log1p(x)-math.log1p(x*x))
for n in [3,4,6,10,24,100,1000,10**5]:
    lo,hi=1e-30,0.5
    for _ in range(200):
        mid=math.sqrt(lo*hi)
        if D(n,mid)>2**-9: hi=mid
        else: lo=mid
    x=lo
    # smallest real k with log1p(x^k) <= 1/(40 (96 k n)^3)
    f=lambda k: math.log1p(x**k)-1/(40*(96*k*n)**3)
    a,b=1.0,16.0
    for _ in range(100):
        c=(a+b)/2
        if f(c)>0: a=c
        else: b=c
    print(n,"x*=%.3e"%x,"k_min(reel)=%.4f"%b,"T0=%.1f"%(b*n))
