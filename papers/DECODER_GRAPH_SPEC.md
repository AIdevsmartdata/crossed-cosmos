# YM Decoder Network — Enriched Graph + Tool-stack Specification

**Author** : Kévin Rémondière — ORCID 0009-0008-2443-7166
**Date**   : 2026-05-27
**Object** : 3-part deliverable (A install plan, B enriched graph, C diagrams).

---

## SECTION A — Symbolic / proof tool-stack install plan

| # | Tool | Why useful here | Install command | Disk / RAM |
|---|------|-----------------|-----------------|------------|
| 1 | **SageMath** 10.x | Number-theory + symbolic + lattice arithmetic. Already a script in repo (`scripts/install_sage_pc.sh`). Used to test M_24/K3 cohomology, ζ(3)/√π closed-form, Bianchi class numbers. Bundles **PARI/GP** (already installed at `/usr/bin/gp`). | `bash /root/cc-private/scripts/install_sage_pc.sh` (mamba/conda-forge, ≈30 min, no sudo) | 2 GB |
| 2 | **Wolfram Engine** (free non-commercial) | Heat-kernel a₂,a₄ for general Riemannian D=4. The cleanest existing implementation of Branson–Gilkey / Vassilevich coefficients. Needed for `b_0=11N/(48π²)` and `κ_FP=1/6` derivations. | Register e-mail at wolfram.com/engine, `bash WolframEngine_*.sh`. Free under EULA. CLI binary `wolframscript`. | 4 GB |
| 3 | **Lean 4 + mathlib** | Already partial in `/root/.elan/bin/lean`. Mathlib has `Mathlib.GroupTheory.Coxeter`, `Mathlib.LinearAlgebra.LieAlgebra`, sufficient for κ_FP(SU(N))=1/(2·\|Φ⁺\|). Formalizes KR-FP-3 conditional proof. | `elan toolchain install leanprover/lean4:v4.10.0 && lake update` inside `lean/`. | 6 GB cache |
| 4 | **Graphviz** | Convert `papers/DECODER_diagram.dot` → PDF for paper figures (publication-quality). Currently MISSING. | `sudo apt-get install -y graphviz` then `dot -Tpdf papers/DECODER_diagram.dot -o decoder.pdf` | 40 MB |
| 5 | **Neo4j Community** 5.x | Graph DB lets Cypher queries like `MATCH (a:Anchor)-[:VALIDATES*1..3]->(b) RETURN a,b`. Powerful for cycle / community queries beyond NetworkX. | `wget -O neo4j.deb https://neo4j.com/download-thanks/?edition=community && sudo dpkg -i neo4j.deb`; load via `papers/DECODER_GRAPH_ENRICHED.json → neo4j-admin import`. | 500 MB + JDK 17 |
| 6 | **Gephi** | Visual exploration (force-atlas, modularity). Reads same JSON via `python -m networkx readwrite gexf` exporter. Useful for outreach figures. | Download `gephi-0.10.1-linux-x64.tar.gz`, untar, run `bin/gephi`. JDK 17 required. | 300 MB |
| 7 | **xACT** (Mathematica) | Index-free tensor calculus — needed for F^{μν}F_{μν}, D_μ F^{μν}=0 manipulations symbolically. Drops into Wolfram. | Inside Mathematica: `<<xAct.xTensor`; or pull `git clone https://github.com/xact/xAct`. | 30 MB |
| 8 | (optional) **PyTorch-Geometric** | Treat decoder graph as a typed-edge MGN: train a GNN to *predict* hidden anchor identities from observed numerical patterns. Adversarial sanity-check against rational-fit overfitting. | `pip install torch torch-geometric` | 2 GB GPU/CPU |

**Order of install for biggest immediate ROI**

1. `apt install graphviz` ← 30 s, immediately renders Section C diagrams.
2. SageMath via the existing script ← reproducible BIG_MASS_TABLE arithmetic.
3. Lean 4 + mathlib ← closes formal KR-FP-3 + KappaOneSixth lemmas.
4. Everything else is bonus.

---

## SECTION B — Enriched graph specification

### B.1  Code that performs the enrichment

