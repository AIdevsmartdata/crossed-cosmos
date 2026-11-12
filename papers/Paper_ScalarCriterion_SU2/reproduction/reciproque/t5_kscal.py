import numpy as np, math, json
import mpmath as mp
mp.mp.dps=60

def omegas(m2, sides):
    ks=[2*np.pi*np.arange(s)/s for s in sides]
    K=sum(np.meshgrid(*[2-2*np.cos(k) for k in ks],indexing='ij'))
    return np.arccosh(1+(m2+K)/2).ravel()
def logZ(m2,sides,M):
    w=omegas(m2,sides)
    return -0.5*np.sum(M*w+2*np.log1p(-np.exp(-M*w)))
def logZ4(m2,x):  # x=(x1..x4); use x[3] as time
    return logZ(m2,x[:3],x[3])

_cache={}
def _classes(s):
    key=s
    if key in _cache: return _cache[key]
    # modes j in Z/s ; reduce by j<->-j (weight 2 unless j=0 or s/2) then unordered triples
    base=[]
    for j in range(s//2+1):
        w=1 if (j==0 or 2*j==s) else 2
        base.append((j,w))
    out=[]
    from itertools import combinations_with_replacement
    for (a,b,c) in combinations_with_replacement(range(len(base)),3):
        ja,wa=base[a];jb,wb=base[b];jc,wc=base[c]
        trip=[a,b,c]
        # multiplicity of permutations
        from math import factorial
        from collections import Counter
        cnt=Counter(trip); perm=factorial(3)
        for v in cnt.values(): perm//=factorial(v)
        out.append((ja,jb,jc,wa*wb*wc*perm))
    _cache[key]=out; return out
def logZ_cube_mp(m2,s,M):
    m2=mp.mpf(m2); tot=mp.mpf(0)
    cs=[2-2*mp.cos(2*mp.pi*j/s) for j in range(s//2+1)]
    for ja,jb,jc,w in _classes(s):
        K=cs[ja]+cs[jb]+cs[jc]
        om=mp.acosh(1+(m2+K)/2)
        tot+=w*(M*om+2*mp.log(1-mp.exp(-M*om)))
    return -tot/2
def Delta(m2,n):
    return float(16*logZ_cube_mp(m2,n,n)-logZ_cube_mp(m2,2*n,2*n))

def hbox(m2,sides,T,wcut=45.0):
    # exact sum with cutoff T*w<=wcut (omitted part < V*e^-45*O(1)); sides up to modest
    cmax=2*math.cosh(wcut/T)-2-m2
    if cmax<0: return 0.0
    ks=[]
    for s in sides:
        j=np.arange(s); k=2*np.pi*j/s
        a=2-2*np.cos(k); ks.append(a[a<=cmax])
    if any(len(a)==0 for a in ks): return 0.0
    if np.prod([len(a) for a in ks],dtype=float)>3e7: return None
    K=sum(np.meshgrid(*ks,indexing='ij'))
    w=np.arccosh(1+(m2+K)/2).ravel(); w=w[T*w<=wcut]
    return float(-np.sum(np.log1p(-np.exp(-T*w))))
def mass_at_threshold(n,target=2**-9):
    lo,hi=1e-6,5.0   # Delta decreasing in m
    for _ in range(60):
        mid=math.sqrt(lo*hi)
        if Delta(mid**2,n)>target: lo=mid
        else: hi=mid
    return hi

for n in [3,4,6,8,12]:
    m=mass_at_threshold(n); m2=m*m; wmin=math.acosh(1+m2/2)
    kmin=None
    for kk in [x/20 for x in range(20,321)]:
        T0=max(3,math.ceil(kk*n))
        # (B*) uniform sufficient bound u<=gamma_max ; (necessary: zero mode of cube 2T0: h/V >= e^{-T0 wmin}/V ... only sufficient test)
        u=-math.log1p(-math.exp(-T0*wmin))
        if u<=1/(40*(96*T0)**3): kmin=kk;break
    print(n,"m_seuil=%.5f"%m,"k_min(suffisant)=",kmin,flush=True)
