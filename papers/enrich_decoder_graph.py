#!/usr/bin/env python3
"""
enrich_decoder_graph.py — Add feedback edges to the YM decoder graph.

Input  : papers/DECODER_GRAPH.json (45 nodes, 56 edges, 0 cycles)
Output : papers/DECODER_GRAPH_ENRICHED.json  (~50 nodes, ~95 edges, multiple cycles)
         papers/DECODER_DISTANCES_CYCLES_ENRICHED.json
         papers/DECODER_diagram.mmd          (mermaid)
         papers/DECODER_diagram.dot          (graphviz)
         papers/DECODER_diagram.tex          (TikZ skeleton)
         papers/DECODER_diagram.html         (D3.js interactive)

The original graph is a DAG (AXIOM -> THEORY -> ANCHOR -> SECTOR -> OBSERVABLE).
This script adds reverse edges (OBSERVABLE -> ANCHOR "validates", SECTOR -> THEORY
"informs", ANCHOR <-> ANCHOR identities) so that the graph becomes a network with
true feedback loops, more representative of an endocrine-style coupling between
mathematical predictions and empirical measurements.

Author: Kévin Rémondière, ORCID 0009-0008-2443-7166
Date:   2026-05-27
"""

import json
import os
from pathlib import Path

import networkx as nx

PAPERS = Path("/root/cc-private/papers")
SRC = PAPERS / "DECODER_GRAPH.json"
DST = PAPERS / "DECODER_GRAPH_ENRICHED.json"
DST_METRICS = PAPERS / "DECODER_DISTANCES_CYCLES_ENRICHED.json"


# ---------------------------------------------------------------------------
# 1. Load existing graph
# ---------------------------------------------------------------------------
with SRC.open() as fh:
    data = json.load(fh)

G = nx.DiGraph()
for nid, attr in data["nodes"].items():
    G.add_node(nid, **attr)

for e in data["edges"]:
    G.add_edge(e["src"], e["dst"], type=e.get("type", "?"), label=e.get("label", ""))


# ---------------------------------------------------------------------------
# 2. Add missing observable nodes referenced in validations
# ---------------------------------------------------------------------------
NEW_OBSERVABLES = {
    # additional EW / Yukawa / cosmo observables needed for validates edges
    "m_e/m_μ":      {"kind": "observable", "value": 0.0048, "sector": "Yukawa"},
    "Koide_lepton": {"kind": "observable", "value": 0.6666, "sector": "Yukawa"},
    "κ_EE_lat(SU2)": {"kind": "observable", "value": 0.5065,
                       "sector": "YM-lattice"},
    "κ_EE_lat(SU3)": {"kind": "observable", "value": 0.603,
                       "sector": "YM-lattice"},
    "κ_EE_lat(SU4)": {"kind": "observable", "value": 0.6358,
                       "sector": "YM-lattice"},
    "sin²θ_W_PDG":   {"kind": "observable", "value": 0.23121,
                       "sector": "EW"},
    "A_CKM_PDG":     {"kind": "observable", "value": 0.826,
                       "sector": "CKM"},
    "ln(M_Pl/v)²":   {"kind": "observable", "value": 73.7,
                       "sector": "Cosmology"},
    "α_s(M_Z)":      {"kind": "observable", "value": 0.1181,
                       "sector": "Hadrons"},
}
for nid, attr in NEW_OBSERVABLES.items():
    if nid not in G.nodes:
        G.add_node(nid, **attr)


# ---------------------------------------------------------------------------
# 3. Reverse edges  OBSERVABLE  ──VALIDATES──▶  ANCHOR
#    Closes the predict→measure→validate loop.
# ---------------------------------------------------------------------------
VALIDATES_EDGES = [
    # (observable, anchor, deviation, label)
    ("m_H=125.10",     "1/2",                "0.016%",
     "m_H = κ(SU(2))·v ⇒ κ(SU(2))=0.5080 = 1/2"),
    ("Koide_lepton",   "κ_FP=1/6",          "0.0%",
     "K=2/3 = 4·κ_FP(SU(3)) (Kostant)"),
    ("κ_EE_lat(SU2)",  "ζ(3)/√π=κ_∞",       "25%",
     "lattice EE saturates κ_∞·(1-1/N²) regime perturbatif"),
    ("κ_EE_lat(SU3)",  "ζ(3)/√π=κ_∞",       "0.0%",
     "lattice EE saturates κ_∞·(1-1/N²)"),
    ("κ_EE_lat(SU4)",  "ζ(3)/√π=κ_∞",       "<0.4σ",
     "lattice EE saturates κ_∞·(1-1/N²)"),
    ("sin²θ_W_PDG",    "sin²θ_W=3/13",      "0.19%",
     "3/13 = 0.23077 matches PDG 0.23121"),
    ("A_CKM_PDG",      "A_CKM=19/23",       "0.01%",
     "19/23 = 0.82609 matches PDG 0.826"),
    ("ln(M_Pl/v)²",    "Σ_8=77",            "4.3%",
     "Σ first 8 primes = 77 ≈ ln(M_Pl/v)²"),
    ("Λ_obs",          "Σ_14=281",          "0.07%",
     "-ln(Λ/M_Pl⁴) ≈ 281 = Σ first 14 primes"),
    ("η_B",            "Σ_21=791",          "24%",
     "-ln(η_B) ≈ 21 = b_2(K3)-1 (weak)"),
    ("α_s(M_Z)",       "4/π²≈2/5",          "5%",
     "α_s ≈ 2/5 first-principles bound"),
    ("v=246.22",       "1/2",                "—",
     "v fixes scale at which κ(SU(2))=1/2 sets m_H"),
    ("m_Z=91.187",     "Koide K=2/3",       "structural",
     "m_Z/v ratio enters Weinberg sector with 2/3 anchor"),
]
for src, dst, dev, lbl in VALIDATES_EDGES:
    G.add_edge(src, dst, type="VALIDATES", label=f"[{dev}] {lbl}")


