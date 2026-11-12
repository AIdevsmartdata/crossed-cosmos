import numpy as np, json
# Verification numerique des bornes intermediaires de la preuve de W<=45 (lem:projrate) : multiplicateur P(k)=E_q E_q^*, f^=a P e_12
import numpy as np, itertools, json
pairs=[(a,b) for a in range(4) for b in range(a+1,4)]
def Eq(q):   # q: (...,4) complexe -> (...,6,4) : (q^u)_{mn}=q_m u_n - q_n u_m
    M=np.zeros(q.shape[:-1]+(6,4),dtype=complex)
    for i,(m,n) in enumerate(pairs): M[...,i,n]+=q[...,m]; M[...,i,m]-=q[...,n]
    return M
def parts(k):
    e=np.exp(1j*k)-1; r=np.sqrt(np.sum(abs(e)**2,axis=-1)); q=e/r[...,None]
    a=1-np.exp(-1j*k[...,1]); E=Eq(q); P=E@np.conj(np.swapaxes(E,-1,-2))
    e12=np.zeros(6,dtype=complex); e12[0]=1   # pairs[0]=(0,1)... on veut (1,2)
    e12=np.zeros(6,dtype=complex); e12[pairs.index((1,2))]=1
    f=a[...,None]*(P@e12)
    return f,P,q,r,a
def fsym(k):  # symboles de la note : f_{mn}=e_m u_n - e_n u_m, u1=-conj(e2) w, u2=conj(e1) w
    e=np.exp(1j*k)-1; kh2=np.sum(abs(e)**2,axis=-1); v=1-np.exp(-1j*k[...,1]); w=v/kh2
    u=[0*w,-np.conj(e[...,2])*w,np.conj(e[...,1])*w,0*w]
    return np.stack([e[...,m]*u[n]-e[...,n]*u[m] for (m,n) in pairs],axis=-1)
rng=np.random.default_rng(7); K=rng.uniform(-np.pi,np.pi,size=(300000,4)); h=1e-6
N=0
for j in range(4):
    Kp=K.copy();Km=K.copy();Kp[:,j]+=h;Km[:,j]-=h
    N=N+np.sum(abs((fsym(Kp)-fsym(Km))/(2*h))**2,axis=-1)
r=2-2*np.cos(K); D=r.sum(1); R=r[:,1]+r[:,2]; T=r[:,0]+r[:,3]; s=R/D; a=r[:,1]/D
form=s+2*a*(2-s)
print(json.dumps({"max|N-formule|":float(np.max(abs(N-form))),"max N":float(N.max()),"mean N":float(N.mean())}))
