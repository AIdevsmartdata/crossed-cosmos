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

import time,random,itertools
random.seed(7); T0t=time.time()
def hcube_box(m2,sides,M):
    arrs=[2-2*np.cos(2*np.pi*np.arange(s)/s) for s in sides]
    K=arrs[0][:,None,None]+arrs[1][None,:,None]+arrs[2][None,None,:]
    w=np.arccosh(1+(m2+K)/2)
    return float(-np.sum(np.log1p(-np.exp(-M*w))))
out={}
BUDGET={0.3:60,0.5:60,1.0:60,2.0:60}
for mass in [2.0,1.0,0.5,0.3]:
    m2=mass*mass; t1=time.time(); rec=dict(ns=[],maxR=0.0,ntori=0,viol=0,argmax=None,skipped=0)
    n=3; Dcache={}
    def Dl(k):
        if k not in Dcache: Dcache[k]=Delta(m2,k)
        return Dcache[k]
    while time.time()-t1<BUDGET[mass]:
        D=Dl(n)
        if D<=2**-9:
            rec['ns'].append(n)
            for mm in (n,2*n):
                Dm=Dl(mm)
                if mm==2*n and (time.time()-t1>BUDGET[mass]): break
                if Dm<=0: continue
                lo,hi=mm,3*mm
                if mm<=12: trip=[t for t in itertools.combinations_with_replacement(range(lo,hi+1),3)]
                else:
                    base=sorted(set([mm,mm+1,mm+2,int(1.5*mm),2*mm,3*mm]))
                    trip=list(itertools.combinations_with_replacement(base,3))
                    trip+= [tuple(sorted(random.randint(lo,hi) for _ in range(3))) for _ in range(15)]
                for t in trip:
                    if t[0]*t[1]*t[2]>2.2e6: rec['skipped']+=1; continue
                    h=hcube_box(m2,t,mm); V=t[0]*t[1]*t[2]
                    R=h/((2*Dm/(31*mm**3))*V)
                    rec['ntori']+=1
                    if R>rec['maxR']: rec['maxR']=R; rec['argmax']=(n,mm,t)
                    if R>1+1e-9: rec['viol']+=1
                if time.time()-t1>BUDGET[mass]: break
        n+=1
        if n>(70 if mass>=0.5 else 100) : break
    # cube gap check r1^n vs 256 Delta for first admissible n and non-dyadic N
    out[str(mass)]=rec
# monotonie de f sur tores aleatoires (masse 0.5, sides 3..14), tolerance 1e-12 relatif
def logZfull(m2,x):
    w=omegas(m2,x[:3]); M=x[3]
    return float(-0.5*np.sum(M*w+2*np.log1p(-np.exp(-M*w))))
viol=0;ntest=0;worst=0
for _ in range(200):
    x=[random.randint(3,14) for _ in range(4)]; mu=random.randrange(4)
    y=list(x); y[mu]+=random.randint(1,3)
    def f(z):
        # use symmetric: time = last coordinate; permute so any coordinate can be time
        zz=list(z); zz[3],zz[mu_p]=zz[mu_p],zz[3]; return logZfull(0.25,zz)/np.prod(z)
    for mu_p in (random.randrange(4),):
        fx,fy=f(x),f(y); ntest+=1
        d=(fy-fx)/abs(fx)
        worst=max(worst,d)
        if d>1e-12: viol+=1
out['monotonie']=dict(tests=ntest,viol=viol,max_rel_increase=worst)
# invariance de Delta
m2=0.25;n=6;a=0.37
d0=16*logZ_cube_mp(m2,n,n)-logZ_cube_mp(m2,2*n,2*n)
d1=16*(logZ_cube_mp(m2,n,n)+a*n**4)-(logZ_cube_mp(m2,2*n,2*n)+a*(2*n)**4)
out['invariance']=float(abs(d0-d1))
# anneaux E3(ii): Z=prod(1+r^x)^{|x|/x}; R = log(1+r^m)/(2D(m)/(31 m^3)) independent of box
mx=0;nv=0;cnt=0
for n in [3,4,5,6,8,12,24,50,100]:
    for lr in np.linspace(-30,-0.01,3000):
        r=math.exp(lr/ n) # r^n = e^lr
        x=r**n
        D=32*n**3*(2*math.log1p(x)-math.log1p(x*x))
        if D>2**-9 or D<=0: continue
        for mm in (n,2*n):
            xm=r**mm; Dm=32*mm**3*(2*math.log1p(xm)-math.log1p(xm*xm))
            if Dm<=0: continue
            R=math.log1p(xm)/(2*Dm/(31*mm**3)); cnt+=1
            mx=max(mx,R)
            if R>1+1e-9: nv+=1
out['anneaux']=dict(cas=cnt,maxR=mx,viol=nv)
# adverse : anneau a niveau NEGATIF (T non positif), n impair
adv=[]
for n in [3,5,7]:
    for r in [0.05,0.2,0.4]:
        x=r**n
        D=32*n**3*(2*math.log1p(-x)-math.log1p(x*x))
        adv.append((n,r,D))
out['adverse_T_non_positif']=adv
print(json.dumps(out,default=str,indent=1))
