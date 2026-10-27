import numpy as np, sys
from serie import series
P,H,M=series(40)
Pf=[np.array([float(t) for t in p]) for p in P]; Hf=[np.array([float(t) for t in h]) for h in H]
def evalser(S,k,x,der=0):
    tot=np.zeros_like(x)
    for n,c in enumerate(S):
        pc=np.polynomial.polynomial.Polynomial(c)
        if der: pc=pc.deriv()
        tot=tot+k**n*pc(x)
    return tot
# grille disque en polaires (densité uniforme du projeté de S³ sur (x,y))
nr,nphi=400,800
gr,wr=np.polynomial.legendre.leggauss(nr); r=(gr+1)/2; wr=wr/2
phi=(np.arange(nphi)+0.5)*2*np.pi/nphi; wphi=2*np.pi/nphi
R,PH=np.meshgrid(r,phi,indexing='ij'); X=R*np.cos(PH); Y=R*np.sin(PH); W=(wr*r)[:,None]*wphi*np.ones_like(R)
def quantities(k,al):
    ca,sa=np.cos(al),np.sin(al)
    p=evalser(Pf,k,X); h=evalser(Hf,k,X); hp=evalser(Hf,k,X,1)
    A=ca*p+sa*Y*hp
    N2=A**2*(1-X**2)+sa**2*h**2*(1-Y**2)-2*X*Y*sa*h*A
    wt=W*np.exp(k*X); Z=wt.sum()
    C=(np.sqrt(np.maximum(N2,0))*wt).sum()/Z
    # borne U : rho = |X0| = sqrt(1-(u.v)^2)/3 ; E[(|X|^2/rho + rho)/2]
    uv=ca*X+sa*Y; rho=np.sqrt(np.maximum(1-uv**2,1e-300))/3
    U=((N2/rho+rho)/2*wt).sum()/Z
    return C,U
C0=8/(9*np.pi); print("C0",C0)
for k in [0,0.1,0.3,0.5,0.8,1.0,1.18]:
    row=[]
    for al in np.linspace(0,np.pi,9):
        C,U=quantities(k,al); row.append((C,U))
    print(f"k={k:4.2f} C:"+" ".join(f"{c:.6f}" for c,u in row)); print(f"       U:"+" ".join(f"{u:.6f}" for c,u in row),flush=True)