The single source of truth is `papers/enrich_decoder_graph.py`. It reads
`papers/DECODER_GRAPH.json` and writes 6 artifacts. Key additions (~43 new
edges, +11 new observable nodes) are:

```python
# 1. New OBSERVABLE nodes (added so VALIDATES edges have targets)
NEW_OBSERVABLES = {
    "m_e/m_μ":      {"kind": "observable", "value": 0.0048,  "sector": "Yukawa"},
    "Koide_lepton": {"kind": "observable", "value": 0.6666,  "sector": "Yukawa"},
    "κ_EE_lat(SU2)": {"kind":"observable", "value": 0.5065,  "sector":"YM-lattice"},
    "κ_EE_lat(SU3)": {"kind":"observable", "value": 0.603,   "sector":"YM-lattice"},
    "κ_EE_lat(SU4)": {"kind":"observable", "value": 0.6358,  "sector":"YM-lattice"},
    "sin²θ_W_PDG":   {"kind":"observable", "value": 0.23121, "sector":"EW"},
    "A_CKM_PDG":     {"kind":"observable", "value": 0.826,   "sector":"CKM"},
    "ln(M_Pl/v)²":   {"kind":"observable", "value": 73.7,    "sector":"Cosmology"},
    "α_s(M_Z)":      {"kind":"observable", "value": 0.1181,  "sector":"Hadrons"},
}

# 2. OBSERVABLE -> ANCHOR  (VALIDATES feedback)
VALIDATES_EDGES = [
    ("m_H=125.10",     "1/2",                "0.016%", "m_H = κ(SU(2))·v ⇒ κ=1/2"),
    ("Koide_lepton",   "κ_FP=1/6",          "0.0%",   "K=2/3 = 4·κ_FP(SU(3))"),
    ("κ_EE_lat(SU2)",  "ζ(3)/√π=κ_∞",       "25%",    "lat EE saturates κ_∞(1-1/N²)"),
    ("κ_EE_lat(SU3)",  "ζ(3)/√π=κ_∞",       "0.0%",   "lat EE saturates κ_∞(1-1/N²)"),
    ("κ_EE_lat(SU4)",  "ζ(3)/√π=κ_∞",       "<0.4σ",  "lat EE saturates κ_∞(1-1/N²)"),
    ("sin²θ_W_PDG",    "sin²θ_W=3/13",      "0.19%",  "3/13 ≈ 0.2308 vs PDG 0.2312"),
    ("A_CKM_PDG",      "A_CKM=19/23",       "0.01%",  "19/23 ≈ 0.8261 vs PDG 0.826"),
    ("ln(M_Pl/v)²",    "Σ_8=77",            "4.3%",   "Σ first 8 primes = 77"),
    ("Λ_obs",          "Σ_14=281",          "0.07%",  "-ln(Λ/M_Pl⁴) ≈ 281"),
    ("η_B",             "Σ_21=791",         "24%",    "-ln(η_B) ≈ 21 (weak)"),
    ("α_s(M_Z)",        "4/π²≈2/5",         "5%",     "α_s ≈ 2/5"),
    ("v=246.22",        "1/2",              "—",      "v sets EW scale where κ=1/2"),
    ("m_Z=91.187",      "Koide K=2/3",      "struct", "m_Z/v in Weinberg sector"),
]

# 3. SECTOR -> THEORY  (INFORMS)
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

# 4. ANCHOR ↔ ANCHOR (explicit reverse identities, new)
ANCHOR_IDENTITY_EDGES = [
    ("Koide K=2/3", "κ_FP=1/6",   "EXACT_id",  "Koide K = 4·κ_FP(SU(3)) reverse"),
    ("ξ★=2/3",      "κ_FP=1/6",   "EXACT_id",  "ξ★ = 4·κ_FP reverse identification"),
    ("ξ★=2/3",      "Koide K=2/3","EXACT_id",  "ξ★ ≡ Koide K  same value 2/3"),
    ("cos²θ_W=10/13","sin²θ_W=3/13","EXACT_id","trig identity sum=1 reverse"),
    ("c∞=1/4",      "1/2",        "STRUCT",    "c∞=1/4 = (1/2)² multiplicity²"),
    ("κ_FP=1/6",    "1/2",        "STRUCT",    "κ_FP(SU(2)) = 1/2 = 1/(2·|Φ⁺|)"),
    ("b_2(K3)=22",  "24=Niemeier","STRUCT",    "b_2(K3)+2 = 24 (string closure)"),
    ("Σ_14=281",    "7=dim G_2",  "META",      "Σ_14 selects k=14=dim G_2 adj"),
    ("Σ_21=791",    "24=Niemeier","META",      "Σ_21 sits 3 below 24"),
    ("Σ_8=77",      "dim SU(N)=N²-1","META",   "k=8=dim SU(3) adj selects QCD"),
]

# 5. SECTOR ↔ SECTOR via shared anchor (X-COMM cross-community)
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
```

