"""Séries de perturbation EXACTES (rationnels) en κ pour le champ de transport gradient d'un lien.
ψ_v = cα g(x) + sα y h(x),  x = u·ŝ, y = u·e (e ⊥ ŝ), p = g'.
  p : (1-x²)(p'+κp) - 3x p = -(x - m(κ))          [m(κ) = E_κ x]
  h : (1-x²)(h''+κh') - 5x h' - (3+κx) h = -1
Retourne listes de polynômes (coeffs Fraction, puissances croissantes de x) p_n, h_n, et m_n."""
from fractions import Fraction as Fr
def polyadd(a,b):
    n=max(len(a),len(b)); return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(n)]
def mulx(a): return [Fr(0)]+list(a)
def deriv(a): return [i*a[i] for i in range(1,len(a))] or [Fr(0)]
def scal(c,a): return [c*t for t in a]
def one_m_x2(a): return polyadd(a, scal(-1,mulx(mulx(a))))
def solveB(r):
    """(1-x²)p' - 3x p = r ; renvoie p et le résidu constant exigé (c_1 - r_0)."""
    r=list(r)+[Fr(0)]*2; d=len(r)-1
    while d>0 and r[d]==0: d-=1
    c=[Fr(0)]*(d+2)
    # coefficient de x^{j}: (j+1)c_{j+1} - (j+2) c_{j-1} = r_j  (j>=1) ; j=0 : c_1 = r_0
    for j in range(d+1,0,-1):
        cj1 = c[j+1] if j+1<len(c) else 0
        c[j-1]=((j+1)*cj1 - r[j])/(j+2)
    return c, c[1]-r[0]
def solveA(r):
    """(1-x²)h'' - 5x h' - 3h = r."""
    d=len(r)-1; c=[Fr(0)]*(d+3)
    for k in range(d,-1,-1):
        c[k]=((k+2)*(k+1)*c[k+2] - r[k])/((k+1)*(k+3))
    return c[:d+1]
def series(N):
    P=[];H=[];M=[]
    for n in range(N+1):
        # p
        r=[Fr(0)]
        if n==0: r=[Fr(0),Fr(-1)]
        else: r=scal(-1,one_m_x2(P[n-1]))
        c,mn=solveB(r)   # need r_0 + m_n = c_1  => m_n = c_1 - r_0
        M.append(mn); P.append(c)
        # h
        if n==0: r=[Fr(-1)]
        else: r=polyadd(scal(-1,one_m_x2(deriv(H[n-1]))), mulx(H[n-1]))
        H.append(solveA(r))
    return P,H,M
if __name__=="__main__":
    import sys
    P,H,M=series(int(sys.argv[1]) if len(sys.argv)>1 else 8)
    for n in range(4): print(n,'m',M[n],'p',P[n],'h',H[n])
    import mpmath
    # gate : m(κ) = I2(κ)/I1(κ)
    for k in [0.3,1.2]:
        s=sum(float(M[n])*k**n for n in range(len(M)))
        print('m gate',k,s, mpmath.besseli(2,k)/mpmath.besseli(1,k))
    for n in range(0,len(P),5):
        print(n, max(abs(float(t)) for t in P[n]), max(abs(float(t)) for t in H[n]))
