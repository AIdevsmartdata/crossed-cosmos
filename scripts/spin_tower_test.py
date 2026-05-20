#!/usr/bin/env python3
"""
Spin Tower Equispacing — Corrected (PySR v5 normalization)
=================================================================
H-ÉMERGE1 : c²(J+2) − c²(J) = 2α = 8/9 EXACT (∀ J, par construction)
→ Δm² scale with F(N)² cross-N

FIXED bugs:
  1. No c²(0) offset — formula IS c² = α·J + (β-P)·(ex+γ)
  2. PySR normalization: K = √(4πe/3), F(N) = (N²+1)/N²
"""

import math

# PySR v5 constants (rational candidates)
ALPHA = 4/9     # = (2/3)² = ξ★²
BETA  = 16/7
GAMMA = 2/3     # = ξ★

K_PYSR = math.sqrt(4 * math.pi * math.e / 3)  # ≈ 3.374

def c2(J, P, ex=0):
    """c² = α·J + (β-P)·(ex+γ)"""
    return ALPHA * J + (BETA - P) * (ex + GAMMA)

def F_pysr(N):
    """F(N) = (N²+1)/N² (PySR normalization, no 9/10)"""
    return (N**2 + 1) / N**2

def m_pred_pysr(J, P, ex, N):
    return K_PYSR * F_pysr(N) * math.sqrt(c2(J, P, ex))

# AT2021 canonical
AT2021 = {3: {'0++':3.405, '2++':4.870, '0-+':5.420, '2-+':6.500, '0++*':5.450},
          2: {'0++':3.781, '2++':5.349}}
LIT = {'1+-':5.66, '3++':5.90, '3+-':6.45, '4++':6.80}

print("=" * 60)
print("SPIN TOWER — PySR v5 (CORRECTED)")
print("=" * 60)
print(f"α=4/9, β=16/7, γ=2/3")
print(f"K=√(4πe/3)={K_PYSR:.4f}, F(3)=10/9={10/9:.4f}")
print(f"K·F(3)={K_PYSR*10/9:.4f}")
print()

# ── Fitted channels (SU(3)) ──
print("FITTED CHANNELS (SU(3)):")
print(f"  {'J^PC':>7} {'c²':>8} {'m pred':>8} {'m AT2021':>8} {'Δ%':>6}")
for lab, J, P, ex in [('0++',0,+1,0),('2++',2,+1,0),('0-+',0,-1,0),
                        ('2-+',2,-1,0),('0++*',0,+1,1)]:
    c2v = c2(J,P,ex); mp = m_pred_pysr(J,P,ex,3)
    ma = AT2021[3][lab]
    print(f"  {lab:>7} {c2v:8.4f} {mp:8.2f} {ma:8.2f} {(mp/ma-1)*100:+5.1f}%")

# ── PREDICTIONS (independent channels) ──
print(f"\nPREDICTIONS (independent, SU(3)):")
print(f"  {'J^PC':>7} {'c²':>8} {'m pred':>8} {'m lit':>8} {'Δ%':>6}")
for lab, J, P in [('1+-',1,+1),('3++',3,+1),('3+-',3,-1),('4++',4,+1)]:
    c2v = c2(J,P); mp = m_pred_pysr(J,P,0,3)
    ml = LIT.get(lab)
    ds = f"{(mp/ml-1)*100:+5.1f}%" if ml else "—"
    ms = f"{ml:.2f}" if ml else "N/A"
    print(f"  {lab:>7} {c2v:8.4f} {mp:8.2f} {ms:>8} {ds:>6}")

# ── EQUISPACING ──
print(f"\nEQUISPACING: Δc² = 2α = 8/9 = {8/9:.4f} (EXACT by formula)")
d02 = c2(2,+1) - c2(0,+1)
d0m2m = c2(2,-1) - c2(0,-1)
print(f"  Δc²(0→2)={d02:.4f}, Δc²(0⁻→2⁻)={d0m2m:.4f}  (ratio={d0m2m/d02:.6f})")
print(f"  → Δm² = K²·F²(N)·8/9")

# ── CROSS-N TEST ──
d_su3 = (AT2021[3]['2++']**2 - AT2021[3]['0++']**2)
d_su2 = (AT2021[2]['2++']**2 - AT2021[2]['0++']**2)
r_theory = (F_pysr(2)/F_pysr(3))**2  # (5/4)/(10/9)² = (45/40)² = (9/8)²
r_meas = d_su2 / d_su3
print(f"\nCROSS-N (SU(2)/SU(3)):")
print(f"  Theory: [F(2)/F(3)]² = {r_theory:.4f}")
print(f"  Measured: {d_su2:.1f}/{d_su3:.1f} = {r_meas:.4f}")
print(f"  Δ = {(r_meas/r_theory-1)*100:+.1f}%")

# ── DEGENERACIES ──
print(f"\nDEGENERACIES (c² equality):")
for a, b in [('0++*','0-+'), ('0-+','3++'), ('1+-','4++')]:
    c2a = c2(*{'0++*':(0,+1,1),'0-+':(0,-1,0),'3++':(3,+1,0),
                '1+-':(1,+1,0),'4++':(4,+1,0)}[a])
    c2b = c2(*{'0-+':(0,-1,0),'3++':(3,+1,0),'4++':(4,+1,0)}[b])
    print(f"  c²({a})={c2a:.4f} = c²({b})={c2b:.4f} ? {'YES' if abs(c2a-c2b)<1e-10 else f'Δ={abs(c2a-c2b):.4f}'}")
