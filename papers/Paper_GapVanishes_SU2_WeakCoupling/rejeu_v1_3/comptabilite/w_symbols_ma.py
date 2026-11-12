# Verification independante des symboles de Fourier de lem:projrate : (i) int sum|f_mn|^2 = c(0)=1.1377494917 ; (ii) W=sum_x |x|^2|f|^2 par derivees ; (iii) sup des derivees par composante vs bornes annoncees
import numpy as np, json
def fh(k):
    e=[np.exp(1j*k[m])-1 for m in range(4)]
    kh2=sum(abs(x)**2 for x in e)
    v=1-np.exp(-1j*k[1]); w=v/kh2
    u2=np.conj(e[1])*w; u1=-np.conj(e[2])*w
    # f_{mu nu} = e_mu u_nu - e_nu u_mu avec u_1=-conj(e2) w, u_2=conj(e1) w, u_0=u_3=0
    u=[0*w,u1,u2,0*w]
    return {(a,b): e[a]*u[b]-e[b]*u[a] for a in range(4) for b in range(a+1,4)}
res={}
for N in (24,32,40):
    g=(np.arange(N)+0.5)/N*2*np.pi-np.pi
    K=np.meshgrid(g,g,g,g,indexing='ij')
    f=fh(K)
    tot=sum(np.mean(abs(x)**2) for x in f.values())
    h=1e-5; W=0; sup={}
    for lam in range(4):
        Kp=[x+(h if m==lam else 0) for m,x in enumerate(K)]; Km=[x-(h if m==lam else 0) for m,x in enumerate(K)]
        fp,fm=fh(Kp),fh(Km)
        for key in f:
            d=(fp[key]-fm[key])/(2*h)
            W+=np.mean(abs(d)**2); sup[(key,lam)]=max(sup.get((key,lam),0),np.max(abs(d)))
    res[N]={'int_sum_|f|^2':float(tot),'W':float(W)}
    if N==40:
        comp={}
        for (key,lam),v in sup.items(): comp.setdefault(str(key),[]).append(round(float(v),3))
        res['sup_deriv_par_composante(lambda=0..3)']=comp
        res['sum_lam_sup2']={k:round(sum(x*x for x in v),3) for k,v in comp.items()}
print(json.dumps(res,indent=1))
