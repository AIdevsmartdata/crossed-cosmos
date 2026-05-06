---
name: Stage 1 R3-C-1 Sage cross-check — PASS at 1e-16 precision
description: SageMath 10.7 f.lseries() on f=4.5.b.a (Newforms(Gamma1(4),5)) gives π·L(f,1)/L(f,2) = 1.1999999999999998990... matching 6/5 to 1e-16 (Sage default 53-bit precision floor). M52 PARI 80-digit result CONFIRMED INDEPENDENTLY. Hallu 91→91
type: project
---

# Stage 1 R3-C-1 — SageMath cross-check executed 2026-05-06

**PARI ground truth (M52 F2 v6, 80-digit)**:
- L(f,1) = 0.15244713359066689399684863807331984908...
- L(f,2) = 0.39910566245771742680468011514137526319...
- π·L(f,1)/L(f,2) = **6/5 = 1.2 EXACTLY**

**SageMath 10.7 f.lseries() (default ≈ 53-bit / 1e-16 precision)**:
- L(f,1) = 0.15244713359066688895815389059862354770302773
- L(f,2) = 0.39910566245771744720016727114852983504533768
- π·L(f,1)/L(f,2) = **1.1999999999999998990139334497001317946975356**
- |diff from 6/5| = **1.0098e-16** ≈ Sage default precision floor

## Verdict: PASS at 1e-16

SageMath INDEPENDENTLY reproduces M52 PARI 6/5 result up to default precision. Both methods agree.

For 1e-30 or 1e-50 confirmation, would need:
- `f.lseries().num_coeffs(N)` increased
- Or `f.lseries().value(s, derivative=0, prec=N)` with N=150 explicit
- Or LFunctions.computeT(...) interface

## Methodology

```python
from sage.all import Newforms, Gamma1, RealField, ComplexField, pi
S = Newforms(Gamma1(4), 5, names="a")  # NOT Newforms(4, 5) which is Γ_0
f = next((nf for nf in S if int(nf.coefficient(2)) == -4), None)
# Confirms: a_2 = -4, a_3 = 0, dim S_5(Γ_1(4))^new = 1
L = f.lseries()
L1 = ComplexField(150)(L(1)).real()  # take real part (round-off ~1e-17 imag)
L2 = ComplexField(150)(L(2)).real()
ratio = pi.n(200) * L1 / L2  # use numerical pi
# ratio ≈ 1.2 to 1e-16 ✓
```

## Files
- `/home/remondiere/r3c1_v5.log` (PC) — full Sage output
- `/tmp/r3_c1_stage1_v5.py` (PC) — final script

## Discipline
- 0 fabrications by parent
- M63 SageMath skeleton TODO #0 implemented as `r3_c1_stage1_v5.py`
- Stage 1 cross-check INDEPENDENT of M52 PARI: same answer at agreed precision
- Hallu 91 → 91

## Next steps (Stage 2)
M63 documented Stage 2 requires KLZ Eisenstein-symbol classes + Beilinson regulator pairing (50-100 CPU-hr specialist work). Outreach Loeffler-Zerbes-Brunault for code.
