# [numerique] sup { Cov_Haar(f, x1) : f 1-Lipschitz } sur S^3, metrique cordale vs geodesique, champ nul.
# Reduction : moyenne sur le stabilisateur SO(3) de e1 => f=g(x1) ; contrainte |g(a)-g(b)| <= d(a,b),
# d = distance minimale entre les niveaux {x1=a},{x1=b}. Loi de x1 sous Haar(S^3) : (2/pi) sqrt(1-a^2) da.
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
def solve(n, kind):
    th=np.linspace(0,np.pi,n)          # a = cos th (grille en angle)
    a=np.cos(th)
    # poids de quadrature : int g(a) a rho(a) da = int g(cos th) cos th (2/pi) sin^2 th dth
    w=np.full(n,np.pi/(n-1)); w[0]=w[-1]=w[0]/2
    c=-(w*a*(2/np.pi)*np.sin(th)**2)
    I,J=np.triu_indices(n,1)
    if kind=='chord':
        d=np.sqrt((a[I]-a[J])**2+(np.sin(th[I])-np.sin(th[J]))**2)
    else:
        d=np.abs(th[I]-th[J])
    m=len(I); rows=np.repeat(np.arange(2*m),2)
    r=np.arange(m)
    A=coo_matrix((np.concatenate([np.ones(m),-np.ones(m),-np.ones(m),np.ones(m)]),
                  (np.concatenate([r,r,m+r,m+r]),np.concatenate([I,J,I,J]))),shape=(2*m,n))
    bnd=[(None,None)]*n; bnd[n//2]=(0,0)
    res=linprog(c,A_ub=A.tocsr(),b_ub=np.concatenate([d,d]),bounds=bnd,method='highs')
    return -res.fun, res.status
for n in (101,201,401):
    vc,sc=solve(n,'chord'); vg,sg=solve(n,'geo')
    print(f"n={n}  cordale: {vc:.6f} (status {sc})   geodesique: {vg:.6f} (status {sg})")
print("references: 1/N=1/4=0.25 ; 8/(9pi)=%.6f ; sqrt5/N=%.6f"%(8/(9*np.pi),np.sqrt(5)/4))
