"""Tests Q1, Q5, Q6 — H25/H26 robustness ECI."""
import numpy as np
from math import sqrt

def class_number(D):
    if D >= 0 or D % 4 not in (0, 1):
        return None
    abs_D = -D
    count = 0
    a_max = int((abs_D / 3) ** 0.5) + 1
    for a in range(1, a_max + 1):
        for b in range(-a, a + 1):
            num = b*b - D
            if num % (4*a) == 0:
                c = num // (4*a)
                if c >= a:
                    if (abs(b) == a or a == c) and b < 0:
                        continue
                    count += 1
    return count

LIE_SIMPLE_DIMS = {
    3: 'A_1=SU(2)', 8: 'A_2=SU(3)', 10: 'B_2=SO(5)=Sp(4)', 14: 'G_2',
    15: 'A_3=SU(4)=SO(6)', 21: 'B_3=SO(7)=Sp(6)', 24: 'A_4=SU(5)',
    28: 'D_4=SO(8)', 35: 'A_5=SU(6)', 36: 'B_4=SO(9)=Sp(8)',
    45: 'D_5=SO(10)', 48: 'A_6=SU(7)', 52: 'F_4', 55: 'B_5=Sp(10)',
    63: 'A_7=SU(8)', 66: 'D_6=SO(12)', 78: 'E_6', 91: 'B_6=SO(13)',
    120: 'A_9=SU(10)', 133: 'E_7', 248: 'E_8',
}
ALLOWED_DIMS = sorted(LIE_SIMPLE_DIMS.keys())

# Q1
b_2_K3 = 22
print("="*72)
print("Q1 : k groupes — partitions Σh = 22+k en k Lie simples")
print('='*72)
for k in [1, 2, 3, 4, 5]:
    target_sum = b_2_K3 + k
    solutions = []
    def find_partitions(remaining, k_left, current, start_idx):
        if k_left == 0:
            if remaining == 0:
                solutions.append(tuple(current))
            return
        for i in range(start_idx, len(ALLOWED_DIMS)):
            d = ALLOWED_DIMS[i]
            if d > remaining:
                break
            if d * k_left <= remaining + d * (k_left-1):
                find_partitions(remaining - d, k_left - 1, current + [d], i)
    find_partitions(target_sum, k, [], 0)
    print(f"\n  k={k}, Σh={target_sum} : {len(solutions)} solution(s)")
    for sol in solutions[:5]:
        groups = ' × '.join([LIE_SIMPLE_DIMS[d] for d in sol])
        print(f"     {sol} = {groups}")
    if len(solutions) > 5:
        print(f"     ... +{len(solutions)-5} autres")

# Q5
print("\n" + "="*72)
print("Q5 : h(D) = dim(G) coincidence sur tous les dims Lie simples")
print('='*72)
print(f"\n  {'dim(G)':>7s}  {'groupe':<25s}  {'min |D|':>9s}")
print('  ' + '-'*55)
coverage = []
for dim_g in ALLOWED_DIMS:
    if dim_g > 100:
        break
    min_D = None
    max_search = max(1000, dim_g * dim_g * 4)
    for d in range(3, min(max_search + 1, 5000)):
        D = -d
        if D % 4 not in (0, 1):
            continue
        h = class_number(D)
        if h == dim_g:
            min_D = D
            break
    coverage.append((dim_g, min_D))
    name = LIE_SIMPLE_DIMS[dim_g]
    if min_D:
        print(f"  {dim_g:>5d}  {name:<25s}  {-min_D:>9d}")
    else:
        print(f"  {dim_g:>5d}  {name:<25s}  NOT FOUND <{max_search}")

# Q6
print("\n" + "="*72)
print("Q6 : (-23,-95,-215) minimise-t-il Σ|D| parmi triples (3,8,14) ?")
print('='*72)
D_h3, D_h8, D_h14 = [], [], []
for d in range(3, 501):
    D = -d
    if D % 4 not in (0, 1):
        continue
    h = class_number(D)
    if h == 3:
        D_h3.append(D)
    elif h == 8:
        D_h8.append(D)
    elif h == 14:
        D_h14.append(D)

print(f"\n  D avec h=3 in [-500,-3] : {len(D_h3)}, premiers : {D_h3[:5]}")
print(f"  D avec h=8 in [-500,-3] : {len(D_h8)}, premiers : {D_h8[:5]}")
print(f"  D avec h=14 in [-500,-3] : {len(D_h14)}, premiers : {D_h14[:5]}")
print(f"  Total triples : {len(D_h3) * len(D_h8) * len(D_h14)}")

# Min |D| per class
min_D3, min_D8, min_D14 = D_h3[0], D_h8[0], D_h14[0]
print(f"\n  Min |D| par h-class :")
print(f"    h=3  → D = {min_D3} (|D|={-min_D3})")
print(f"    h=8  → D = {min_D8} (|D|={-min_D8})")
print(f"    h=14 → D = {min_D14} (|D|={-min_D14})")
print(f"    Σ|D|_min = {-min_D3 + -min_D8 + -min_D14}")

# Our triple
our = (-23, -95, -215)
print(f"\n  Notre triple : {our}")
print(f"    Σ|D| = 23+95+215 = {23+95+215}")

if (min_D3, min_D8, min_D14) == our:
    print(f"\n  ★★★ CONFIRMÉ : (-23,-95,-215) = MIN |D| par h-class !!! H25 prouvé.")
else:
    print(f"\n  ✗ MISMATCH : real min per-class = ({min_D3}, {min_D8}, {min_D14})")