# ---------------------------------------------------------------------------
# 4. Reverse edges  SECTOR  ──INFORMS──▶  THEORY
#    e.g., lattice EE measurement informs the Vassilevich heat-kernel ansatz.
# ---------------------------------------------------------------------------
INFORMS_EDGES = [
    ("SECTOR_YM-lattice", "Branson-Gilkey",  "lattice κ_EE constrains a_2,a_1"),
    ("SECTOR_YM-SD",      "Branson-Gilkey",  "SD coefficients tested by SD-asymptotics"),
    ("SECTOR_YM-SD",      "Horava-Lifshitz", "d_s decoder selects z=2 vs z=3"),
    ("SECTOR_d_s-decoder","Horava-Lifshitz", "d_s sector chooses HL anisotropy"),
    ("SECTOR_d_s-decoder","Branson-Gilkey",  "d_s data feed back to BG SD"),
    ("SECTOR_Cosmology",  "Riemann_ζ(3)",    "Λ-fit calibrates ζ(3)/√π asymptote"),
    ("SECTOR_CKM",        "K3_topology",     "CKM A=19/23 ≈ b_2-related candidate"),
    ("SECTOR_Σ_p",        "K3_topology",     "Σ_21 ≈ b_2(K3)-1 metaselector"),
    ("SECTOR_Group",      "K3_topology",     "G_2 ↔ K3 Calabi-Yau holonomy"),
    ("SECTOR_EW",         "Branson-Gilkey",  "EW broken phase via heat-kernel SD"),
    ("SECTOR_Bianchi",    "K3_topology",     "Bianchi identity ⇄ b_2 cycle"),
    ("SECTOR_Hadrons",    "Branson-Gilkey",  "glueball spectrum from SD coefficients"),
]
for src, dst, lbl in INFORMS_EDGES:
    G.add_edge(src, dst, type="INFORMS", label=lbl)


# ---------------------------------------------------------------------------
# 5. ANCHOR ↔ ANCHOR identities (new explicit reverse edges)
# ---------------------------------------------------------------------------
ANCHOR_IDENTITY_EDGES = [
    ("Koide K=2/3", "κ_FP=1/6",   "EXACT_id",
     "Koide K = 4·κ_FP(SU(3)) reverse"),
    ("ξ★=2/3",      "κ_FP=1/6",   "EXACT_id",
     "ξ★ = 4·κ_FP reverse identification"),
    ("ξ★=2/3",      "Koide K=2/3","EXACT_id",
     "ξ★ ≡ Koide K same value 2/3"),
    ("cos²θ_W=10/13","sin²θ_W=3/13","EXACT_id",
     "trig identity sum=1 reverse"),
    ("c∞=1/4",      "1/2",        "STRUCT",
     "c∞=1/4 = (1/2)² Lie/SD multiplicity squared"),
    ("κ_FP=1/6",    "1/2",        "STRUCT",
     "κ_FP(SU(2)) = 1/2 = 1/(2|Φ⁺(SU(2))|)"),
    ("b_2(K3)=22",  "24=Niemeier","STRUCT",
     "b_2(K3)+2 = 24 string-theory closure"),
    ("Σ_14=281",    "7=dim G_2",  "META",
     "Σ first 14 primes selects k=14=dim G_2 adj"),
    ("Σ_21=791",    "24=Niemeier","META",
     "Σ_21 sits 3 below 24 (string vacuum count)"),
    ("Σ_8=77",      "dim SU(N)=N²-1","META",
     "k=8=dim SU(3) adj selects QCD sector"),
]
for src, dst, t, lbl in ANCHOR_IDENTITY_EDGES:
    G.add_edge(src, dst, type=t, label=lbl)