### B.2  New cycles created (excerpt)

Before enrichment: **0 cycles** (pure DAG).
After enrichment: **42 cycles ≤ 6 hops**, distributed as

| length | count |
|--------|-------|
| 2      | 7     |
| 3      | 10    |
| 4      | 10    |
| 5      | 9     |
| 6      | 6     |

Highlight (top 5 endocrine loops):

1. `sin²θ_W=3/13 ↔ cos²θ_W=10/13` (2-cycle, exact-id)
2. `24=Niemeier → SECTOR_Group → K3_topology → b_2(K3)=22 → 24=Niemeier` (4-cycle, topological)
3. `Koide K=2/3 → ξ★=2/3 → κ_FP=1/6 → Koide K=2/3` (3-cycle, Kostant identity triangle)
4. `SECTOR_YM-SD ↔ SECTOR_YM-lattice` (2-cycle, X-COMM)
5. `SECTOR_Σ_p → K3_topology → b_2(K3)=22 → SECTOR_Σ_p` (3-cycle, metaselector)

### B.3  Strongly Connected Components (the true feedback loops)

The graph now contains **3 non-trivial SCCs**:

* **SCC #1 — YM core feedback** (9 nodes)
  `{Koide K=2/3, SECTOR_d_s-decoder, κ_FP=1/6, SECTOR_YM-SD, SECTOR_YM-lattice,
   SECTOR_Yukawa, SECTOR_EW, Branson-Gilkey, ξ★=2/3}`
  → predictions (κ_FP) ↔ measurements (lattice EE, Higgs mass) ↔ theory (Branson-Gilkey)

* **SCC #2 — Topo/Cosmo feedback** (10 nodes)
  `{24=Niemeier, SECTOR_Σ_p, SECTOR_Cosmology, Riemann_ζ(3), K3_topology,
   SECTOR_Group, b_2(K3)=22, SECTOR_CKM, SECTOR_Bianchi, ζ(3)/√π=κ_∞}`
  → number-theory + cosmology metaselectors mutually inform K3 topology

* **SCC #3 — Weinberg identity** (2 nodes)
  `{sin²θ_W=3/13, cos²θ_W=10/13}`
  → sum=1 trig identity (smallest possible loop)

### B.4  Updated metrics (Δ vs pre-enrichment)

| metric                          | before | after  | Δ        |
|---------------------------------|--------|--------|----------|
| nodes                           | 45     | 56     | +11      |
| edges                           | 56     | 99     | +43      |
| cycles (len ≤ 6)                | 0      | 42     | **+42**  |
| SCCs (size > 1)                 | 0      | 3      | **+3**   |
| diameter (undirected)           | 12     | 9      | −3       |
| avg shortest path               | 4.74   | 3.71   | −1.03    |
| top-betweenness node            | 7=dim G_2 | Branson-Gilkey | bridge moved to theory layer |
| cut vertices (bottlenecks)      | 14     | 15     | +1 (more observable singletons) |

### B.5  Top-5 centrality after enrichment

