#!/usr/bin/env python3
"""
BRIDGE MAP — Cross-sector explicit network :
- Anchors (κ_FP, ξ★, c∞, F∞, 4/π², ζ(3)/√π, b_0, ...) → ALL observations matching
- Bianchi geometric structure (F_μν, ε^{abc}, K3 b_2, dim G, ...) → sectors
- Riemann ζ(s) connections (ζ(3), ζ(s) poles, prime sums)
- Cross-sector identity bridges

Output : visual network map + JSON.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json, re
import numpy as np
from sympy import sieve

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


obs_list = []
for e in cat['entries']:
    val = parse_value(e.get('value'))
    if val is None: continue
    obs_list.append({
        'id': e['id'], 'name': e.get('observable',''), 'value': val,
        'sector': e.get('sector',''), 'status': e.get('derivation_status',''),
        'type': e.get('type',''), 'source': e.get('source','')
    })

print(f"=== BRIDGE MAP from {len(obs_list)} observations ===\n")

# ============================
# ANCHORS DEFINITIONS
# ============================
anchors = {
    # YM Seeley-DeWitt
    'κ_FP = 1/6 (Kostant)':        (1/6, 'YM-SD a_2 coefficient'),
    'ξ★ = 2/3 (BG SD a_1)':         (2/3, 'YM-SD boundary'),
    'c∞ = 1/4 (Bekenstein D=4)':    (1/4, 'BH area-law'),
    'c∞ D=3 = 1/3':                 (1/3, 'BH area-law D=3'),
    'F∞ = 9/10 (saturation)':       (9/10, 'YM polynomial saturation'),
    'b_0/N = 11/3 (β-fct one-loop)': (11/3, 'YM β-function'),
    'd_s = 3 (GZ standard)':        (3, 'spectral dim'),
    'd_s = 7/3 (refined GZ)':       (7/3, 'spectral dim BG×HL'),
    'z = 3 (Hořava renorm)':        (3, 'anisotropic critical'),

    # Universal constants
    '4/π² ≈ 0.4053':                (4/np.pi**2, 'universal const'),
    'ζ(3)/√π ≈ 0.6782':             (1.2020569/np.sqrt(np.pi), 'κ_∞ asymptote'),
    'π/4 ≈ 0.785':                  (np.pi/4, 'universal'),

    # SM rationals
    'A_CKM = 19/23':                (19/23, 'CKM rational'),
    'sin²θ_W = 3/13':               (3/13, 'EW rational'),
    'cos²θ_W = 10/13':              (10/13, 'EW complement'),
    'Koide K = 2/3':                (2/3, 'Yukawa identity'),
    'sin²θ₂₃ = 4/7':                (4/7, 'PMNS'),
    'm_Z/v = 10/27':                (10/27, 'EW mass'),
    'n_s = 27/28':                  (27/28, 'cosmology'),

    # Σ premiers
    'Σ_8 = 77 (QCD adj)':           (77, 'Σ_k=8 premiers'),
    'Σ_14 = 281 (G_2 adj)':         (281, 'Σ_k=14 premiers'),
    'Σ_21 = 791 (b_2(K3))':         (791, 'Σ_k=21 premiers'),
}

# ============================
# BRIDGE 1 : each ANCHOR → observations matching
# ============================
print("="*80)
print("BRIDGE 1 : Anchor → ALL observations where it appears (rel < 0.005)")
print("="*80)

bridges_anchor_to_obs = {}
for aname, (aval, origin) in anchors.items():
    hits = []
    for o in obs_list:
        if o['value'] is None or o['value'] <= 0: continue
        if o['status'] in ('FALSIFIED ❌', 'FALSIFIED'): continue
        rel = abs(o['value'] - aval) / max(abs(o['value']), abs(aval), 1e-20)
        if rel < 0.005:
            hits.append({'obs': o['name'], 'sector': o['sector'], 'rel': rel, 'status': o['status']})
    bridges_anchor_to_obs[aname] = {'value': aval, 'origin': origin, 'hits': hits}
    if len(hits) >= 2:
        sectors = set(h['sector'] for h in hits)
        sector_str = ', '.join(sorted(sectors))
        print(f"\n🔗 {aname:35s} ({origin}) appears in {len(sectors)} sectors:")
        print(f"   {sector_str}")
        for h in hits[:8]:
            print(f"   [{h['sector'][:12]:12s}] {h['obs'][:45]:45s} rel={h['rel']*100:.3f}%")


# ============================
# BRIDGE 2 : BIANCHI structure
# ============================
print("\n" + "="*80)
print("BRIDGE 2 : Bianchi geometric structure")
print("="*80)

bianchi_keywords = {
    'f^abc structure constants': ['f^{abc}', 'fabc', 'structure constant', 'f_{abc}'],
    'F_μν field strength':       ['F_{μν}', 'F_munu', 'field strength', 'tr(F'],
    'd^abc symmetric tensor':    ['d^{abc}', 'dabc', 'symmetric tensor'],
    'K3 b_2 = 22':               ['b_2(K3)', 'K3', 'Hodge'],
    'Bianchi identity':          ['Bianchi', 'D_μ', 'd F = 0'],
    'Gribov ∂Ω':                 ['Gribov', '∂Ω', 'horizon'],
    'Faddeev-Popov':             ['Faddeev', 'FP', 'Δ_FP', 'M_FP'],
    'dim G = N²-1':              ['dim G', 'dim SU', 'dim(G)'],
    'Casimir SU(N) = N':         ['Casimir', 'C_2', 'C2'],
    'Kostant Φ⁺(SU(N))':         ['Kostant', 'Φ+', 'positive roots'],
    'AHS instanton':              ['AHS', 'Atiyah-Hitchin-Singer', 'instanton'],
}

bianchi_hits = {}
for bname, kws in bianchi_keywords.items():
    hits = []
    for o in obs_list:
        name_low = (o['name'] + ' ' + o.get('source','')).lower()
        for kw in kws:
            if kw.lower() in name_low:
                hits.append({'obs': o['name'], 'sector': o['sector'], 'value': o['value']})
                break
    if hits:
        bianchi_hits[bname] = hits
        sectors = set(h['sector'] for h in hits)
        print(f"\n🔷 {bname} ({len(hits)} hits across {len(sectors)} sectors):")
        for h in hits[:8]:
            print(f"   [{h['sector'][:12]:12s}] {h['obs'][:55]:55s} = {h['value']:.4e}")


# ============================
# BRIDGE 3 : RIEMANN ζ
# ============================
print("\n" + "="*80)
print("BRIDGE 3 : Riemann ζ(s) connections")
print("="*80)

zeta_keywords = {
    'ζ(3) Apéry':                  ['ζ(3)', 'zeta3', 'zeta(3)', 'Apéry', 'apery', 'Apery'],
    'ζ(s) poles':                  ['ζ(s)', 'pole ζ', 'zeta function', 'zeta pole'],
    'ζ_Δ_FP spectral zeta':        ['ζ_Δ', 'spectral zeta', 'ζ_{Δ_FP}'],
    'Selberg trace':               ['Selberg', 'trace formula'],
    'Σ premiers':                  ['Σ premiers', 'sum of primes', 'Σ_k=', 'cumsum', 'metaselector'],
    'Mertens theorem':             ['Mertens', 'prime counting', 'π(x)'],
    'ln(M_Pl/v) ~ Σ_8':            ['ln(M_Pl', 'M_Pl/v', 'Σ_8'],
    'L-functions':                 ['L-function', 'Dirichlet'],
}

primes = list(sieve.primerange(2, 250))
cumsum_p = np.cumsum(primes[:30])

zeta_hits = {}
for zname, kws in zeta_keywords.items():
    hits = []
    for o in obs_list:
        name_low = (o['name'] + ' ' + o.get('source','')).lower()
        for kw in kws:
            if kw.lower() in name_low:
                hits.append({'obs': o['name'], 'sector': o['sector'], 'value': o['value']})
                break
    if hits:
        zeta_hits[zname] = hits
        sectors = set(h['sector'] for h in hits)
        print(f"\n🌀 {zname} ({len(hits)} hits across {len(sectors)} sectors):")
        for h in hits[:6]:
            print(f"   [{h['sector'][:12]:12s}] {h['obs'][:55]:55s} = {h['value']:.4e}")


# ============================
# BRIDGE 4 : CROSS-SECTOR identity chains
# ============================
print("\n" + "="*80)
print("BRIDGE 4 : Cross-sector chains (anchor appears in ≥ 3 sectors)")
print("="*80)

strong_bridges = []
for aname, info in bridges_anchor_to_obs.items():
    sectors = set(h['sector'] for h in info['hits'])
    if len(sectors) >= 3:
        strong_bridges.append({'anchor': aname, 'sectors': sorted(sectors), 'n_obs': len(info['hits'])})

print(f"\n  Anchors crossing ≥3 sectors :")
for sb in strong_bridges:
    print(f"\n  🌟 {sb['anchor']}")
    print(f"     Sectors: {sb['sectors']}")
    print(f"     {sb['n_obs']} observations")


# ============================
# BRIDGE 5 : VISUAL NETWORK
# ============================
print("\n" + "="*80)
print("BRIDGE 5 : Network visualization (text-art)")
print("="*80)

network = """

                      [Riemann ζ(3)] ←──────────────┐
                            │                       │
                            ▼                       │
              ζ(3)/√π = 0.6782 = κ_∞                │
                  (YM-lattice asymptote)            │
                  (ECI κ formula)                   │
                            │                       │
                            ▼                       │
              [κ_FP=1/6] (Kostant) ⇐⇒ [Koide K=2/3]
                  ↑                       ↑
                  │                       │
              YM-SD anchor          Yukawa identity
                  ↑                       ↑
                  │                       │
              [a_2 SD coef]         [4·κ_FP = K]
                  │                       │
                  ▼                       │
              [Bianchi: D_μ F^μν = 0]    │
                  │                       │
                  ▼                       │
              [ξ★ = 2/3] (BG a_1)         │
                  ↑                       │
                  │                       │
                d_∂ = 2/3 (Gribov ∂Ω)    │
                  ↑                       │
                  │                       │
              [Hořava-Lifshitz z=3] ← {b_0=11N/(48π²)}
                  │                       │
                  ▼                       │
              [d_s = 7/3] (BG×HL fixed point)
                  ↓
              [d_s = 3] (GZ standard z=2) ← simpler defendable
                  │
                  ▼
              [Mass gap kinematic argument ρ(0)=0]
                  │
                  ▼
              [Clay YM millennium]


              [Σ premiers metaselector]
                  ├── k=8 (QCD adj): ln(M_Pl/v)² ≈ Σ_8 = 77  (4.3%)
                  ├── k=14 (G_2 adj): -ln(Λ/M_Pl⁴) ≈ Σ_14 = 281 (0.07%★)
                  ├── k=21 (b_2(K3)): -ln(η_B) ≈ Σ_21 = 791 (24% — weak)
                  └── Z = 2.12σ marginal globally


              [F∞ = 9/10] cross-sector multi-hit:
                  ├── YM-SD saturation polynomial
                  ├── Hadron K_ASP coefficient
                  └── Misc-NT-Bianchi (DW 2D YM)


              [A_CKM = 19/23] CKM/PMNS /23 cluster:
                  ├── A_CKM
                  ├── η_bar = 8/23
                  └── sin²θ₁₂_PMNS = 7/23


              [/13 cluster] EW family:
                  ├── sin²θ_W = 3/13
                  └── cos²θ_W = 10/13

"""
print(network)


# ============================
# SAVE all bridges as JSON
# ============================
out = {
    'date': '2026-05-27',
    'description': 'Cross-sector bridge map : anchors ↔ Bianchi ↔ Riemann',
    'anchors_to_observations': {a: {'value': v[0], 'origin': v[1], 'n_hits': len(bridges_anchor_to_obs[a]['hits']),
                                     'sectors': sorted(set(h['sector'] for h in bridges_anchor_to_obs[a]['hits']))}
                                 for a, v in anchors.items()},
    'bianchi_geometric_keywords': {k: {'n_hits': len(v), 'sectors': sorted(set(h['sector'] for h in v))} for k, v in bianchi_hits.items()},
    'riemann_zeta_keywords': {k: {'n_hits': len(v), 'sectors': sorted(set(h['sector'] for h in v))} for k, v in zeta_hits.items()},
    'strong_cross_sector_bridges_3plus_sectors': strong_bridges,
}
with open('/root/cc-private/papers/BRIDGE_MAP_decoder.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /root/cc-private/papers/BRIDGE_MAP_decoder.json")
print("\n=== END ===")