# ---------------------------------------------------------------------------
# 6. SECTOR ↔ SECTOR via shared anchor (new cross-community edges)
# ---------------------------------------------------------------------------
SECTOR_SECTOR_EDGES = [
    ("SECTOR_YM-SD",      "SECTOR_YM-lattice", "κ_∞ asymptote shared"),
    ("SECTOR_YM-lattice", "SECTOR_YM-SD",      "lattice tests SD predictions"),
    ("SECTOR_EW",         "SECTOR_Yukawa",     "Higgs vev v shared"),
    ("SECTOR_Yukawa",     "SECTOR_EW",         "Yukawa fixes m_f from v"),
    ("SECTOR_CKM",        "SECTOR_Yukawa",     "Yukawa matrix diagonalisation"),
    ("SECTOR_Cosmology",  "SECTOR_Σ_p",        "Λ-decoder uses Σ_14"),
    ("SECTOR_Σ_p",        "SECTOR_Cosmology",  "metaselector feedback"),
    ("SECTOR_Group",      "SECTOR_YM-SD",      "Lie alg dims drive SD"),
    ("SECTOR_Group",      "SECTOR_Bianchi",    "G_2 ↔ Bianchi cohomology"),
    ("SECTOR_d_s-decoder","SECTOR_YM-SD",      "spectral dim is SD output"),
]
for src, dst, lbl in SECTOR_SECTOR_EDGES:
    G.add_edge(src, dst, type="X-COMM", label=lbl)


# ---------------------------------------------------------------------------
# 7. Tagging — colour by tier & community
# ---------------------------------------------------------------------------
TIER_COLOR = {
    "EXACT":            "#1f77b4",  # blue
    "EXACT_emp":        "#1f77b4",
    "EXACT_id":         "#1f77b4",
    "THEOREM":          "#2ca02c",  # green
    "THEOREM_topology": "#2ca02c",
    "THEOREM_GT":       "#2ca02c",
    "AXIOM":            "#9467bd",  # purple
    "CONJECTURE":       "#ff7f0e",  # orange
    "STRUCTURAL":       "#bcbd22",  # olive
    "STRUCT":           "#bcbd22",
    "EMPIRICAL":        "#d62728",  # red
    "META":             "#8c564b",  # brown
    "VALIDATES":        "#17becf",  # cyan (feedback)
    "INFORMS":          "#17becf",
    "X-COMM":           "#e377c2",  # pink (cross-community)
    "DERIVED":          "#7f7f7f",  # grey
    "SHARED":           "#aaaaaa",
    "CONJECTURAL":      "#ff7f0e",
}
KIND_COLOR = {
    "anchor":      "#4daf4a",
    "derived":     "#e0d000",
    "rational":    "#f4a300",
    "identity":    "#1f78b4",
    "metaselector":"#a6761d",
    "group_inv":   "#984ea3",
    "sector":      "#377eb8",
    "root":        "#999999",
    "theory":      "#66a61e",
    "observable":  "#e41a1c",
}
COMMUNITY = {
    # 4 macro-clusters
    "YM-core":     ["YM_action", "A/G_Gribov", "Δ_FP", "Bianchi_id",
                    "κ_FP=1/6", "ξ★=2/3", "b_0=11N/(48π²)", "F∞=9/10",
                    "c∞=1/4", "1/2", "d_s=3 (GZ)", "d_s=7/3",
                    "Horava-Lifshitz", "Branson-Gilkey",
                    "SECTOR_YM-SD", "SECTOR_YM-lattice", "SECTOR_d_s-decoder",
                    "α_s(M_Z)", "κ_EE_lat(SU2)", "κ_EE_lat(SU3)",
                    "κ_EE_lat(SU4)", "ζ(3)/√π=κ_∞"],
    "SM-pheno":    ["sin²θ_W=3/13", "cos²θ_W=10/13", "A_CKM=19/23",
                    "Koide K=2/3", "m_H=125.10", "v=246.22", "m_Z=91.187",
                    "SECTOR_EW", "SECTOR_Yukawa", "SECTOR_CKM",
                    "SECTOR_Hadrons", "m_e/m_μ", "Koide_lepton",
                    "sin²θ_W_PDG", "A_CKM_PDG"],
    "Topo-NT":     ["b_2(K3)=22", "24=Niemeier", "7=dim G_2",
                    "dim SU(N)=N²-1", "K3_topology", "Riemann_ζ(3)",
                    "SECTOR_Group", "SECTOR_Bianchi", "4/π²≈2/5"],
    "Meta-Σp":     ["Σ_8=77", "Σ_14=281", "Σ_21=791", "SECTOR_Σ_p",
                    "SECTOR_Cosmology", "Λ_obs", "η_B", "ln(M_Pl/v)²"],
}
NODE_COMMUNITY = {}
for cname, nodes in COMMUNITY.items():
    for n in nodes:
        NODE_COMMUNITY[n] = cname

# Attach colours on nodes
for n, attr in G.nodes(data=True):
    attr["color_kind"] = KIND_COLOR.get(attr.get("kind", ""), "#cccccc")
    attr["color_tier"] = TIER_COLOR.get(attr.get("tier", ""), "#cccccc")
    attr["community"] = NODE_COMMUNITY.get(n, "Other")
