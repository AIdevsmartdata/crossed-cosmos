#!/usr/bin/env python3
"""
MAP DECODER GRAPH — networkx full graph with typed edges + visualization.

Edges types :
- EXACT : algebraic identity (e.g., 4·κ_FP = Koide K)
- DERIVED : theorem path (e.g., κ_FP = R/6 Kostant)
- SHARED : same numerical value across sectors
- STRUCTURAL : group-theoretic link (e.g., dim G_2 = 7)
- PHYSICAL : hypothesized mechanism (e.g., Σ_p_k=14 ↔ Λ)
- CONJECTURAL : not yet derived (e.g., d_s=7/3)

Output :
- JSON graph (machine-readable)
- Mermaid diagram (markdown-friendly)
- Centrality analysis

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json
from collections import defaultdict

# Build graph manually based on findings
# Format: {node_id: {sector, value, type}}

NODES = {
    # === ANCHORS (8 super-nodes ≥3 sectors + secondary) ===
    'κ_FP=1/6':      {'kind': 'anchor', 'value': 1/6, 'origin': 'Kostant theorem', 'tier': 'EXACT'},
    'F∞=9/10':       {'kind': 'anchor', 'value': 9/10, 'origin': 'saturation poly', 'tier': 'EXACT'},
    'c∞=1/4':        {'kind': 'anchor', 'value': 1/4, 'origin': 'Bekenstein BH', 'tier': 'EXACT'},
    'ξ★=2/3':        {'kind': 'anchor', 'value': 2/3, 'origin': 'BG SD a_1', 'tier': 'CONJECTURE'},
    'b_0=11N/(48π²)':{'kind': 'anchor', 'value': 11/3, 'origin': 'Vassilevich a_4', 'tier': 'EXACT'},
    '4/π²≈2/5':      {'kind': 'anchor', 'value': 4/3.14159**2, 'origin': '???', 'tier': 'EMPIRICAL'},
    'ζ(3)/√π=κ_∞':   {'kind': 'anchor', 'value': 0.6782, 'origin': 'Apéry × √π', 'tier': 'EMPIRICAL'},
    'b_2(K3)=22':    {'kind': 'anchor', 'value': 22, 'origin': 'K3 cohomology', 'tier': 'THEOREM_topology'},
    '24=Niemeier':   {'kind': 'anchor', 'value': 24, 'origin': 'Conway lattice', 'tier': 'THEOREM_topology'},
    '7=dim G_2':     {'kind': 'anchor', 'value': 7, 'origin': 'G_2 fund repr', 'tier': 'THEOREM_GT'},
    '1/2':           {'kind': 'anchor', 'value': 0.5, 'origin': 'Lie/SD multi', 'tier': 'STRUCTURAL'},

    # === SECONDARY NODES (≥2 sectors) ===
    'd_s=3 (GZ)':    {'kind': 'derived', 'value': 3, 'origin': '1+D/z (z=2)', 'tier': 'EXACT'},
    'd_s=7/3':       {'kind': 'derived', 'value': 7/3, 'origin': '1+D/z (z=3 refined)', 'tier': 'CONJECTURE'},
    'sin²θ_W=3/13':  {'kind': 'rational', 'value': 3/13, 'origin': 'EW empirical', 'tier': 'EMPIRICAL'},
    'cos²θ_W=10/13': {'kind': 'rational', 'value': 10/13, 'origin': 'EW empirical', 'tier': 'EMPIRICAL'},
    'A_CKM=19/23':   {'kind': 'rational', 'value': 19/23, 'origin': 'CKM empirical', 'tier': 'EMPIRICAL'},
    'Koide K=2/3':   {'kind': 'identity', 'value': 2/3, 'origin': '4·κ_FP(SU(3))', 'tier': 'EXACT_emp'},
    'Σ_8=77':        {'kind': 'metaselector', 'value': 77, 'origin': 'sum first 8 primes', 'tier': 'EMPIRICAL'},
    'Σ_14=281':      {'kind': 'metaselector', 'value': 281, 'origin': 'sum first 14 primes', 'tier': 'EMPIRICAL'},
    'Σ_21=791':      {'kind': 'metaselector', 'value': 791, 'origin': 'sum first 21 primes', 'tier': 'EMPIRICAL'},
    'dim SU(N)=N²-1':{'kind': 'group_inv', 'value': None, 'origin': 'Lie algebra', 'tier': 'EXACT'},

    # === SECTORS (visual grouping) ===
    'SECTOR_YM-SD':       {'kind': 'sector', 'name': 'Yang-Mills Seeley-DeWitt'},
    'SECTOR_YM-lattice':  {'kind': 'sector', 'name': 'YM lattice κ_EE'},
    'SECTOR_EW':          {'kind': 'sector', 'name': 'Electroweak'},
    'SECTOR_Yukawa':      {'kind': 'sector', 'name': 'Yukawa fermion masses'},
    'SECTOR_Hadrons':     {'kind': 'sector', 'name': 'Hadrons + glueballs'},
    'SECTOR_CKM':         {'kind': 'sector', 'name': 'CKM mixing'},
    'SECTOR_Cosmology':   {'kind': 'sector', 'name': 'Cosmology Λ, η_B'},
    'SECTOR_Group':       {'kind': 'sector', 'name': 'Group theory'},
    'SECTOR_d_s-decoder': {'kind': 'sector', 'name': 'Spectral dim decoder'},
    'SECTOR_Σ_p':         {'kind': 'sector', 'name': 'Σ_premiers metaselector'},
    'SECTOR_Bianchi':     {'kind': 'sector', 'name': 'Bianchi NT misc'},

    # === GEOMETRIC/THEORETICAL ROOTS ===
    'YM_action':     {'kind': 'root', 'value': 'S = (1/4g²)∫F²', 'tier': 'AXIOM'},
    'A/G_Gribov':    {'kind': 'theory', 'value': 'gauge orbit space', 'tier': 'AXIOM'},
    'Δ_FP':          {'kind': 'theory', 'value': 'Faddeev-Popov Laplacian', 'tier': 'AXIOM'},
    'Bianchi_id':    {'kind': 'theory', 'value': 'D_μ F^{μν}=0', 'tier': 'AXIOM'},
    'Hořava-Lifshitz':{'kind':'theory', 'value': 'd_s = 1+D/z', 'tier': 'THEOREM'},
    'Branson-Gilkey':{'kind': 'theory', 'value': 'heat kernel SD', 'tier': 'THEOREM'},
    'K3_topology':   {'kind': 'theory', 'value': 'Calabi-Yau b_2=22', 'tier': 'THEOREM'},
    'Riemann_ζ(3)':  {'kind': 'theory', 'value': 'Apéry constant', 'tier': 'THEOREM'},

    # === ROOT OBSERVABLES (a few key) ===
    'm_H=125.10':    {'kind': 'observable', 'value': 125.10, 'sector': 'EW'},
    'v=246.22':      {'kind': 'observable', 'value': 246.22, 'sector': 'EW'},
    'm_Z=91.187':    {'kind': 'observable', 'value': 91.187, 'sector': 'EW'},
    'Λ_obs':         {'kind': 'observable', 'value': 1.105e-122, 'sector': 'Cosmology'},
    'η_B':           {'kind': 'observable', 'value': 6.12e-10, 'sector': 'Cosmology'},
}

# EDGES typed
EDGES = [
    # === Theoretical roots → spectrum ===
    ('YM_action', 'A/G_Gribov', 'DERIVED', 'gauge fixing'),
    ('A/G_Gribov', 'Δ_FP', 'DERIVED', 'FP operator def'),
    ('Δ_FP', 'd_s=3 (GZ)', 'DERIVED', 'spectral via z=2 GZ standard'),
    ('Δ_FP', 'd_s=7/3', 'CONJECTURAL', 'refined GZ + Hořava'),
    ('Δ_FP', 'κ_FP=1/6', 'EXACT', 'Kostant a_2 coefficient'),
    ('Δ_FP', 'ξ★=2/3', 'CONJECTURAL', 'BG boundary a_1'),
    ('Δ_FP', 'b_0=11N/(48π²)', 'EXACT', 'Vassilevich Eq 4.34'),
    ('Hořava-Lifshitz', 'd_s=3 (GZ)', 'EXACT', '1+4/2=3 z=2'),
    ('Hořava-Lifshitz', 'd_s=7/3', 'EXACT', '1+4/3=7/3 z=3'),
    ('Branson-Gilkey', 'κ_FP=1/6', 'EXACT', 'a_2 bulk coefficient'),
    ('Branson-Gilkey', 'ξ★=2/3', 'CONJECTURAL', 'a_1 boundary fractal'),
    ('Bianchi_id', 'YM_action', 'AXIOM', 'F closed 2-form'),
    ('K3_topology', 'b_2(K3)=22', 'EXACT', 'Calabi-Yau cohomology'),
    ('K3_topology', '24=Niemeier', 'STRUCTURAL', 'Niemeier lattice Conway'),
    ('Riemann_ζ(3)', 'ζ(3)/√π=κ_∞', 'EXACT', 'Apéry × √π'),

    # === EXACT identities (algebraic) ===
    ('κ_FP=1/6', 'Koide K=2/3', 'EXACT', '4·κ_FP(SU(3)) = K_lepton'),
    ('κ_FP=1/6', 'ξ★=2/3', 'EXACT', '4·κ_FP = ξ★'),
    ('Koide K=2/3', 'ξ★=2/3', 'EXACT', 'same value 2/3 multi-origin'),
    ('sin²θ_W=3/13', 'cos²θ_W=10/13', 'EXACT', 'sum = 1'),
    ('b_2(K3)=22', '24=Niemeier', 'STRUCTURAL', 'b_2 + 2 vacuum = 24 (string theory)'),
    ('Σ_8=77', '8', 'STRUCTURAL', 'k=8=dim SU(3) adj'),
    ('Σ_14=281', '7=dim G_2', 'STRUCTURAL', 'k=14=dim G_2 adj'),
    ('Σ_21=791', 'b_2(K3)=22', 'STRUCTURAL', 'k=21=b_2(K3)-1'),

    # === Anchor → Sector (which anchors appear in which sectors) ===
    ('κ_FP=1/6', 'SECTOR_YM-SD', 'SHARED', 'a_2 coefficient'),
    ('κ_FP=1/6', 'SECTOR_Yukawa', 'SHARED', 'Koide identity'),
    ('κ_FP=1/6', 'SECTOR_d_s-decoder', 'SHARED', 'Nakagawa α_FP fit'),
    ('F∞=9/10', 'SECTOR_YM-SD', 'SHARED', 'saturation polynomial'),
    ('F∞=9/10', 'SECTOR_Hadrons', 'SHARED', 'K_ASP coefficient'),
    ('F∞=9/10', 'SECTOR_Bianchi', 'SHARED', 'DW 2D YM Z_0/(Z_0+Z_1)'),
    ('ζ(3)/√π=κ_∞', 'SECTOR_YM-lattice', 'SHARED', 'κ_∞ dilute asymptote'),
    ('ζ(3)/√π=κ_∞', 'SECTOR_CKM', 'SHARED', 'A² ≈ ζ(3)/√π'),
    ('4/π²≈2/5', 'SECTOR_EW', 'SHARED', 'α_s = 2/5'),
    ('4/π²≈2/5', 'SECTOR_Cosmology', 'SHARED', 'Λ via Arefieva J(τ)'),
    ('24=Niemeier', 'SECTOR_Group', 'SHARED', 'dim SU(5)'),
    ('24=Niemeier', 'SECTOR_Σ_p', 'SHARED', 'k=21 weight'),
    ('24=Niemeier', 'SECTOR_Bianchi', 'SHARED', 'Lichtenbaum'),
    ('7=dim G_2', 'SECTOR_Group', 'SHARED', 'dim G_2 fund'),
    ('7=dim G_2', 'SECTOR_YM-SD', 'SHARED', 'd_s=7/3 numerator'),
    ('7=dim G_2', 'SECTOR_d_s-decoder', 'SHARED', 'spectral dim conjecture'),
    ('b_2(K3)=22', 'SECTOR_Group', 'SHARED', 'b_2(K3) topology'),
    ('b_2(K3)=22', 'SECTOR_Σ_p', 'SHARED', 'k=21=b_2-1 → exp(-21)'),
    ('b_2(K3)=22', 'SECTOR_Bianchi', 'SHARED', 'Kevin identity Σ(h-1)=b_2'),
    ('sin²θ_W=3/13', 'SECTOR_EW', 'SHARED', 'PDG measured'),
    ('cos²θ_W=10/13', 'SECTOR_EW', 'SHARED', 'PDG measured'),
    ('A_CKM=19/23', 'SECTOR_CKM', 'SHARED', 'CKM matrix element'),
    ('Koide K=2/3', 'SECTOR_Yukawa', 'SHARED', 'lepton K=4·κ_FP'),
    ('c∞=1/4', 'SECTOR_YM-SD', 'SHARED', 'Bianchi/Wilson D=4'),
    ('b_0=11N/(48π²)', 'SECTOR_YM-SD', 'SHARED', 'one-loop β-function'),
    ('d_s=3 (GZ)', 'SECTOR_d_s-decoder', 'SHARED', 'GZ standard z=2'),
    ('d_s=3 (GZ)', 'SECTOR_YM-SD', 'SHARED', 'candidate'),
    ('d_s=7/3', 'SECTOR_d_s-decoder', 'SHARED', 'refined GZ conjecture'),
    ('dim SU(N)=N²-1', 'SECTOR_Group', 'SHARED', 'Lie algebra'),
    ('dim SU(N)=N²-1', 'SECTOR_YM-lattice', 'SHARED', 'leading κ_EE ~ N²'),

    # === PHYSICAL mechanisms (Σ_p metaselector) ===
    ('Σ_8=77', 'SECTOR_Cosmology', 'CONJECTURAL', 'ln(M_Pl/v)² ≈ 77 at 4.3%'),
    ('Σ_14=281', 'SECTOR_Cosmology', 'CONJECTURAL', '-ln(Λ/M_Pl⁴) ≈ 281 at 0.07%'),
    ('Σ_21=791', 'SECTOR_Cosmology', 'CONJECTURAL', '-ln(η_B) ≈ 21 at 24% (weak)'),
]


# ============================
# BUILD networkx graph
# ============================
try:
    import networkx as nx
    G = nx.DiGraph()
    for nid, attrs in NODES.items():
        G.add_node(nid, **attrs)
    for src, dst, edge_type, label in EDGES:
        G.add_edge(src, dst, type=edge_type, label=label)

    print(f"=== Graph built ===")
    print(f"  Nodes : {G.number_of_nodes()}")
    print(f"  Edges : {G.number_of_edges()}")

    # === Centrality analysis ===
    print(f"\n=== Centrality measures ===")
    # Degree centrality
    deg_cen = nx.degree_centrality(G)
    print(f"\n  Top 10 by degree centrality (most connected) :")
    for nid, c in sorted(deg_cen.items(), key=lambda x: -x[1])[:15]:
        print(f"    {nid:30s} : {c:.3f}")

    # Betweenness centrality (which nodes bridge the most)
    btw_cen = nx.betweenness_centrality(G.to_undirected())
    print(f"\n  Top 10 by betweenness (bridges) :")
    for nid, c in sorted(btw_cen.items(), key=lambda x: -x[1])[:10]:
        print(f"    {nid:30s} : {c:.3f}")

    # Find communities (Louvain or label propagation)
    print(f"\n=== Communities (label propagation) ===")
    G_undir = G.to_undirected()
    communities = list(nx.community.label_propagation_communities(G_undir))
    print(f"  {len(communities)} communities found")
    for i, comm in enumerate(communities[:10]):
        members = sorted(list(comm))[:8]
        print(f"  Community {i+1} ({len(comm)} nodes): {members}")

    # Save graph
    pass  # GEXF skipped (type issue)
    pass
except ImportError:
    print("networkx not installed locally, skipping graph analysis")
    G = None


# ============================
# Export as Mermaid diagram
# ============================
print(f"\n=== Mermaid diagram ===\n")

mermaid = ["graph TD"]
mermaid.append("    %% Theoretical roots")
for nid, attrs in NODES.items():
    if attrs.get('kind') in ('root', 'theory'):
        label = nid.replace('_', ' ').replace('=', '_eq_')
        mermaid.append(f"    {nid.replace('/','_')}[{label}]:::theory")

mermaid.append("    %% Anchors (super-nodes)")
for nid, attrs in NODES.items():
    if attrs.get('kind') == 'anchor':
        nid_safe = nid.replace('/','_').replace('π','pi').replace('²','2').replace('★','star').replace('=','_eq_').replace('≈','_approx_').replace('₂','2').replace('(','_').replace(')','_')
        label = nid
        tier = attrs.get('tier', '')
        cls = 'exact' if tier=='EXACT' else 'emp' if tier=='EMPIRICAL' else 'conj'
        mermaid.append(f"    {nid_safe}((\"{label}\")):::​{cls}")

mermaid.append("    %% Edges")
edge_count = 0
for src, dst, etype, label in EDGES[:40]:  # limit for readability
    src_safe = src.replace('/','_').replace('π','pi').replace('²','2').replace('★','star').replace('=','_eq_').replace('≈','_approx_').replace('₂','2').replace('(','_').replace(')','_').replace('∞','inf').replace('Σ','S').replace('κ','k').replace('ξ','xi').replace('ζ','zeta').replace('Δ','D').replace(' ','_')
    dst_safe = dst.replace('/','_').replace('π','pi').replace('²','2').replace('★','star').replace('=','_eq_').replace('≈','_approx_').replace('₂','2').replace('(','_').replace(')','_').replace('∞','inf').replace('Σ','S').replace('κ','k').replace('ξ','xi').replace('ζ','zeta').replace('Δ','D').replace(' ','_')
    if etype == 'EXACT':
        mermaid.append(f"    {src_safe} ==>|EXACT| {dst_safe}")
    elif etype == 'DERIVED':
        mermaid.append(f"    {src_safe} -->|DERIVED| {dst_safe}")
    elif etype == 'CONJECTURAL':
        mermaid.append(f"    {src_safe} -.->|CONJ| {dst_safe}")
    elif etype == 'SHARED':
        mermaid.append(f"    {src_safe} -->|SHARED| {dst_safe}")
    else:
        mermaid.append(f"    {src_safe} ---|{etype}| {dst_safe}")
    edge_count += 1

mermaid_text = "\n".join(mermaid)
with open('/tmp/decoder_graph.mermaid', 'w') as f:
    f.write(mermaid_text)
print(f"  Mermaid diagram with {edge_count} edges → /tmp/decoder_graph.mermaid")


# ============================
# Save full graph JSON
# ============================
out = {
    'description': 'Decoder graph : 8 super-nodes + secondary + theoretical roots + sectors',
    'date': '2026-05-27',
    'n_nodes': len(NODES),
    'n_edges': len(EDGES),
    'nodes': NODES,
    'edges': [{'src': s, 'dst': d, 'type': t, 'label': l} for s,d,t,l in EDGES],
}
if G is not None:
    out['top_degree_centrality'] = sorted(nx.degree_centrality(G).items(), key=lambda x:-x[1])[:15]
    out['top_betweenness'] = sorted(nx.betweenness_centrality(G.to_undirected()).items(), key=lambda x:-x[1])[:10]

with open('/root/cc-private/papers/DECODER_GRAPH.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /root/cc-private/papers/DECODER_GRAPH.json")
