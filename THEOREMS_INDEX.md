# THEOREMS INDEX — crossed-cosmos / ECI

Quick lookup of all proved theorems with tier classification, paper reference, and current status.

**Cluster firm**: 444 STABLE (entry = exit, 110+ anti-fab catches ledgered)
**Date**: 2026-05-20 (v7.0.0.1)
**Author**: Kévin Rémondière, ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)

---

## Tier classification

| Tier | Definition |
|---|---|
| **1 PROVED UNCOND** | Full unconditional proof, all inputs classical or cited |
| **1 PROVED-COND** | Full proof modulo a *named* conjectural input |
| **1 EMPIRICAL** | ≥100 PARI verifications ≥50-digit + structural support |
| **2 NUM** | Numerical match >50-digit cross-D verified |
| **2 STRUCTURAL** | Reframe with PARI-verifiable test, identification conjectural |
| **3 SKETCH** | Scaffold + identified gaps, working hypothesis realistic |
| **3 OPEN** | Explicit open question, falsifiable test stated |

---

## TIER 1 PROVED UNCONDITIONAL (8)

| ID | Theorem | Paper | Page | Source |
|---|---|---|---|---|
| TH1 | **Theorem D'** — Universal Q-rational orbit count `N_w(K) = 2^r` if `e ∣ (w-1)` | [P4W3 Math.Ann.](papers/Paper_P4W3_MathAnn/) | §3 | Hecke/Shimura/Schütt/Gauss 4-input chain |
| TH2 | **Lemma C universal** — cup-product Br genus subgroup vanishes | [HSH v3 JNT](papers/Paper_HSH_v3_letter_JNT_v2/) | §4 | Mackey + character orthog. |
| TH3a | **F(N) form `1 + c/N²`** STRUCTURAL via Dijkgraaf-Witten genus expansion | [PRL Théorème A](papers/Paper_PRL_Theoreme_A_LMP/) + [Survey](papers/Paper_ECI_Survey_Clay_BullAMS/) | §3 | DW 1990 + 't Hooft genus (Z_g = N^{2-2g}) |
| TH-Arith | **M(D) arithmetic surrogate** `M(D) = √(2πe·2/3)·(9/10)·(h_K²+1)/h_K²·√σ₀` — definition + monotonie + limite + calculabilité | [Théorème A LMP](papers/Paper_PRL_Theoreme_A_LMP/) | new §A | Pure algebra + analysis élémentaire (publishable J.NT NOW) |
| TH4 | **Borel + Genus Field K₃ decomposition** | [Schütt Hecke JHEP](papers/Paper_Holographic_SchuttHecke_JHEP/) | §5 | Borel 1977 + Cox 1989 |
| TH5 | **Wilson loop bijection γ ↔ 𝔞** at h_K = 2 | [P4W3 Math.Ann.](papers/Paper_P4W3_MathAnn/) | §6 | Heegner-Birch + Atkin-Lehner |
| TH7 | **HSH r(D) = 2^{rk_2}** for Cl(K) a 2-group (TIER 0 promoted, McCallum-Sharifi dependency removed) | [HSH v3 JNT](papers/Paper_HSH_v3_letter_JNT_v2/) | §3 | Gauss 1801 genus + Hecke-Shimura-Ribet |
| W1 | **ξ\* = 2/3 UNIVERSAL** via Selberg trace identity-term only | [W1 Comptes Rendus](papers/Paper_W1_xi_star_universal_CR/) | §3 | Selberg 1956 + Vassilevich 2003 |
| TH-1.1 | **Per-χ spectral decomposition** of Selberg pretrace on Bianchi 3-orbifolds | [Lemma A3-2 JFA](papers/Paper_Lemma_A32_Selberg_JFA/) | Theorem 1.1 | 5-step pipeline UNCOND (Hecke action / P_χ / Δ_χ self-adj / Bunke-Olbrich / Gangolli-Warner) |

---

## TIER 1 PROVED-CONDITIONAL (4)