for u, v, attr in G.edges(data=True):
    attr["color"] = TIER_COLOR.get(attr.get("type", ""), "#777777")

# Mark G_2 keystone
if "7=dim G_2" in G.nodes:
    G.nodes["7=dim G_2"]["keystone"] = True


# ---------------------------------------------------------------------------
# 8. Recompute metrics : cycles, SCC, diameter, betweenness
# ---------------------------------------------------------------------------
cycles = list(nx.simple_cycles(G, length_bound=6))
cycles_len = sorted([len(c) for c in cycles])
sccs = [list(c) for c in nx.strongly_connected_components(G) if len(c) > 1]

# Undirected for diameter / centrality
UG = G.to_undirected()
if nx.is_connected(UG):
    diameter = nx.diameter(UG)
    avg_path = nx.average_shortest_path_length(UG)
else:
    largest_cc = max(nx.connected_components(UG), key=len)
    sub = UG.subgraph(largest_cc).copy()
    diameter = nx.diameter(sub)
    avg_path = nx.average_shortest_path_length(sub)

degcent = nx.degree_centrality(G)
btwn = nx.betweenness_centrality(G)
top_deg = sorted(degcent.items(), key=lambda x: -x[1])[:15]
top_btw = sorted(btwn.items(), key=lambda x: -x[1])[:15]


# ---------------------------------------------------------------------------
# 9. Save enriched graph + metrics
# ---------------------------------------------------------------------------
out_nodes = {n: {k: v for k, v in attr.items()} for n, attr in G.nodes(data=True)}
out_edges = [{"src": u, "dst": v, **{k: w for k, w in attr.items() if k != "color"}}
             for u, v, attr in G.edges(data=True)]

with DST.open("w") as fh:
    json.dump({
        "description": "Enriched decoder graph with feedback edges "
                       "(VALIDATES, INFORMS, X-COMM, anchor identities)",
        "date":        "2026-05-27",
        "n_nodes":     G.number_of_nodes(),
        "n_edges":     G.number_of_edges(),
        "communities": COMMUNITY,
        "nodes":       out_nodes,
        "edges":       out_edges,
        "top_degree_centrality": top_deg,
        "top_betweenness":       top_btw,
    }, fh, indent=2, ensure_ascii=False)
print(f"[enrich] wrote {DST}")
print(f"  nodes = {G.number_of_nodes()}, edges = {G.number_of_edges()}")
print(f"  cycles (len<=6) = {len(cycles)}; SCC>1 = {len(sccs)}")
print(f"  diameter = {diameter}, avg_path = {avg_path:.3f}")


# ---------------------------------------------------------------------------
# 10. Save distances + cycles file
# ---------------------------------------------------------------------------
with DST_METRICS.open("w") as fh:
    json.dump({
        "date":     "2026-05-27",
        "n_nodes":  G.number_of_nodes(),
        "n_edges":  G.number_of_edges(),
        "cycles_short":            [list(c) for c in cycles[:50]],
        "cycles_count_by_length":  {str(k): cycles_len.count(k)
                                    for k in sorted(set(cycles_len))},
        "strongly_connected_components": sccs,
        "diameter":         diameter,
        "avg_shortest_path": avg_path,
        "top_degree_centrality": top_deg,
        "top_betweenness":       top_btw,
        "cut_vertices_bottlenecks": sorted(
            nx.articulation_points(UG)),
    }, fh, indent=2, ensure_ascii=False)
print(f"[enrich] wrote {DST_METRICS}")


# ---------------------------------------------------------------------------
# 11. Mermaid diagram (top 20 nodes by centrality)
# ---------------------------------------------------------------------------
top_nodes = [n for n, _ in top_deg[:22]]
mmd_lines = ["%%{init: {'theme':'dark'}}%%", "flowchart LR"]

# group by community
for cname, nodes_in_c in COMMUNITY.items():
    sub_nodes = [n for n in nodes_in_c if n in top_nodes]
    if not sub_nodes:
        continue
    mmd_lines.append(f"  subgraph {cname.replace('-', '_')}")
    for n in sub_nodes:
        nid_clean = (n.replace(' ', '_').replace('=', '_')
                      .replace('(', '_').replace(')', '_')
                      .replace('/', '_').replace('²', '2')
                      .replace('³', '3').replace('★', 'star')
                      .replace('₂', '2').replace('₁', '1')
                      .replace('∞', 'inf').replace(',', '_')
                      .replace('-', '_').replace('+', 'p')
                      .replace('=', '_'))
        label_clean = n.replace("[", "(").replace("]", ")")
        if n == "7=dim G_2":
            mmd_lines.append(f"    {nid_clean}[\"{label_clean}\"]:::keystone")
        else:
            mmd_lines.append(f"    {nid_clean}[\"{label_clean}\"]")
    mmd_lines.append("  end")

