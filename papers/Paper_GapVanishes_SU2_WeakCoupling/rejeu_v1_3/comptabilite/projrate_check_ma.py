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
rng=np.random.default_rng(1); res={}
K=rng.uniform(-np.pi,np.pi,size=(400000,4)); f,P,q,r,a=parts(K)
res['diff_symboles_vs_P']=float(np.max(abs(f-fsym(K))))
res['max_norme_P_e12']=float(np.max(np.linalg.norm(P[...,:,pairs.index((1,2))],axis=-1)))
res['max_|a|/r']=float(np.max(abs(a)/r))
h=1e-6; mx_dq=0; mx_dP=0; mx_df=[0]*4; W=0
for j in range(4):
    Kp=K.copy(); Km=K.copy(); Kp[:,j]+=h; Km[:,j]-=h
    fp,Pp,qp,_,_=parts(Kp); fm,Pm,qm,_,_=parts(Km)
    dq=np.linalg.norm((qp-qm)/(2*h),axis=-1)*r; mx_dq=max(mx_dq,float(np.max(dq)))
    dP=np.linalg.norm((Pp-Pm)/(2*h),ord=2,axis=(-2,-1))*r/2; mx_dP=max(mx_dP,float(np.max(dP)))   # ||dP|| r /2 <= 1 ?
    df=np.linalg.norm((fp-fm)/(2*h),axis=-1); mx_df[j]=float(np.max(df))
res['max_r|d_j q| (<=1)']=mx_dq; res['max_r||d_j P||/2 (<=|d_j q| r<=1)']=mx_dP
res['max_|d_j f^| par j (<= 2+delta_j1)']=mx_df
res['borne_somme_carres_sup']=sum(x*x for x in mx_df)
# W par grille de milieux (symboles) : somme_j moyenne |d_j f|^2
N=32; g=(np.arange(N)+0.5)/N*2*np.pi-np.pi; Kg=np.stack(np.meshgrid(g,g,g,g,indexing='ij'),-1).reshape(-1,4)
W=0
for j in range(4):
    Kp=Kg.copy(); Km=Kg.copy(); Kp[:,j]+=h; Km[:,j]-=h
    d=(fsym(Kp)-fsym(Km))/(2*h); W+=float(np.mean(np.sum(abs(d)**2,axis=-1)))
res['W_grille32']=W
res['norme2_u (a/r)^2 moyenne = 1/4 ?']=float(np.mean(abs(1-np.exp(-1j*Kg[:,1]))**2/np.sum(abs(np.exp(1j*Kg)-1)**2,axis=-1)))
print(json.dumps(res,indent=1))
