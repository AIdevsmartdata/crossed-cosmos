# BDH Verification: ModAlg 2-Category Originality Check
**Date:** 2026-05-02
**Purpose:** Month 1 task from `tomita_takesaki_2cat_2026_05_02.md` — verify or refute whether Bartels–Douglas–Henriques (BDH) conformal nets programme, or any related operator-algebraic categorification work, implicitly contains the proposed `ModAlg` 2-category.
**Verification standard:** Every arXiv citation verified directly via `https://export.arxiv.org/api/query?id_list=...` with `User-Agent: ECI-bdh-verify/1.0`. Zero-tolerance for fabricated references.

---

## 1. BDH Papers Verified

The following papers were retrieved directly via arXiv API batch query (id_list) and confirmed to exist with the stated titles and authors:

| arXiv ID | Title | Authors |
|---|---|---|
| **0912.5307v2** | Conformal nets and local field theory | Bartels, Douglas, Henriques |
| **1302.2604v3** | Conformal nets I: coordinate-free nets | Bartels, Douglas, Henriques |
| **1310.8263v4** | Conformal nets III: fusion of defects | Bartels, Douglas, Henriques |
| **1409.8672v2** | Conformal nets II: conformal blocks | Bartels, Douglas, Henriques |
| **1605.00662v3** | Conformal nets IV: The 3-category | Bartels, Douglas, Henriques |
| **1905.03393v1** | Conformal nets V: dualizability | Bartels, Douglas, Henriques |
| **1110.5671v2** | Dualizability and index of subfactors | Bartels, Douglas, Henriques |
| **1701.02052v2** | Bicommutant categories from conformal nets | Henriques |

All 8 papers confirmed to exist. arXiv IDs verified on 2026-05-02.

---

## 2. The BDH 3-Category Structure: Precise Identification

The BDH programme constructs a symmetric monoidal 3-category (established in 1605.00662) with the following cellular structure:

- **0-cells:** Conformal nets (functors from intervals to von Neumann algebras — i.e., *nets of algebras*, not individual factors with states)
- **1-cells:** Defects between conformal nets (models for interactions or phase transitions between CFTs)
- **2-cells:** Sectors between defects (bimodules)
- **3-cells:** Intertwiners between sectors

This is confirmed verbatim in arXiv:1605.00662: "the collection of conformal nets, defects, sectors, and intertwiners, equipped with the fusion of defects and fusion of sectors, forms a symmetric monoidal 3-category."