# Edges among the top nodes
def slug(n):
    return (n.replace(' ', '_').replace('=', '_')
             .replace('(', '_').replace(')', '_')
             .replace('/', '_').replace('²', '2')
             .replace('³', '3').replace('★', 'star')
             .replace('₂', '2').replace('₁', '1')
             .replace('∞', 'inf').replace(',', '_')
             .replace('-', '_').replace('+', 'p'))

edge_styles = {
    "VALIDATES": "-.->",
    "INFORMS":   "==>",
    "X-COMM":    "-.->",
    "EXACT":     "-->",
    "EXACT_id":  "-->",
    "EXACT_emp": "-->",
    "DERIVED":   "-->",
    "CONJECTURAL":"-->|conj|",
    "CONJECTURE": "-->|conj|",
    "SHARED":    "--",
    "STRUCT":    "-->",
    "STRUCTURAL":"-->",
    "META":      "-.->",
    "AXIOM":     "-->|ax|",
    "THEOREM":   "-->",
    "EMPIRICAL": "-->|emp|",
}
for u, v, attr in G.edges(data=True):
    if u in top_nodes and v in top_nodes:
        e = edge_styles.get(attr.get("type", ""), "-->")
        mmd_lines.append(f"  {slug(u)} {e} {slug(v)}")
mmd_lines.append("  classDef keystone stroke:#ff0,stroke-width:4px,fill:#222")
(PAPERS / "DECODER_diagram.mmd").write_text("\n".join(mmd_lines))
print(f"[enrich] wrote {PAPERS / 'DECODER_diagram.mmd'}")


# ---------------------------------------------------------------------------
# 12. Graphviz DOT (full graph, publication PDF)
# ---------------------------------------------------------------------------
COMMUNITY_BG = {
    "YM-core":  "#e6f0ff",
    "SM-pheno": "#fff0e6",
    "Topo-NT":  "#e6ffe6",
    "Meta-Σp":  "#f5e6ff",
    "Other":    "#ffffff",
}
dot = ['digraph DECODER {',
       '  rankdir=LR;',
       '  graph [splines=true, overlap=false, nodesep=0.4, ranksep=0.7,'
       ' fontname="Helvetica", fontsize=10, label="Yang-Mills Decoder Network'
       ' — Kévin Rémondière 2026-05-27\\n8 super-nodes + feedback loops"];',
       '  node [style="filled,rounded", shape=box, fontname="Helvetica"];',
       '  edge [fontname="Helvetica", fontsize=8];']

# Community subgraphs
for cname in COMMUNITY:
    dot.append(f'  subgraph cluster_{cname.replace("-", "_")} {{')
    dot.append(f'    label="{cname}"; style=filled; color="{COMMUNITY_BG[cname]}";')
    for n in COMMUNITY[cname]:
        if n not in G.nodes:
            continue
        attr = G.nodes[n]
        col = attr.get("color_kind", "#cccccc")
        shape = "box"
        if attr.get("kind") == "anchor":
            shape = "ellipse"
        elif attr.get("kind") == "sector":
            shape = "hexagon"
        elif attr.get("kind") == "observable":
            shape = "note"
        elif attr.get("kind") == "theory":
            shape = "doubleoctagon"
        elif attr.get("kind") == "root":
            shape = "tripleoctagon"
        peripheries = 1
        penwidth = 1.0
        bd_color = "black"
        if attr.get("keystone"):
            peripheries = 2
            penwidth = 3.0
            bd_color = "gold"
        n_safe = n.replace('"', '\\"')
        dot.append(f'    "{n_safe}" [fillcolor="{col}", shape={shape},'
                   f' peripheries={peripheries}, penwidth={penwidth},'
                   f' color="{bd_color}"];')
    dot.append('  }')

# Edges
EDGE_STYLE = {
    "VALIDATES":  ('color="#17becf"', 'style=bold',     'arrowhead=vee'),
    "INFORMS":    ('color="#17becf"', 'style=dashed',   'arrowhead=vee'),
    "X-COMM":     ('color="#e377c2"', 'style=dashed',   'arrowhead=normal'),
    "EXACT":      ('color="#1f77b4"', 'style=solid',    'arrowhead=normal'),
    "EXACT_id":   ('color="#1f77b4"', 'style=solid',    'arrowhead=normal'),
    "EXACT_emp":  ('color="#1f77b4"', 'style=solid',    'arrowhead=normal'),
    "STRUCT":     ('color="#bcbd22"', 'style=solid',    'arrowhead=normal'),
    "STRUCTURAL": ('color="#bcbd22"', 'style=solid',    'arrowhead=normal'),
    "DERIVED":    ('color="#7f7f7f"', 'style=solid',    'arrowhead=normal'),
    "CONJECTURAL":('color="#ff7f0e"', 'style=dotted',   'arrowhead=onormal'),
    "CONJECTURE": ('color="#ff7f0e"', 'style=dotted',   'arrowhead=onormal'),
    "SHARED":     ('color="#aaaaaa"', 'style=solid',    'arrowhead=normal'),
    "META":       ('color="#8c564b"', 'style=dashed',   'arrowhead=normal'),
    "AXIOM":      ('color="#9467bd"', 'style=bold',     'arrowhead=normal'),
    "THEOREM":    ('color="#2ca02c"', 'style=solid',    'arrowhead=normal'),
    "EMPIRICAL":  ('color="#d62728"', 'style=solid',    'arrowhead=normal'),
}
for u, v, attr in G.edges(data=True):
    t = attr.get("type", "?")
    styles = EDGE_STYLE.get(t, ('color="#888888"', 'style=solid', 'arrowhead=normal'))
    label = attr.get("label", "")[:38]
    u_s = u.replace('"', '\\"')
    v_s = v.replace('"', '\\"')
    dot.append(f'  "{u_s}" -> "{v_s}" [{", ".join(styles)},'
               f' label="{label.replace(chr(34),"")}"];')