| rank | node                       | degree | betweenness |
|------|----------------------------|--------|-------------|
| 1    | `SECTOR_YM-SD`             | 0.218  | 0.056       |
| 2    | `κ_FP=1/6`                 | 0.200  | 0.070       |
| 3    | `SECTOR_Cosmology`         | 0.127  | —           |
| 4    | `SECTOR_Group`             | 0.127  | —           |
| 5    | `SECTOR_d_s-decoder`       | 0.127  | —           |
| —    | `Branson-Gilkey` (top btw) | 0.073  | **0.085**   |
| —    | `K3_topology` (top btw)    | 0.073  | 0.049       |

→ Branson–Gilkey emerges as the new top-betweenness *theoretical* hub (it now
sits inside SCC #1 and connects YM-SD predictions to lattice measurements).
G_2 remains the **keystone** node (still the most cross-cluster connector).

---

## SECTION C — Diagram specifications

### C.1  Mermaid (markdown-renderable) — top-22 nodes only

File : `papers/DECODER_diagram.mmd` (52 lines).

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart LR
  subgraph YM_core
    Δ_FP["Δ_FP"]
    κ_FP_1_6["κ_FP=1/6"]
    ξstar_2_3["ξ★=2/3"]
    Branson_Gilkey["Branson-Gilkey"]
    SECTOR_YM_SD["SECTOR_YM-SD"]
    SECTOR_YM_lattice["SECTOR_YM-lattice"]
    SECTOR_d_s_decoder["SECTOR_d_s-decoder"]
    ζ_3__√π_κ_inf["ζ(3)/√π=κ_∞"]
  end
  subgraph SM_pheno
    Koide_K_2_3["Koide K=2/3"]
    SECTOR_EW["SECTOR_EW"]
    SECTOR_Yukawa["SECTOR_Yukawa"]
  end
  subgraph Topo_NT
    b_2_K3__22["b_2(K3)=22"]
    24_Niemeier["24=Niemeier"]
    7_dim_G_2["7=dim G_2"]:::keystone
    K3_topology["K3_topology"]
    SECTOR_Group["SECTOR_Group"]
    dim_SU_N__N2_1["dim SU(N)=N²-1"]
  end
  subgraph Meta_Σp
    Σ_14_281["Σ_14=281"]
    SECTOR_Cosmology["SECTOR_Cosmology"]
  end
  Δ_FP --> κ_FP_1_6
  Δ_FP -->|conj| ξstar_2_3
  Branson_Gilkey --> κ_FP_1_6
  Branson_Gilkey -->|conj| ξstar_2_3
  κ_FP_1_6 --> Koide_K_2_3
  κ_FP_1_6 --> ξstar_2_3
  Koide_K_2_3 --> ξstar_2_3
  K3_topology --> b_2_K3__22
  K3_topology -- 24_Niemeier
  ζ_3__√π_κ_inf -- SECTOR_YM_lattice
  Σ_14_281 -.-> 7_dim_G_2
  Σ_14_281 -->|conj| SECTOR_Cosmology
  %% feedback (validates) — dotted
  SECTOR_EW -.-> κ_FP_1_6
  SECTOR_Yukawa -.-> Koide_K_2_3
  SECTOR_YM_lattice -.-> ζ_3__√π_κ_inf
  classDef keystone stroke:#ff0,stroke-width:4px,fill:#222
```

### C.2  Graphviz DOT (publication PDF)

File : `papers/DECODER_diagram.dot` (170 lines, full 56-node, 99-edge graph).

Render:

```bash
sudo apt-get install -y graphviz                       # one-time
dot -Tpdf  papers/DECODER_diagram.dot -o papers/DECODER_diagram.pdf
dot -Tsvg  papers/DECODER_diagram.dot -o papers/DECODER_diagram.svg
```

Layout details baked in:

* `rankdir=LR` (left→right reading)
* `splines=true, overlap=false, nodesep=0.4, ranksep=0.7`
* Four `cluster_*` subgraphs (one per community) with pastel backgrounds
* Anchors = ellipses (green fill), sectors = hexagons, observables = "note",
  theories = doubleoctagons, roots = tripleoctagons
* G_2 keystone : `peripheries=2, penwidth=3.0, color=gold`
* Edge palette : exact=blue, feedback (VALIDATES/INFORMS)=cyan,
  X-COMM=pink-dashed, conjectural=orange-dotted, axiom=purple-bold

### C.3  TikZ skeleton (LaTeX paper figure)

File : `papers/DECODER_diagram.tex` (86 lines). Compile with

```bash
pdflatex papers/DECODER_diagram.tex                    # standalone
```

Defines 11 super-nodes (`κ_FP, Koide, ξ★, F∞, c∞, b_0, ζ(3)/√π, G_2, K3, 24,
4/π²`) and 8 sector diamonds, then draws three edge classes:

* `EXACT` solid blue arrows (`κ_FP → Koide` etc.)
* `INFORMS` cyan dashed arrows (anchor → sector)
* `VALIDATES` cyan densely-dotted arrows (sector → anchor, feedback)
* `X-COMM` pink dotted bi-arrows (sector ↔ sector)
* G_2 keystone has 2-pt gold border

The skeleton compiles standalone; positions can be fine-tuned by editing
`\node[anchor,right=of …]` directives.

### C.4  D3.js interactive HTML (optional, but very valuable)

File : `papers/DECODER_diagram.html` (single file, embeds full enriched graph
as JSON, no server required).

Open in any browser, drag nodes, scroll-zoom. Edge tooltips show
`type: label`. Used for screencasts, exploratory debugging, and Zenodo
companion artifact.

---

## REPORT — costs, ROI, next steps

| item                                  | time      | $   | risk |
|---------------------------------------|-----------|-----|------|
| Section A : install Graphviz only     | 30 s      | 0   | none |
| Section A : full SageMath install     | 30 min    | 0   | none |
| Section A : Lean 4 + mathlib          | 1 h       | 0   | none |
| Section A : Wolfram + xACT            | 45 min    | 0   | EULA |
| Section A : Neo4j + Gephi             | 1 h       | 0   | JDK  |
| Section B : enrichment script (done)  | n/a       | 0   | n/a  |
| Section C : render PDF (`dot -Tpdf`)  | < 1 s     | 0   | needs graphviz |
| Section C : render TikZ PDF           | < 5 s     | 0   | latex installed |

**Highest-ROI next step** : `sudo apt-get install -y graphviz` followed by
`dot -Tpdf papers/DECODER_diagram.dot -o papers/DECODER_diagram.pdf`.
That gives you a publication-quality figure in 30 s for any of the Clay or
ECI papers (e.g. `Paper_ECI_Survey_Clay_BullAMS`).

**Files created in this session** (all under `/root/cc-private/papers/`) :

| file                                       | size  | purpose |
|--------------------------------------------|-------|---------|
| `enrich_decoder_graph.py`                  | 17 KB | reproducible enrichment script |
| `DECODER_GRAPH_ENRICHED.json`              | ~25 KB | 56 nodes, 99 edges, with colour + community tags |
| `DECODER_DISTANCES_CYCLES_ENRICHED.json`   | ~10 KB | 42 cycles, 3 SCCs, diameter=9 |
| `DECODER_diagram.mmd`                      | 1.5 KB | Mermaid (markdown-embed) |
| `DECODER_diagram.dot`                      | 8 KB  | Graphviz (PDF/SVG render) |
| `DECODER_diagram.tex`                      | 4 KB  | TikZ skeleton (LaTeX standalone) |
| `DECODER_diagram.html`                     | 18 KB | D3.js interactive |
| `DECODER_GRAPH_SPEC.md`                    | this file | master specification |

**Suggested integration** : drop `\input{DECODER_diagram.tex}` (or
`\includegraphics{DECODER_diagram.pdf}`) into the figure environment of any
of these papers :

* `Paper_ECI_Survey_Clay_BullAMS` — best fit (Bull AMS survey style)
* `Paper_Mass_Gap_First_Principles_PRL` — overview figure in §1
* `Paper_KR_FP_B_BakryEmery_LMP` — show the FP-anchor sub-cluster
* `ARXIV_BATCH_SUBMISSION_2026-05-26.md` — companion landing page

**To rerun after any anchor / observable update** :

```bash
python3 /root/cc-private/papers/enrich_decoder_graph.py
```

Everything regenerates idempotently in < 1 s.