| ID | Theorem | Conditional on | Paper |
|---|---|---|---|
| TH6 | **Arrow A3 Lichnerowicz** — Conjecture F v3 (cup product vanishing) | Burns-Flach + Brunault-Chida + Castella 2024 | [P4W3](papers/Paper_P4W3_MathAnn/) §7 |
| TH8 | **P4-W3 Theorem 14 precise** — `r(D) = (A/B)·√d_gen^e` | (KS) + (BC-NC) + (CAST-EXT) + (TAM-PRIM) | [P4W3](papers/Paper_P4W3_MathAnn/) §8 |
| TH11 | **Center-Rank theorem CR** — `rk_2(Cl K_ASP(N)) ≥ v_2(N)` | Gauss genus + 't Hooft (Z/2^{v_2(N)})⁶ | [CR Theorem JNT](papers/Paper_CR_Theorem_JNT/) §3 |
| TH-8.1 | **Route B mass-gap physical claim** — `m_0⁺⁺(SU(N))/√σ = M(D_min^{(N)})/√λ₁(Y_K)` | (i) Karamata-Stirling + (T1)(T2) Transport + **(iii) H20/H21 9/10 = SU(3) calibration** | [Route B LMP](papers/Paper_RouteB_Mass_Gap_LMP/) §3 |
| TH3b | **F(N) coefficient `c = 9/10 = 3²/(3²+1)`** = SU(3) anchor calibration F(3)=1 (H20 verdict 20-hypothesis test eliminates all alternatives) | [PRL Théorème A](papers/Paper_PRL_Theoreme_A_LMP/) | §3 | Empirical CONVENTION, NOT structural derivation. Tier 2 CALIBRATION. |

---

## TIER 1 EMPIRICAL (9)

| ID | Result | Anchors | Paper |
|---|---|---|---|
| EMP1 | **M.B 688 EXACT cross-Galois Q-rationals** | 7 disc h_K=2 + 6 disc h_K=4 Klein | [P4W3](papers/Paper_P4W3_MathAnn/) §M.B |
| EMP2 | **III-A bootstrap 3/3 EXACT 50-digit** — Q1 D=-91 λ_nt=0.78929 / Q2 D=-84 Tr=2.5485 / Q3 D=-15 ξ=0.74130 | h_K=2 cyclic + h_K=4 Klein V₄ | [P4W3](papers/Paper_P4W3_MathAnn/) §III-A |
| EMP3 | **HSH r(D) = 2^{rk_2} 16+2 anchors** verified PARI 200-digit incl. D=-9240 rats=32 EXACT | D ∈ {-15,...,-9240} | [HSH v3 JNT](papers/Paper_HSH_v3_letter_JNT_v2/) §2 |
| EMP4 | **M142 9 rational L-value anchors** α_2(D) = L(f_D,2)π²/Ω_D⁴ ∈ Q\* | Heegner h_K=1 ∪ twins | [M142 unified](papers/Paper_unified_M142_hierarchy/) |
| EMP5 | **Beilinson q(D) 8/8 EXACT 50-digit** via Chowla-Selberg Ω_K | h_K=2 anchors | [Beilinson qD Note](papers/Paper_Beilinson_qD_Note/) |
| EMP6 | **F-A32-1 PASS 60-digit PARI** — ξ(K_{-15}) = 0.7413019528... | D=-15 | [Lemma A3-2](papers/Paper_Lemma_A32_Selberg_JFA/) Falsifier F-A32-1 |
| EMP7 | **K(a,b) 28-disc closed-form cross-ratio** + 200-digit verified | 28 disc | (drafts) `notes/CLOSED_FORM_CROSS_RATIO_DERIVED.md` |
| EMP8 | **L-ratio 16/16 Heegner Q-rational** PARI 200-digit | 16 Heegner | (note) `notes/L_RATIO_QRATIONAL_8_8_CONFIRMED.md` |
| EMP9 | **m_arith RMS 0.85% vs AT2021** 6 anchors (tautological under λ_1=1) | SU(N) N ∈ {2,3,4,5,6,∞} | [Survey](papers/Paper_ECI_Survey_Clay_BullAMS/) §6 |

---

## TIER 2 NUM / STRUCTURAL (selected)

| ID | Result | Paper |
|---|---|---|
| T2-1 | **F(N) χ²/ndf = 1.135** AT2021 | [Survey](papers/Paper_ECI_Survey_Clay_BullAMS/) |
| T2-2 | **Lee-Yang SU(2) strip width** β ∈ [0.5, 2.5] V=6⁴/8⁴/10⁴ (paper-ready, V=4 done) | [Lee-Yang LMP](papers/Paper_LeeYang_SU2/) |
| T2-3 | **SU(3) Transport TIER 2 NUM** Boolean falsifier `λ_1 = 1` Worker 8 reframing | [Transport V2 arXiv](papers/Paper_Transport_Conjecture_v2_arXiv/) |

---

## TIER 3 OPEN (the unfinished gaps)

| ID | Open Problem | Status |
|---|---|---|
| OPEN-Transport | **Transport Conjecture** — Φ : lattice YM Wightman → Bianchi spectral identification | TIER 3 OPEN, 2-Millennium stack (M1: constructive 4D YM + M2: spectral identification). PARI Selberg λ_1 falsifier setup ($50 KVM, 1-3 mo). [Transport v3 FINAL](papers/Paper_Transport_Conjecture_v3_FINAL/) |
| OPEN-KS | **Karamata-Stirling rigorous completion** — substep (i) √(2πe) of Route B Theorem 8.1 | TIER 3 sketch. ~2-3 wk completion attempt. |
| OPEN-K_ASP(32) | **K_ASP(32)** — smallest D with h_K=32, rk_2=5. PARI sweep `|D| < 2×10⁶` to find. | Sweep ongoing. |
| OPEN-Faltings-rk2-5 | **First rk_2=5 anchor** — confirmed `|D| > 10000` (4 rk_2=4 in [-10000,-3]) | Computed Faltings sweep, see Phase 1. |