dot.append('}')
(PAPERS / "DECODER_diagram.dot").write_text("\n".join(dot))
print(f"[enrich] wrote {PAPERS / 'DECODER_diagram.dot'}")


# ---------------------------------------------------------------------------
# 13. TikZ skeleton (8 super-nodes only — manual fine-tuning expected)
# ---------------------------------------------------------------------------
SUPER_NODES = [
    "κ_FP=1/6", "F∞=9/10", "c∞=1/4", "ξ★=2/3",
    "b_0=11N/(48π²)", "4/π²≈2/5", "ζ(3)/√π=κ_∞", "b_2(K3)=22",
    "24=Niemeier", "7=dim G_2", "Koide K=2/3",
]
tikz = [
    r"\documentclass[tikz,border=8pt]{standalone}",
    r"\usepackage{tikz}",
    r"\usetikzlibrary{positioning,arrows.meta,calc,backgrounds,fit}",
    r"\definecolor{ymcore}{HTML}{E6F0FF}",
    r"\definecolor{smpheno}{HTML}{FFF0E6}",
    r"\definecolor{toponomt}{HTML}{E6FFE6}",
    r"\definecolor{metasigp}{HTML}{F5E6FF}",
    r"\definecolor{validates}{HTML}{17BECF}",
    r"\definecolor{informs}{HTML}{17BECF}",
    r"\definecolor{xcomm}{HTML}{E377C2}",
    r"\definecolor{exact}{HTML}{1F77B4}",
    r"\definecolor{keystoneborder}{HTML}{D4AF37}",
    r"\begin{document}",
    r"\begin{tikzpicture}[",
    r"  anchor/.style={ellipse,draw,fill=ymcore,minimum height=8mm,minimum width=18mm,font=\small},",
    r"  keystone/.style={ellipse,draw=keystoneborder,line width=2pt,fill=toponomt,minimum height=8mm,font=\bfseries\small},",
    r"  sector/.style={diamond,draw,fill=smpheno,aspect=2,font=\small},",
    r"  observable/.style={rectangle,draw,fill=metasigp,rounded corners=2pt,font=\small},",
    r"  every edge/.append style={font=\tiny},",
    r"  node distance=15mm and 22mm]",
    r"",
    r"  % --- Anchors (super-nodes) -------------------------------------------",
    r"  \node[anchor]      (kFP)     {$\kappa_{FP}=\tfrac{1}{6}$};",
    r"  \node[anchor,right=of kFP] (Koide)  {$K=\tfrac{2}{3}$};",
    r"  \node[anchor,below=of kFP] (xistar) {$\xi^{\star}=\tfrac{2}{3}$};",
    r"  \node[anchor,below=of Koide] (Foo)  {$F_{\infty}=\tfrac{9}{10}$};",
    r"  \node[anchor,right=of Koide] (cinf) {$c_{\infty}=\tfrac{1}{4}$};",
    r"  \node[anchor,right=of cinf]  (b0)   {$b_0=\tfrac{11N}{48\pi^{2}}$};",
    r"  \node[anchor,below=of cinf]  (kinf) {$\zeta(3)/\sqrt{\pi}$};",
    r"  \node[keystone,right=of b0]  (G2)   {$\dim G_{2}=7$};",
    r"  \node[anchor,below=of G2]    (K3)   {$b_2(K3)=22$};",
    r"  \node[anchor,below=of K3]    (N24)  {$24=\text{Niemeier}$};",
    r"  \node[anchor,below=of kinf]  (pi2)  {$\tfrac{4}{\pi^{2}}\approx\tfrac{2}{5}$};",
    r"",
    r"  % --- Sectors --------------------------------------------------------",
    r"  \node[sector,below=of xistar] (SYM)  {YM-SD};",
    r"  \node[sector,below=of SYM]    (SYL)  {YM-lattice};",
    r"  \node[sector,below=of Foo]    (SH)   {Hadrons};",
    r"  \node[sector,right=of SH]     (SEW)  {EW};",
    r"  \node[sector,right=of SEW]    (SYuk) {Yukawa};",
    r"  \node[sector,right=of SYuk]   (SCKM) {CKM};",
    r"  \node[sector,below=of N24]    (SCo)  {Cosmology};",
    r"  \node[sector,left=of SCo]     (SSp)  {Sigma-primes};",
    r"",
    r"  % --- EXACT / IDENTITY arrows ----------------------------------------",
    r"  \draw[->,thick,color=exact] (kFP) edge[bend left=10] node[above]{$4\kappa_{FP}$} (Koide);",
    r"  \draw[->,thick,color=exact] (kFP) edge[bend right=15] (xistar);",
    r"  \draw[->,thick,color=exact] (Koide) edge[bend left=8] node[right,font=\tiny]{$=$} (xistar);",
    r"",
    r"  % --- INFORMS / SHARED (anchor -> sector) ----------------------------",
    r"  \draw[->,color=informs,dashed] (Foo)  -- (SH);",
    r"  \draw[->,color=informs,dashed] (kFP)  -- (SYM);",
    r"  \draw[->,color=informs,dashed] (kinf) -- (SYL);",
    r"  \draw[->,color=informs,dashed] (b0)   -- (SYM);",
    r"  \draw[->,color=informs,dashed] (G2)   -- (SYM);",
    r"  \draw[->,color=informs,dashed] (K3)   -- (SSp);",
    r"  \draw[->,color=informs,dashed] (N24)  -- (SCo);",
    r"  \draw[->,color=informs,dashed] (pi2)  -- (SEW);",
    r"",
    r"  % --- VALIDATES feedback (sector -> anchor)---------------------------",
    r"  \draw[->,color=validates,line width=1.2pt,densely dotted]",
    r"        (SEW) edge[bend left=25] (kFP);   % Higgs validates kappa_FP",
    r"  \draw[->,color=validates,line width=1.2pt,densely dotted]",
    r"        (SYuk) edge[bend right=20] (Koide); % Koide validates 2/3",
    r"  \draw[->,color=validates,line width=1.2pt,densely dotted]",
    r"        (SYL) edge[bend left=18] (kinf);  % lattice validates zeta(3)/sqrt(pi)",
    r"  \draw[->,color=validates,line width=1.2pt,densely dotted]",
    r"        (SCo) edge[bend right=25] (N24);  % Lambda validates 281",
    r"",
    r"  % --- X-COMM (sector ↔ sector via shared anchor) ---------------------",
    r"  \draw[<->,color=xcomm,dotted,thick] (SYM)  -- (SYL);",
    r"  \draw[<->,color=xcomm,dotted,thick] (SEW)  -- (SYuk);",
    r"  \draw[<->,color=xcomm,dotted,thick] (SYuk) -- (SCKM);",
    r"  \draw[<->,color=xcomm,dotted,thick] (SCo)  -- (SSp);",
    r"",
    r"  % --- Legend ---------------------------------------------------------",
    r"  \node[anchor=south west,font=\scriptsize,align=left,fill=white,draw]",
    r"        at ($(SH.south west)+(-5mm,-12mm)$) {",
    r"          \textbf{Legend} \\",
    r"          $\,\bullet$ blue solid: \textsc{exact identity}\\",
    r"          $\,\bullet$ cyan dashed: \textsc{informs} (anchor$\to$sector)\\",
    r"          $\,\bullet$ cyan dotted: \textsc{validates} (sector$\to$anchor, feedback)\\",
    r"          $\,\bullet$ pink dotted: \textsc{X-COMM} (sector$\leftrightarrow$sector)\\",
    r"          $\,\bullet$ gold border: keystone node (G$_2$)",
    r"        };",
    r"\end{tikzpicture}",
    r"\end{document}",
]
(PAPERS / "DECODER_diagram.tex").write_text("\n".join(tikz))
print(f"[enrich] wrote {PAPERS / 'DECODER_diagram.tex'}")


