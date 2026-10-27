# [numerique] D_metric(kappa, alpha) = sup{ Cov_{q_kappa}(f, <u,v>) : f 1-Lipschitz } sur S^3,
# q_kappa ∝ exp(kappa x1) Haar, v = cos(alpha) e1 + sin(alpha) e2.
# Reduction : moyenne sur SO(2) du plan (e3,e4) => f = g(x1,x2) sur le disque (loi uniforme sous Haar).
# Contrainte |g(p)-g(q)| <= dist min entre fibres : cordale sqrt(|p-q|^2+(r_p-r_q)^2), geodesique arccos(p.q+r_p r_q).
import numpy as np, sys
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
def D(kappa, alpha, kind, m=24):
    # grille polaire equi-aire sur le disque : anneaux
    pts=[];wts=[]
    for i in range(m):
        r0,r1=i/m,(i+1)/m; rc=np.sqrt((r0**2+r1**2)/2)
        k=max(6,int(round(2*np.pi*rc*m)))
        for j in range(k):
            ph=2*np.pi*(j+0.5)/k; pts.append((rc*np.cos(ph),rc*np.sin(ph))); wts.append(np.pi*(r1**2-r0**2)/k)
    P=np.array(pts); w=np.array(wts)/np.pi
    w=w*np.exp(kappa*P[:,0]); w/=w.sum()
    y=np.cos(alpha)*P[:,0]+np.sin(alpha)*P[:,1]
    c=-(w*(y-(w*y).sum()))
    n=len(P); I,J=np.triu_indices(n,1)
    r=np.sqrt(np.clip(1-(P**2).sum(1),0,None))
    if kind=='chord':
        d=np.sqrt(((P[I]-P[J])**2).sum(1)+(r[I]-r[J])**2)
    else:
        d=np.arccos(np.clip((P[I]*P[J]).sum(1)+r[I]*r[J],-1,1))
    M=len(I); ar=np.arange(M)
    A=coo_matrix((np.concatenate([np.ones(M),-np.ones(M),-np.ones(M),np.ones(M)]),
                  (np.concatenate([ar,ar,M+ar,M+ar]),np.concatenate([I,J,I,J]))),shape=(2*M,n)).tocsr()
    bnd=[(None,None)]*n; bnd[0]=(0,0)
    res=linprog(c,A_ub=A,b_ub=np.concatenate([d,d]),bounds=bnd,method='highs')
    return -res.fun
m=int(sys.argv[1]) if len(sys.argv)>1 else 20
print("m =",m)
for kind in ('geo','chord'):
    for kappa in (0.0,0.5,1.0,1.3333,2.0):
        vals=[D(kappa,al,kind,m) for al in np.linspace(0,np.pi/2,7)]
        print(f"{kind:5s} kappa={kappa:6.4f}  D(alpha=0..pi/2)=",' '.join(f"{v:.5f}" for v in vals),f" max={max(vals):.5f}")
print("ref: 8/(9pi)=%.5f  1/4"%(8/(9*np.pi)))
