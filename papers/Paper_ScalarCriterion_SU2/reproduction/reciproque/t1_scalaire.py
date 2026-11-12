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
res=[];viol=[]
for n in [3,4,6,8,12]:
    mth=mass_at_threshold(n)
    masses=[mth*f for f in (1.0,1.0001,1.02,1.1,1.3,1.7,2.5)]
    for m in masses:
        m2=m*m; D=Delta(m2,n)
        if D>2**-9: continue
        T0=16*n; wmin=math.acosh(1+m2/2)
        u=-math.log1p(-math.exp(-T0*wmin)); gmax=1/(40*(96*T0)**3)
        # exact sums on some boxes
        worst=u*0; sidesets=[(2,2,2),(2,3,5),(3,5,12),(12,12,12),(2,2,12)]
        wh=0.0
        for ss in sidesets:
            hh=hbox(m2,tuple(s*T0 for s in ss),T0)
            if hh is None: continue
            wh=max(wh,hh/np.prod([s*T0 for s in ss]))
        # intermediate (4): h_t(m')<=2D(m')V/(31 m'^3), t_i>=m'
        ok4=True; slack4=1e9
        for j in range(0,3):
            mm=n*2**j; Dm=Delta(m2,mm)
            for tt in [(mm,mm,mm),(mm,2*mm,3*mm),(mm+1,mm+2,2*mm+1)]:
                hh=hbox(m2,tt,mm,wcut=700.0)
                if hh is None: continue
                bound=2*Dm*np.prod(tt)/(31*mm**3)
                if hh>bound*(1+1e-9)+1e-300: ok4=False
                if bound>0 and hh>0: slack4=min(slack4,bound/hh)
        # (7) cubes N>=n: gap=wmin ; need r^n=exp(-n wmin)<=256 D
        ok7=math.exp(-n*wmin)<=256*D*(1+1e-12) and wmin>=math.log(2)/n
        rec=dict(n=n,m=m,Delta=D,u_bound=u,gamma_max=gmax,ratio_u_over_gmax=u/gmax,exact_max_h_over_V=wh,ok4=ok4,min_bound_over_h_eq4=slack4,ok7=ok7,Bstar=(max(u,wh)<=gmax))
        res.append(rec)
        if not (rec['Bstar'] and ok4 and ok7): viol.append(rec)
        print(json.dumps(rec),flush=True)
print("VIOLATIONS",len(viol)); print(json.dumps(viol))
