# [numerique] controles : (a) D_cordal(kappa, v || s) par LP 1D fine ; (b) borne de reflexion (Levin, Lemme 3.2)
# pour v ⟂ s : D_cordal(kappa, v ⟂ s) <= E_kappa[x_2^2] = (1 - E_kappa[x_1^2])/3.
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.integrate import quad
def lp1d(kappa,n=801):
    th=np.linspace(0,np.pi,n); a=np.cos(th)
    w=np.full(n,np.pi/(n-1)); w[0]/=2; w[-1]/=2
    rho=w*(2/np.pi)*np.sin(th)**2*np.exp(kappa*a); rho/=rho.sum()
    y=a-(rho*a).sum(); c=-(rho*y)
    I,J=np.triu_indices(n,1)
    d=np.sqrt((a[I]-a[J])**2+(np.sin(th[I])-np.sin(th[J]))**2)
    m=len(I); r=np.arange(m)
    A=coo_matrix((np.concatenate([np.ones(m),-np.ones(m),-np.ones(m),np.ones(m)]),(np.concatenate([r,r,m+r,m+r]),np.concatenate([I,J,I,J]))),shape=(2*m,n)).tocsr()
    bnd=[(None,None)]*n; bnd[0]=(0,0)
    return -linprog(c,A_ub=A,b_ub=np.concatenate([d,d]),bounds=bnd,method='highs').fun
def Ex1sq(k):
    Z=quad(lambda t: np.exp(k*np.cos(t))*np.sin(t)**2,0,np.pi)[0]
    return quad(lambda t: np.cos(t)**2*np.exp(k*np.cos(t))*np.sin(t)**2,0,np.pi)[0]/Z
for k in (0,0.25,0.5,1.0,4/3,2.0):
    print(f"kappa={k:.4f}  LP1D parallele={lp1d(k):.6f}   reflexion perp <= {(1-Ex1sq(k))/3:.6f}")
