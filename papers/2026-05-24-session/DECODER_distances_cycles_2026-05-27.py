#!/usr/bin/env python3
"""
DECODER DISTANCES + CYCLES + FEEDBACK LOOPS — endocrine-style analysis.

Analogie endocrinienne :
- Anchors = hormones (signaux régulateurs)
- Sectors = tissus/organes (cibles)
- Edges = liaisons récepteur-ligand
- Cycles = boucles rétroaction +/-
- Distances = longueur pathway signal
- Hubs = glandes maîtres (hypothalamus-like)

Output :
- Distance matrix (heatmap) entre tous les anchors
- Cycle detection (boucles de rétroaction)
- Strongly connected components (signal flow closed)
- Bottlenecks (single point of failure)
- Passages détaillés (paths explicits)

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json
import numpy as np
import networkx as nx
from collections import defaultdict

# Load decoder graph
with open('/root/cc-private/papers/DECODER_GRAPH.json') as f:
    g_data = json.load(f)

# Rebuild networkx graph
G = nx.DiGraph()
for nid, attrs in g_data['nodes'].items():
    G.add_node(nid, **attrs)
for e in g_data['edges']:
    G.add_edge(e['src'], e['dst'], type=e['type'], label=e['label'])

print(f"=== DECODER GRAPH analysis ===", flush=True)
print(f"  Nodes : {G.number_of_nodes()}", flush=True)
print(f"  Edges : {G.number_of_edges()}", flush=True)
print(f"  Directed : {G.is_directed()}", flush=True)

# ============================
# ANALYSIS 1 : ALL-PAIRS DISTANCES
# ============================
print(f"\n=== ANALYSIS 1 : Distances entre anchors ===", flush=True)

# Anchors only (skip sectors and observables)
anchors = [n for n, a in G.nodes(data=True) if a.get('kind') == 'anchor']
print(f"  {len(anchors)} anchors", flush=True)

# Undirected for distance (paths exist either way)
G_u = G.to_undirected()
dist_matrix = {}
for src in anchors:
    dist_matrix[src] = {}
    try:
        paths = nx.single_source_shortest_path_length(G_u, src)
        for dst in anchors:
            dist_matrix[src][dst] = paths.get(dst, -1)
    except nx.NetworkXError:
        pass

print(f"\n  DISTANCE MATRIX (anchors only) — value = #edges shortest path", flush=True)
print(f"  {'':30s}", end="")
for a in anchors:
    print(f"{a[:8]:>8s}", end="")
print()
for src in anchors:
    print(f"  {src[:30]:30s}", end="")
    for dst in anchors:
        d = dist_matrix[src].get(dst, -1)
        if d == -1: s = "∞"
        elif d == 0: s = "·"
        else: s = str(d)
        print(f"{s:>8s}", end="")
    print()

# ============================
# ANALYSIS 2 : SPECIFIC PASSAGES (paths)
# ============================
print(f"\n=== ANALYSIS 2 : Passages between key anchors ===", flush=True)

key_pairs = [
    ('κ_FP=1/6', 'Koide K=2/3'),
    ('κ_FP=1/6', 'ζ(3)/√π=κ_∞'),
    ('κ_FP=1/6', 'ξ★=2/3'),
    ('Riemann_ζ(3)', 'm_H=125.10'),  # Riemann to mass
    ('Δ_FP', 'Koide K=2/3'),  # spectral to Yukawa
    ('K3_topology', '7=dim G_2'),  # Calabi-Yau to G_2
    ('Bianchi_id', 'ξ★=2/3'),  # geometric to boundary
    ('4/π²≈2/5', 'Λ_obs'),  # universal const to observable
    ('Σ_14=281', 'Λ_obs'),  # metaselector to observable
    ('7=dim G_2', 'b_2(K3)=22'),  # G_2 to K3
]

passages = []
for src, dst in key_pairs:
    if src in G_u.nodes and dst in G_u.nodes:
        try:
            path = nx.shortest_path(G_u, src, dst)
            edges_info = []
            for i in range(len(path)-1):
                a, b = path[i], path[i+1]
                # Try both directions
                if G.has_edge(a, b):
                    t = G[a][b].get('type', '?')
                    l = G[a][b].get('label', '')
                elif G.has_edge(b, a):
                    t = G[b][a].get('type', '?')
                    l = G[b][a].get('label', '')
                else:
                    t, l = '?', ''
                edges_info.append((a, b, t, l))
            passages.append({'src': src, 'dst': dst, 'path': path, 'edges': edges_info})
            print(f"\n  📍 {src}  →  {dst}  (distance = {len(path)-1})", flush=True)
            for a, b, t, l in edges_info:
                print(f"    {a}", flush=True)
                print(f"      │ {t} : {l}", flush=True)
            print(f"    {dst}", flush=True)
        except nx.NetworkXNoPath:
            print(f"\n  ❌ NO PATH between {src} and {dst}", flush=True)
            passages.append({'src': src, 'dst': dst, 'path': None})


# ============================
# ANALYSIS 3 : CYCLES (feedback loops)
# ============================
print(f"\n=== ANALYSIS 3 : Cycles (boucles de rétroaction) ===", flush=True)

# Find all simple cycles up to length 6 (computationally feasible)
G_u_for_cycles = nx.Graph()
G_u_for_cycles.add_nodes_from(G.nodes())
G_u_for_cycles.add_edges_from(G.to_undirected().edges())

try:
    cycles = list(nx.simple_cycles(G, length_bound=6))
    print(f"  {len(cycles)} cycles found (length ≤ 6)", flush=True)

    # Group by length
    cycles_by_len = defaultdict(list)
    for c in cycles:
        cycles_by_len[len(c)].append(c)

    for cl in sorted(cycles_by_len.keys()):
        clst = cycles_by_len[cl]
        print(f"\n  Length {cl} : {len(clst)} cycles", flush=True)
        for c in clst[:5]:
            print(f"    {' → '.join(c)} → ...", flush=True)
except Exception as ex:
    print(f"  Cycle detection failed : {ex}", flush=True)
    cycles = []

# Undirected cycles (feedback loops both directions)
print(f"\n=== Undirected cycle basis (boucles topologiques) ===", flush=True)
try:
    cycle_basis = nx.cycle_basis(G.to_undirected())
    print(f"  {len(cycle_basis)} independent cycles in undirected graph", flush=True)
    cycle_basis.sort(key=len)
    for i, c in enumerate(cycle_basis[:10]):
        print(f"    Cycle {i+1} (len {len(c)}): {c}", flush=True)
except Exception as ex:
    print(f"  Undirected cycle failed : {ex}", flush=True)


# ============================
# ANALYSIS 4 : STRONGLY CONNECTED (closed signal loops)
# ============================
print(f"\n=== ANALYSIS 4 : Strongly connected components ===", flush=True)
sccs = list(nx.strongly_connected_components(G))
sccs.sort(key=lambda c: -len(c))
print(f"  {len(sccs)} strongly connected components", flush=True)
for i, scc in enumerate(sccs[:10]):
    if len(scc) >= 2:
        print(f"    SCC {i+1} ({len(scc)} nodes): {sorted(scc)}", flush=True)


# ============================
# ANALYSIS 5 : DIAMETER + AVERAGE PATH LENGTH
# ============================
print(f"\n=== ANALYSIS 5 : Global metrics ===", flush=True)
try:
    diameter = nx.diameter(G_u)
    avg_path = nx.average_shortest_path_length(G_u)
    print(f"  Diameter (longest shortest path) : {diameter}", flush=True)
    print(f"  Average shortest path : {avg_path:.2f}", flush=True)
except nx.NetworkXError:
    # graph not connected, use largest component
    largest_cc = max(nx.connected_components(G_u), key=len)
    print(f"  Graph not connected, largest CC has {len(largest_cc)} nodes", flush=True)
    sub = G_u.subgraph(largest_cc)
    diameter = nx.diameter(sub)
    avg_path = nx.average_shortest_path_length(sub)
    print(f"  Diameter (largest CC) : {diameter}", flush=True)
    print(f"  Average shortest path (largest CC) : {avg_path:.2f}", flush=True)


# ============================
# ANALYSIS 6 : Identify FEEDBACK LOOPS (endocrine-style)
# ============================
print(f"\n=== ANALYSIS 6 : Endocrine-style feedback loops ===", flush=True)
print(f"  (Cycles passing through ≥2 communities = cross-community feedback)")

# Get communities
G_u_comm = G.to_undirected()
communities = list(nx.community.label_propagation_communities(G_u_comm))
node_to_comm = {}
for i, c in enumerate(communities):
    for n in c:
        node_to_comm[n] = i

# Find cycles that cross communities
cross_comm_cycles = []
if cycles:
    for c in cycles:
        comms_in_cycle = set(node_to_comm.get(n, -1) for n in c)
        if len(comms_in_cycle) >= 2:
            cross_comm_cycles.append((c, comms_in_cycle))

print(f"\n  {len(cross_comm_cycles)} cycles crossing ≥2 communities", flush=True)
for c, comms in cross_comm_cycles[:10]:
    print(f"    {' → '.join(c)} (passes through communities {sorted(comms)})", flush=True)


# ============================
# ANALYSIS 7 : Bottlenecks (cut nodes)
# ============================
print(f"\n=== ANALYSIS 7 : Bottlenecks (cut vertices) ===", flush=True)
print(f"  Nodes whose removal disconnects the graph (single points of failure)")
cuts = list(nx.articulation_points(G_u))
print(f"  {len(cuts)} cut vertices", flush=True)
for c in cuts[:15]:
    print(f"    [BOTTLENECK] {c}", flush=True)


# ============================
# SAVE comprehensive analysis
# ============================
out = {
    'date': '2026-05-27',
    'n_nodes': G.number_of_nodes(),
    'n_edges': G.number_of_edges(),
    'distance_matrix_anchors': {src: dict(d) for src, d in dist_matrix.items()},
    'passages_key_pairs': [{'src': p['src'], 'dst': p['dst'],
                             'distance': len(p['path'])-1 if p.get('path') else None,
                             'path': p.get('path'),
                             'edges': [(a,b,t,l) for a,b,t,l in p.get('edges', [])]} for p in passages],
    'cycles_short': [list(c) for c in cycles[:50]] if cycles else [],
    'cycles_count_by_length': {str(cl): len(lst) for cl, lst in cycles_by_len.items()} if cycles else {},
    'strongly_connected_components': [sorted(scc) for scc in sccs if len(scc) >= 2],
    'cross_community_feedback_loops': [{'cycle': list(c), 'communities': sorted(list(comms))} for c, comms in cross_comm_cycles[:30]],
    'cut_vertices_bottlenecks': cuts,
    'diameter': diameter,
    'avg_shortest_path': float(avg_path),
}
with open('/root/cc-private/papers/DECODER_DISTANCES_CYCLES.json', 'w') as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n→ Saved /root/cc-private/papers/DECODER_DISTANCES_CYCLES.json")
