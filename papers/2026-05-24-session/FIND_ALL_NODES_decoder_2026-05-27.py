#!/usr/bin/env python3
"""
FIND ALL NODES — Exhaustive node detection in decoder network.

Pour chaque value dans catalog, on cherche TOUTES les autres values qui matchent
(rel < 0.005). Si 2+ sectors → c'est un NŒUD du network.

Output : ranked list of all potential nodes by network connectivity.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json, re
import numpy as np
from collections import defaultdict

with open('/root/cc-private/papers/OBSERVABLES_DATASET.json') as f:
    cat = json.load(f)


def parse_value(s):
    if s is None: return None
    if isinstance(s, (int, float)): return float(s)
    if not isinstance(s, str): return None
    s = s.strip().lstrip('~<>≈')
    m = re.match(r'^-?\d+/\d+$', s)
    if m:
        n, d = s.split('/'); return float(n)/float(d)
    try: return float(s)
    except: pass
    m = re.match(r'^(-?\d+\.?\d*(?:[eE][-+]?\d+)?)', s)
    if m:
        try: return float(m.group(1))
        except: pass
    return None


# Build clean list
obs = []
for e in cat['entries']:
    val = parse_value(e.get('value'))
    if val is None or val <= 0: continue
    if e.get('derivation_status') in ('FALSIFIED ❌', 'FALSIFIED'): continue
    obs.append({
        'id': e['id'], 'name': e.get('observable',''), 'value': val,
        'sector': e.get('sector',''), 'status': e.get('derivation_status',''),
        'source': e.get('source','')
    })

print(f"=== Find all nodes from {len(obs)} non-falsified observations ===\n")

# ============================
# CLUSTERING : group by value (rel < 0.005)
# ============================
# For each obs, find all other obs that match within 0.5%
clusters = []  # list of {value, members}
used = set()
for i, o in enumerate(obs):
    if i in used: continue
    cluster = [o]
    used.add(i)
    for j, o2 in enumerate(obs):
        if j == i or j in used: continue
        rel = abs(o['value'] - o2['value']) / max(abs(o['value']), abs(o2['value']))
        if rel < 0.005:
            cluster.append(o2)
            used.add(j)
    if len(cluster) >= 2:
        # Compute "centroid" value
        centroid = float(np.mean([m['value'] for m in cluster]))
        sectors = set(m['sector'] for m in cluster)
        clusters.append({
            'centroid_value': centroid,
            'n_members': len(cluster),
            'n_sectors': len(sectors),
            'sectors': sorted(sectors),
            'members': cluster
        })

# Rank by n_sectors (most cross-sector first), then n_members
clusters.sort(key=lambda c: (-c['n_sectors'], -c['n_members']))

print(f"=== All NODES (≥2 sectors) — ranked by cross-sector connectivity ===\n")
print(f"{'value':>12s} {'#sect':>6s} {'#obs':>5s} sectors  | top member names")
print("-"*120)

major_nodes = [c for c in clusters if c['n_sectors'] >= 2]
print(f"\nTotal major nodes (≥2 sectors) : {len(major_nodes)}\n")

for c in major_nodes[:40]:
    sect_str = ", ".join(c['sectors'][:5])
    names_str = " | ".join(m['name'][:20] for m in c['members'][:5])
    print(f"{c['centroid_value']:>12.4e} {c['n_sectors']:>6d} {c['n_members']:>5d} [{sect_str:50s}] {names_str[:60]}")

# Sub-class : super-nodes (≥3 sectors)
super_nodes = [c for c in clusters if c['n_sectors'] >= 3]
print(f"\n\n=== SUPER-NODES (≥3 sectors) ===\n")
for c in super_nodes:
    print(f"\n🌟 Value = {c['centroid_value']:.4e} ({c['n_sectors']} sectors, {c['n_members']} observations)")
    print(f"   Sectors : {c['sectors']}")
    for m in c['members'][:10]:
        print(f"     [{m['sector'][:14]:14s}] {m['name'][:50]:50s} = {m['value']:.4e}")

# Try to identify each super-node value
print(f"\n=== Identification des super-nodes ===\n")
named_constants = {
    '1/6': 1/6, '2/3': 2/3, '1/4': 1/4, '1/3': 1/3, '1/2': 0.5,
    '3/4': 0.75, '9/10': 0.9, '4/3': 4/3, '11/3': 11/3,
    'π': np.pi, '4/π²': 4/np.pi**2, 'π/4': np.pi/4, '1/π': 1/np.pi,
    'ζ(3)/√π': 1.2020569/np.sqrt(np.pi), 'ζ(3)': 1.2020569,
    'e': np.e, '1/e': 1/np.e, 'ln2': np.log(2),
    'phi_gold': 1.6180339887, '1/phi': 1/1.6180339887,
    'sqrt2': np.sqrt(2), 'sqrt3': np.sqrt(3),
    '7/3 (d_s)': 7/3, '5/3 (K41)': 5/3,
    '3/13': 3/13, '10/13': 10/13, '19/23': 19/23,
    '22 (b₂K3)': 22, '21 (b₂K3-1)': 21,
    '77 (Σ_8)': 77, '281 (Σ_14)': 281,
}

for c in super_nodes:
    v = c['centroid_value']
    best_match = None
    best_rel = 1.0
    for name, cv in named_constants.items():
        rel = abs(v - cv) / max(abs(v), abs(cv), 1e-20)
        if rel < best_rel:
            best_rel = rel
            best_match = name
    if best_match and best_rel < 0.01:
        print(f"  {v:>12.4e} → {best_match} (rel = {best_rel*100:.2f}%)")
    else:
        print(f"  {v:>12.4e} → NO standard match (best : {best_match} at {best_rel*100:.1f}%)")

# Save
out = {
    'date': '2026-05-27',
    'total_obs': len(obs),
    'total_clusters': len(clusters),
    'major_nodes_2plus_sectors': len(major_nodes),
    'super_nodes_3plus_sectors': len(super_nodes),
    'all_nodes': [{
        'value': c['centroid_value'],
        'n_sectors': c['n_sectors'],
        'n_members': c['n_members'],
        'sectors': c['sectors'],
        'members': [{'name': m['name'], 'sector': m['sector'], 'value': m['value']} for m in c['members']]
    } for c in clusters],
}
with open('/root/cc-private/papers/NODES_decoder.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /root/cc-private/papers/NODES_decoder.json")
print(f"\nTotal : {len(clusters)} value clusters")
print(f"  ≥2 sectors : {len(major_nodes)}")
print(f"  ≥3 sectors : {len(super_nodes)}")
print(f"  ≥4 sectors : {sum(1 for c in clusters if c['n_sectors']>=4)}")
print(f"  ≥5 sectors : {sum(1 for c in clusters if c['n_sectors']>=5)}")