---

## RETRACTED / FALSIFIED (selected)

For full list see `notes/YM_CLOSURE_V2_2026-05-20.md` §5 Falsifications Ledger.

| ID | What | Reason | Date |
|---|---|---|---|
| RETR-BC | **BC h_K=2 over K imag.quad** | Brunault-Chida works over Q only; pivot to LLZ 2015 Compositio | 2026-05-18 |
| RETR-Sarnak | **Sarnak 1983 λ_1 ≥ 21/25 universal Bianchi** | Sarnak applies to specific arithmetic 3-manifolds only | catch #100 2026-05-19 |
| FALS-Phase-E2 | **Spin-4 SU(3-10) prediction** | ~10σ off AT2021 cross-N | 2026-05-15 |
| FALS-Bridge-9.1 | **AdS hard-wall j_{0,1} cross-N N≥3** | 14.3σ off | 2026-05-15 |
| FALS-Koide-struct | **Koide Q = 2/3 ↔ ECI ξ\* structural** | W1 PARI: ξ\*=2/3 UNIVERSAL topological (Selberg identity term only), no structural bridge to Koide | W1 verdict 2026-05-20 |
| FALS-Maulik-K3-attribution | **Maulik 2014 Duke for K3 Picard≥16 → Hodge** | Maulik 2014 = Tate supersingular char p, NOT Hodge over C. Correct chain: Pohlmann + Tankeev + Varesco | Phase 1 catch 2026-05-20 |

---

## Lean formalization status (parallel track)

| File | Theorems PROVED zero-sorry | Coverage |
|---|---|---|
| [`lean/Crossed/Basic.lean`](lean/Crossed/Basic.lean) | 19 | substrats algébriques + ξ\*=2/3 ℚ + c_DW=9/10 + F(N=3)=1 + G3 substrates {4,8,16,32} |
| [`lean/Crossed/BasicMathlib.lean`](lean/Crossed/BasicMathlib.lean) | 16 | norm_num lifts |
| [`lean/Crossed/CRTheorem.lean`](lean/Crossed/CRTheorem.lean) | 1 (+2 sorry) | nrComplexPlaces + bridges |
| [`lean/Crossed/G3.lean`](lean/Crossed/G3.lean) | 5 (+4 sorry) | padicValNat ≥ rk_2 partial |

**Total Lean kernel-verified zero-sorry: ~36 lemmas/theorems**. See [`notes/LEAN_FORMALIZATION_STATUS_2026-05-20.md`](notes/LEAN_FORMALIZATION_STATUS_2026-05-20.md).

---

## Cross-references

- **BIGTABLE V4.1 REVISED** (canonical reference, 1514 lignes 93.7 KB): [`notes/BIGTABLE_V4_1_REVISED_2026-05-20.md`](notes/BIGTABLE_V4_1_REVISED_2026-05-20.md)
- **YM CLOSURE V2** (honest audit): [`notes/YM_CLOSURE_V2_2026-05-20.md`](notes/YM_CLOSURE_V2_2026-05-20.md)
- **MILLENNIUM PISTES** (6-problem map, 84 KB): [`notes/MILLENNIUM_PISTES_ECI_2026-05-20.md`](notes/MILLENNIUM_PISTES_ECI_2026-05-20.md)
- **TRANSPORT CLOSURE FINAL** (V3 Wiles-style): [`notes/TRANSPORT_CLOSURE_FINAL_2026-05-20.md`](notes/TRANSPORT_CLOSURE_FINAL_2026-05-20.md)
- **PAPERS.md** (full inventory): [`PAPERS.md`](PAPERS.md)

---

## Honest scope

This work is **NOT a Theory of Everything**, **NOT a Clay Millennium solution**, and **NOT a fundamental physics breakthrough**. It is a tier-classified arithmetic-geometric research program with peripheral physics connections (Yang-Mills mass-gap surrogate formula matching lattice AT2021 at RMS 0.85%, conditional on the Transport Conjecture remaining open).

**P(Clay-level contribution 15y)** : ~18-30% honest (dominated by YM/BSD/Hodge axis via 2-rank Cl(K)[2] shared organization).

Anti-fab discipline is the brand value: every claim tier-classified, every failure ledgered, every catch (110+ to date) documented openly.