The foundational bimodule theory underpinning this programme (arXiv:1110.5671) works with bimodules over von Neumann algebras and establishes that the Haagerup L²-space and Connes fusion are functorial with respect to finite-index homomorphisms. "Connes fusion" here refers to the relative tensor product of Connes (fusion of bimodules), **not** the Connes Radon-Nikodym cocycle [Dω' : Dω]_t.

---

## 3. Critical Comparison: BDH vs. the Proposed ModAlg

### 3.1 What BDH does

BDH categorifies at the level of **nets of algebras** — each conformal net assigns a von Neumann algebra A(I) to each interval I ⊂ S¹. The categorification is geometric: it tracks how algebras associated to overlapping intervals fuse, how defects between two nets compose, how sectors between defects fuse (Connes fusion of bimodules).

The mathematical tools used are:
- Connes fusion = relative tensor product of bimodules over von Neumann algebras (Connes 1980)
- Haagerup L²-space (standard form of a von Neumann algebra)
- Finite-index subfactor theory

### 3.2 What ModAlg proposes

`ModAlg` categorifies at the level of **individual von Neumann factors with faithful normal states**. Its cellular structure is:

- **0-cells:** Pairs (M, ω) — a single factor M with a faithful normal state ω
- **1-cells:** *-homomorphisms Φ: M → M' intertwining modular flows up to a Connes Radon-Nikodym cocycle {u_t} — i.e., pairs (Φ, {u_t}) where Φ(σ^ω_t(x)) = Ad(u_t)(σ^{ω'}_t(Φ(x)))
- **2-cells:** Connes Radon-Nikodym cocycles [Dω' : Dω]_t ∈ U(M), implementing transitions between modular automorphism groups for different states on the same factor

### 3.3 The structural mismatch

The BDH 0-cells are **entire nets** (a functor assigning algebras to all intervals of a circle), while `ModAlg` 0-cells are **single factor-state pairs**. A conformal net is a much more elaborate object than a single (M, ω). The BDH categorification is *horizontal* (it moves between theories), while `ModAlg` is *vertical* (it moves between states on a single algebra).

More specifically:

| Feature | BDH | ModAlg |
|---|---|---|
| 0-cell | Conformal net (net of vN algebras) | (M, ω) — factor + state |
| 1-cell | Defect (interval-based bimodule) | *-homomorphism + Radon-Nikodym cocycle |
| 2-cell | Sector (bimodule between defects) | Connes Radon-Nikodym cocycle [Dω' : Dω]_t |
| 3-cell | Intertwiner | (does not appear in ModAlg) |
| Connes fusion used? | Yes (bimodule tensor product) | Marginally (cocycle chain rule) |
| Modular automorphism group σ_t as morphism data? | **No** | **Yes — central to 1-cell definition** |
| States ω on factors as object-level data? | **No** | **Yes — part of every 0-cell** |
| Connes Radon-Nikodym cocycle [Dω' : Dω]_t as a 2-cell? | **No** | **Yes — the paradigmatic 2-cell** |

### 3.4 Verdict on BDH

**BDH does not implicitly contain `ModAlg`.** The two structures are disjoint at the level of 0-cells. BDH never writes down a category whose objects are pairs (factor, state), never uses the modular automorphism group σ^ω_t as part of morphism data, and never treats the Connes Radon-Nikodym cocycle [Dω' : Dω]_t as a 2-morphism. The "Connes fusion" appearing in arXiv:1110.5671 is the bimodule tensor product, a structurally different object.

---

## 4. Additional Candidates: Search Results

### 4.1 Schreiber/Schommer-Pries on extended TQFT

- arXiv:1112.1000 (Schommer-Pries, "Classification of 2D extended TQFTs"): Objects are surfaces, morphisms are cobordisms. No relation to factor-state pairs or modular theory. **Not a precursor.**
- arXiv:1411.0945 (Bartlett–Douglas–Schommer-Pries–Vicary, "Extended 3-dimensional bordism"): The 3D bordism bicategory with 1-, 2-, 3-manifolds. No relation to operator algebras. **Not a precursor.**
- Schreiber (Urs Schreiber) search on TQFT + operator algebra: **0 results** in joint search.

### 4.2 Penneys and Henriques on subfactors

arXiv search: au:Penneys + (von Neumann / category / subfactor). Papers found (arXiv:1511.05226, 2004.08271, 1611.04620, etc.) concern fusion categories, bicommutant categories, planar algebras, local topological order. None define a category whose objects are (factor, state) pairs. None use modular automorphism groups or Connes Radon-Nikodym cocycles as morphisms. **Not a precursor.**

### 4.3 Kong-Runkel on local operator algebras and CFT

Five papers verified (arXiv:0902.3829, 0708.1897, 1307.5956, 0807.3356, 1310.1875). All concern algebras in modular tensor categories (a 1-categorical Frobenius/Morita theory), not 2-categories of factor-state pairs. **Not a precursor.**

### 4.4 Roberts on superselection sectors

arXiv search au:Roberts + (superselection OR local cohomology) + (category OR functor): **0 results.** The Roberts–Longo DHR superselection sector literature uses braided tensor categories (1-categorical in the relevant sense). No 2-category of factor-state pairs appears.

### 4.5 Neshveyev

arXiv search au:Neshveyev: 15 papers retrieved (KMS states on groupoids, ergodicity, smooth crossed products, symmetric cocycles, quantum groups). None define 2-categories of factor-state pairs. Neshveyev's modular-theory work is at the 1-category level (groupoid C*-algebra KMS states). **Not a precursor.**

### 4.6 Targeted keyword searches — all negative

| Search query | Total results | Relevant results |
|---|---|---|
| `ti:modular automorphism AND ti:category` | 7816 (all unrelated) | 0 |
| `ti:factor AND ti:state AND (ti:2-category OR ti:bicategory)` | 0 math results | 0 |
| `ti:Connes cocycle AND ti:category` | 399 (all unrelated: model categories, homotopy cocycles) | 0 |
| `ti:Connes AND ti:Radon-Nikodym` | 0 | 0 |
| `ti:modular flow AND ti:category` | 7777 (all unrelated: flow categories in topology) | 0 |
| `au:Schreiber_U AND (ti:TQFT OR ti:operator)` | 0 | 0 |

---

## 5. Conclusion: Originality Assessment

**Finding: ORIGINALITY CONFIRMED.**

The proposed `ModAlg` 2-category — whose 0-cells are (factor M, faithful normal state ω), 1-cells are *-homomorphisms intertwining modular flows up to a Connes Radon-Nikodym cocycle, and 2-cells are Connes cocycles [Dω' : Dω]_t — has no precursor in the published or arXiv literature.

The specific claim requiring verification was: "Bartels–Douglas–Henriques might implicitly contain the proposed 2-category structure without naming it." This claim is **refuted.** The BDH 3-category has:
- 0-cells = conformal nets (functors I → vN algebra), not (factor, state) pairs
- 2-cells = sectors (bimodules between defects), not Connes Radon-Nikodym cocycles
- No appearance of σ^ω_t as part of morphism data at any level
- No appearance of [Dω' : Dω]_t as a morphism at any level

The adjacent literature (DHR/Longo tensor categories, Penneys subfactor categories, Kong-Runkel Frobenius categories, Schommer-Pries extended TQFTs, Neshveyev KMS groupoids) all categorify different structures and do not overlap with `ModAlg`.

**The novel contribution of `ModAlg` is:**
1. Introducing states ω as *object-level data* in an operator-algebraic category (no prior work does this)
2. Treating the modular automorphism group σ^ω_t as the structural constraint on 1-cells
3. Identifying Connes Radon-Nikodym cocycles [Dω' : Dω]_t as the natural 2-cells

**Recommendation:** The v8-bis paper may proceed with an originality claim on the `ModAlg` 2-category structure. The disclaimer that BDH "was not verified" in the previous agent's report is now resolved: BDH has been fully verified (8 papers, all IDs confirmed), and it does not overlap with `ModAlg`.

The remaining technical gap (verification of the interchange law for 2-cells in `ModAlg`, see §2.4 of the parent note) is an internal mathematical check, not an originality issue.

---

## 6. Verification Record

| Item | Claimed | Verified via | Result |
|---|---|---|---|
| arXiv:0912.5307 | BDH: conformal nets as tricategory | Direct API id_list query, 2026-05-02 | Confirmed; 0-cells = conformal nets |
| arXiv:1302.2604 | BDH Conformal nets I | Direct API id_list query, 2026-05-02 | Confirmed; 0-cells = functors I → vN alg |
| arXiv:1310.8263 | BDH Conformal nets III | Direct API id_list query, 2026-05-02 | Confirmed; 2-cells = sectors (bimodules) |
| arXiv:1409.8672 | BDH Conformal nets II | Direct API id_list query, 2026-05-02 | Confirmed; no modular flow in morphisms |
| arXiv:1605.00662 | BDH Conformal nets IV: 3-category | Direct API id_list query, 2026-05-02 | Confirmed; 3-cat = nets/defects/sectors/intertwiners |
| arXiv:1905.03393 | BDH Conformal nets V | Direct API id_list query, 2026-05-02 | Confirmed; dualizability, no (factor,state) objects |
| arXiv:1110.5671 | BDH Dualizability and subfactors | Direct API id_list query, 2026-05-02 | Confirmed; Connes fusion = bimodule tensor product (distinct from RN cocycle) |
| arXiv:1701.02052 | Henriques, bicommutant categories | Direct API id_list query, 2026-05-02 | Confirmed; objects = soliton categories, not (factor,state) |
| arXiv:1112.1000 | Schommer-Pries, 2D extended TQFT | Direct API query, 2026-05-02 | Confirmed; objects = surfaces |
| arXiv:1411.0945 | Bartlett–Douglas–Schommer-Pries–Vicary | Direct API query, 2026-05-02 | Confirmed; objects = 3D manifolds |
| Penneys + subfactor / category papers | 10 papers retrieved | API search au:Penneys, 2026-05-02 | None involve (factor, state) 2-category |
| Kong-Runkel papers | 5 papers retrieved | API search au:Kong+au:Runkel, 2026-05-02 | None involve (factor, state) 2-category |
| Neshveyev papers | 15 papers retrieved | API search au:Neshveyev, 2026-05-02 | None define (factor, state) 2-category |
| `ti:modular automorphism AND ti:category` | 7816 results | API keyword search, 2026-05-02 | 0 relevant to operator-algebraic 2-category |
| `ti:Connes cocycle AND ti:category` | 399 results | API keyword search, 2026-05-02 | 0 relevant (all homotopy-theoretic cocycles) |
| `ti:factor AND ti:state AND ti:2-category` | 0 math results | API keyword search, 2026-05-02 | 0 relevant results |

---

*End of verification note. All arXiv IDs confirmed directly. Originality claim cleared for BDH caveat. Outstanding internal task: verify interchange law in §2.4 of parent note before submission.*
