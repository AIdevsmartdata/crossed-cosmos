import math, random, json
random.seed(20261112)
LOG2=math.log(2)
def lse(a,b): m=max(a,b); return m+math.log(math.exp(a-m)+math.exp(b-m))
class Ring:
    def __init__(s,levels,kappa,f=0.0):  # levels: list of (g,a) -> rho=exp(-a*kappa)
        s.lv=levels; s.k=kappa; s.f=f
    def sT(s,L): return sum(g*math.exp(-a*s.k*L) for g,a in s.lv)
    def phi(s,L): return math.log1p(s.sT(L))
    def loglam(s,t):  # log lambda0 of spatial torus t (time-independent part), per m
        V=t[0]*t[1]*t[2]
        return s.f*V+sum((V/ti)*s.phi(ti) for ti in t)
    def logZ4(s,x):  # full log Z of 4-torus
        P=x[0]*x[1]*x[2]*x[3]
        return s.f*P+sum((P/xm)*s.phi(xm) for xm in x)
def make(nc):
    comps=[]
    for c in range(nc):
        nl=random.randint(1,6)
        lv=[(random.randint(1,4),math.exp(random.uniform(math.log(0.1),math.log(10)))) for _ in range(nl)]
        comps.append(lv)
    return comps
class Model:
    def __init__(s,comps,kappa,deltas):
        s.rs=[Ring(lv,kappa,d) for lv,d in zip(comps,deltas)]
    def logZ4(s,x):
        v=[r.logZ4(x) for r in s.rs]
        m=max(v); return m+math.log(sum(math.exp(a-m) for a in v))
    def Delta(s,n):
        # subtract dominant-ring extensive part exactly: baseline = ring0 with f0
        r0=s.rs[0]
        d0=32*n**3*(2*r0.phi(n)-r0.phi(2*n)) # ring0 part (f0 extensive cancels)
        def corr(x):
            v=[r.logZ4(x)-r0.logZ4(x) for r in s.rs]  # first is 0
            m=max(v); return m+math.log(sum(math.exp(a-m) for a in v))
        return d0+16*corr((n,)*4)-corr((2*n,)*4)
    def hhat(s,t,M):  # log Zhat_t(M), exact
        ll=[r.loglam(t) for r in s.rs]; L=max(ll)
        V=t[0]*t[1]*t[2]
        terms=[M*(l-L)+V*r.phi(M) for l,r in zip(ll,s.rs)]
        # 1 = dominant ground state: Zhat = sum_a e^{M(l_a-L)}(1+s_a)^V ; ln of that
        m=max(terms); return m+math.log(sum(math.exp(a-m) for a in terms))
def tune(comps,deltas,n,target):
    lo,hi=1e-4,50.0   # kappa: Delta decreasing in kappa
    f=lambda k: Model(comps,k,deltas).Delta(n)
    if f(lo)<target or f(hi)>target: return None
    for _ in range(80):
        mid=math.sqrt(lo*hi)
        if f(mid)>target: lo=mid
        else: hi=mid
    return hi
BOX=[(2,2,2),(2,3,5),(3,5,12),(12,12,12),(2,2,47),(47,47,47)]
def gam(T0): return 1/(40*(96*T0)**3)
def Bstar(M,T0):
    worst=0
    for b in BOX:
        t=tuple(s*T0 for s in b); V=t[0]*t[1]*t[2]
        h=M.hhat(t,T0)
        worst=max(worst,h/V)
    return worst<=gam(T0), worst/gam(T0)
res={"ring":dict(N=0,kmax=0,viol=[],eq4viol=[],worst=None),"sum":dict(N=0,kmax=0,viol=[],eq4viol=[],worst=None)}
import time; t0=time.time()
for fam in ("ring","sum"):
    R=res[fam]
    while time.time()-t0 < (110 if fam=="ring" else 220):
        n=random.choice([3,3,4,5,6,8,10,16,24,40])
        nc=1 if fam=="ring" else 2
        comps=make(nc)
        deltas=[0.0]+([random.choice([-1,1])*math.exp(random.uniform(-14,-4))*0 for _ in range(nc-1)] if nc>1 else [])
        if nc>1:
            # f2-f1 negative (component 2 subdominant at all sizes), size of gap tuned randomly relative to 1/n^4
            deltas=[0.0,-math.exp(random.uniform(math.log(1e-3),math.log(1.0)))/(n**3)]
        target=2**-9*random.choice([1,1,1,0.9,0.5,0.1,0.01])
        kap=tune(comps,deltas,n,target)
        if kap is None: continue
        M=Model(comps,kap,deltas); D=M.Delta(n)
        if D>2**-9*(1+1e-9): continue
        # simplicity of lambda0 for ring comps: component 2 dominance check on box set
        ok=True
        # find k_min over grid, T0 = ceil(k n)
        kmin=None
        for kk in [x/4 for x in range(4,65)]:
            T0=max(3,math.ceil(kk*n))
            okB,_=Bstar(M,T0)
            if okB: kmin=kk;break
        if kmin is None: kmin=99
        R["N"]+=1
        if kmin>R["kmax"]: R["kmax"]=kmin; R["worst"]=dict(n=n,Delta=D,comps=comps,deltas=deltas,kappa=kap)
        T0=16*n
        okB,ratio=Bstar(M,T0)
        if not okB: R["viol"].append(dict(n=n,D=D,comps=comps,deltas=deltas,kappa=kap))
        # eq (4) at m=n,2n,4n on boxes with sides >= m
        for j in range(3):
            m=n*2**j; Dm=M.Delta(m)
            for tt in [(m,m,m),(m,2*m,3*m),(m+1,m+3,2*m+1)]:
                V=tt[0]*tt[1]*tt[2]
                if M.hhat(tt,m)>2*Dm*V/(31*m**3)*(1+1e-9)+1e-300:
                    R["eq4viol"].append(dict(n=n,m=m,tt=tt,Dm=Dm,h=M.hhat(tt,m)))
print(json.dumps({k:{"N":v["N"],"kmax_min_factor_worst":v["kmax"],"n_viol_Bstar_16n":len(v["viol"]),"n_viol_eq4":len(v["eq4viol"]),"worst_model":v["worst"],"viol_sample":v["viol"][:2],"eq4_sample":v["eq4viol"][:2]} for k,v in res.items()},indent=1,default=str))