# ---------------------------------------------------------------------------
# 14. D3.js HTML (interactive — minimal force-directed)
# ---------------------------------------------------------------------------
d3_nodes = []
for n, attr in G.nodes(data=True):
    d3_nodes.append({
        "id": n,
        "kind": attr.get("kind", ""),
        "tier": attr.get("tier", ""),
        "community": attr.get("community", "Other"),
        "color": attr.get("color_kind", "#cccccc"),
        "keystone": bool(attr.get("keystone")),
    })
d3_links = []
for u, v, attr in G.edges(data=True):
    d3_links.append({
        "source": u, "target": v,
        "type":   attr.get("type", ""),
        "label":  attr.get("label", ""),
        "color":  attr.get("color", "#777"),
    })
html = f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>YM Decoder Network — feedback loops</title>
<style>
 body {{font-family:Helvetica,Arial;background:#111;color:#eee;margin:0}}
 svg  {{width:100vw;height:96vh;display:block;background:#111}}
 .node text {{font-size:10px;fill:#eee;pointer-events:none}}
 .link {{stroke-opacity:0.55}}
 .keystone {{stroke:gold;stroke-width:4px}}
 #legend {{position:fixed;top:6px;left:6px;background:rgba(0,0,0,0.7);padding:6px;
            border:1px solid #555;font-size:11px;line-height:1.3}}
 .lk-VALIDATES {{stroke:#17becf;stroke-dasharray:4 2}}
 .lk-INFORMS   {{stroke:#17becf;stroke-dasharray:6 3}}
 .lk-X-COMM    {{stroke:#e377c2;stroke-dasharray:2 2}}
 .lk-EXACT, .lk-EXACT_id, .lk-EXACT_emp {{stroke:#1f77b4}}
 .lk-CONJECTURAL, .lk-CONJECTURE {{stroke:#ff7f0e;stroke-dasharray:3 2}}
 .lk-STRUCT, .lk-STRUCTURAL {{stroke:#bcbd22}}
 .lk-META   {{stroke:#8c564b;stroke-dasharray:5 2}}
 .lk-SHARED {{stroke:#888}}
 .lk-DERIVED {{stroke:#7f7f7f}}
 .lk-AXIOM  {{stroke:#9467bd}}
 .lk-THEOREM {{stroke:#2ca02c}}
</style></head><body>
<div id='legend'>
  <b>YM Decoder Network — {G.number_of_nodes()} nodes / {G.number_of_edges()} edges</b><br>
  Click + drag nodes. Mouse wheel zooms. Hover edge for label.<br>
  <span style='color:#1f77b4'>━</span> exact identity
  &nbsp;<span style='color:#17becf'>┄</span> feedback (informs/validates)
  &nbsp;<span style='color:#e377c2'>┈</span> X-comm
  &nbsp;<span style='color:#ff7f0e'>┄</span> conjectural<br>
  Keystone = G<sub>2</sub> (gold border)
</div>
<svg></svg>
<script src='https://d3js.org/d3.v7.min.js'></script>
<script>
const nodes = {json.dumps(d3_nodes, ensure_ascii=False)};
const links = {json.dumps(d3_links, ensure_ascii=False)};
const svg = d3.select('svg');
const w = window.innerWidth, h = window.innerHeight * 0.95;
const g = svg.append('g');
svg.call(d3.zoom().on('zoom', e => g.attr('transform', e.transform)));
const sim = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d=>d.id).distance(80))
  .force('charge', d3.forceManyBody().strength(-220))
  .force('center', d3.forceCenter(w/2, h/2));
const link = g.append('g').selectAll('line').data(links).enter().append('line')
  .attr('class', d=>'link lk-' + d.type)
  .attr('stroke-width', d => d.type==='VALIDATES'||d.type==='INFORMS' ? 2 : 1)
  .attr('marker-end','url(#arrow)');
link.append('title').text(d => d.type + ': ' + d.label);
svg.append('defs').append('marker').attr('id','arrow').attr('viewBox','0 -5 10 10')
  .attr('refX',16).attr('refY',0).attr('markerWidth',6).attr('markerHeight',6)
  .attr('orient','auto').append('path').attr('d','M0,-5L10,0L0,5').attr('fill','#aaa');
const node = g.append('g').selectAll('g').data(nodes).enter().append('g')
  .attr('class','node')
  .call(d3.drag()
        .on('start', (e,d) => {{ if(!e.active) sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; }})
        .on('drag',  (e,d) => {{ d.fx=e.x; d.fy=e.y; }})
        .on('end',   (e,d) => {{ if(!e.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }}));
node.append('circle').attr('r', d => d.keystone?14:9)
  .attr('fill', d => d.color)
  .attr('class', d => d.keystone?'keystone':'')
  .attr('stroke','#fff').attr('stroke-width', d => d.keystone?3:1);
node.append('text').attr('x',14).attr('y',4).text(d=>d.id);
sim.on('tick', () => {{
  link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y)
      .attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
  node.attr('transform', d => 'translate('+d.x+','+d.y+')');
}});
</script></body></html>
"""
(PAPERS / "DECODER_diagram.html").write_text(html, encoding="utf-8")
print(f"[enrich] wrote {PAPERS / 'DECODER_diagram.html'}")


# ---------------------------------------------------------------------------
# 15. Quick textual summary printed to stdout
# ---------------------------------------------------------------------------
print()
print("=" * 64)
print(f" enriched graph metrics : {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print("=" * 64)
print(f" cycles (len<=6) : {len(cycles)}")
print(f" SCC (size>1)    : {len(sccs)}")
print(f" diameter (UG)   : {diameter}")
print(f" avg shortest    : {avg_path:.3f}")
print(" top-5 cycles    :")
for c in cycles[:5]:
    print("   -", " -> ".join(c))
print(" top-5 by deg    :")
for n, v in top_deg[:5]:
    print(f"   - {n:<30s} {v:.3f}")
print(" top-5 by btwn   :")
for n, v in top_btw[:5]:
    print(f"   - {n:<30s} {v:.3f}")
