"""A62 — analyze ckm_hits.json: deduplicate by underlying rational, rank by simplicity."""
import json
from fractions import Fraction

with open('/root/crossed-cosmos/notes/eci_v7_aspiration/A62_CKM_SYSTEMATIC/ckm_hits.json') as fh:
    d = json.load(fh)

a = {1: Fraction(1, 10), 2: Fraction(1, 12), 3: Fraction(1, 24), 4: Fraction(1, 60)}


def expr_rational(expr_label):
    """Return Fraction value for pure-alpha expressions, None if pi/sqrt involved."""
    s = expr_label
    if 'pi' in s or 'sqrt' in s:
        return None
    if '^2' in s:
        m = int(s.split('^')[0][1:])
        return a[m] * a[m]
    if '/' in s:
        L, R = s.split('/')
        return a[int(L[1:])] / a[int(R[1:])]
    parts = s.split('*')
    val = Fraction(1)
    for p in parts:
        val *= a[int(p[1:])]
    return val


def expr_complexity(label):
    score = 0
    if 'pi' in label:
        score += 8
    if 'sqrt' in label:
        score += 8
    if '^2' in label:
        score += 1
    score += label.count('a')
    score += label.count('/') * 2
    return score


hits = d['Qi_specific_hits']

# Group by (CKM_target, exact rational underlying value)
groups = {}
for h in hits:
    er = expr_rational(h['expr_label'])
    qn, qd = map(int, h['q'].split('/'))
    qf = Fraction(qn, qd)
    if er is None:
        key = (h['CKM_target'], 'IRR:' + h['expr_label'] + ':' + h['q'])
    else:
        prod = qf * er
        key = (h['CKM_target'], str(prod))
    groups.setdefault(key, []).append(h)

# Build unique-pure list with simplest representative per group
unique_pure = []
for (target, key), hs in groups.items():
    if key.startswith('IRR'):
        continue
    hs_sorted = sorted(hs, key=lambda h: expr_complexity(h['expr_label']))
    rep = hs_sorted[0]
    unique_pure.append({
        "CKM_target": target,
        "product": key,
        "best_expr": rep['expr_label'],
        "q": rep['q'],
        "sigma_dist": float(rep['Q(i)_sigma_dist']),
        "n_equiv": len(hs),
    })

unique_pure.sort(key=lambda h: (h["sigma_dist"], expr_complexity(h["best_expr"])))

# Also collect pi-involving and sqrt-involving (separate, since these are
# *not* rational at K=Q(i) and constitute distinct algebraic predictions)
irr_hits = []
for (target, key), hs in groups.items():
    if not key.startswith('IRR'):
        continue
    rep = hs[0]
    irr_hits.append({
        "CKM_target": target,
        "best_expr": rep['expr_label'],
        "q": rep['q'],
        "sigma_dist": float(rep['Q(i)_sigma_dist']),
    })
irr_hits.sort(key=lambda h: (h["sigma_dist"], expr_complexity(h["best_expr"])))

print('=' * 90)
print('A62 — DEDUP UNIQUE PURE-ALPHA Q(i)-SPECIFIC HITS (rational at K=Q(i))')
print('=' * 90)
print(f"{'CKM target':<22} {'best expr':<28} {'q':<10} {'product':<14} {'sigma':>7} {'n_eq':>5}")
print('-' * 90)
for h in unique_pure[:40]:
    expr_with_q = f"{h['best_expr']}"
    print(f"{h['CKM_target']:<22} {expr_with_q:<28} {h['q']:<10} {h['product']:<14} "
          f"{h['sigma_dist']:.4f} {h['n_equiv']:>5}")

print()
print('=' * 90)
print('A62 — TOP IRRATIONAL Q(i)-specific HITS (involve pi or sqrt)')
print('=' * 90)
print(f"{'CKM target':<22} {'best expr':<28} {'q':<10} {'sigma':>7}")
print('-' * 90)
for h in irr_hits[:30]:
    print(f"{h['CKM_target']:<22} {h['best_expr']:<28} {h['q']:<10} {h['sigma_dist']:.4f}")

# Now: for each CKM target, list the cleanest unique pure-alpha hit
print()
print('=' * 90)
print('A62 — CLEANEST PURE-ALPHA HIT PER CKM TARGET')
print('=' * 90)
per_target = {}
for h in unique_pure:
    t = h['CKM_target']
    if t not in per_target or h['sigma_dist'] < per_target[t]['sigma_dist']:
        per_target[t] = h
for t in sorted(per_target.keys()):
    h = per_target[t]
    print(f"{t:<22} -> q={h['q']:<8} expr={h['best_expr']:<28} prod={h['product']:<14} "
          f"sigma={h['sigma_dist']:.4f}")

# Save to JSON
out = {
    "metadata": {
        "agent": "A62",
        "mode": "deduplicated by exact rational value at K=Q(i)",
    },
    "unique_pure_alpha_hits": unique_pure,
    "irrational_hits_top30": irr_hits[:30],
    "cleanest_per_target": {t: h for t, h in per_target.items()},
}
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/A62_CKM_SYSTEMATIC/ckm_hits_dedup.json', 'w') as fh:
    json.dump(out, fh, indent=2, default=str)
print('\nWritten ckm_hits_dedup.json')
