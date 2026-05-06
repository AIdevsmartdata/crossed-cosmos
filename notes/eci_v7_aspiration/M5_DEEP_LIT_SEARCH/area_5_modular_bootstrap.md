# Area 5: Modular Bootstrap / MSS (hep-th)
**Search date:** 2026-05-06
**Queries used:**
- `cat:hep-th AND (ti:"modular bootstrap" OR ti:"lightcone bootstrap" OR ti:"chaos bound" OR ti:"Lyapunov exponent")`
- `cat:hep-th AND (ti:"OPE coefficient bound" OR ti:"Cardy formula" OR ti:"density of states")`
- `cat:hep-th AND ti:"bootstrap"`
- `cat:hep-th AND (ti:"chaos bound" OR ti:"scrambling" OR ti:"out-of-time-order")`

**Papers post-2026-04-01 verified:**

---

## P5-A1: ADJACENT

**ID:** 2604.11277v2
**DATE:** 2026-04-13 (revised; originally April 2026)
**AUTHORS:** Suresh Govindarajan, Akhila Sadanandan
**TITLE:** Updating the holomorphic modular bootstrap
**ABSTRACT (verified):** Updates holomorphic modular bootstrap with exact S-matrix from Modular Linear Differential Equations (MLDE). Finds admissible solutions with up to six characters and Wronskian index < 6. Identifies solutions with good fusion rules and associated modular tensor category (MTC) structure.
**CLASSIFICATION: ADJACENT**
**ECI RELEVANCE:** Holomorphic modular bootstrap — extension of the MLDE classification program. ECI's modular shadow paper (P4: Modular Shadow LMP) addresses the MSS bound via a different approach (finite-rank theorem for modular shadows). The Govindarajan-Sadanandan work extends rational CFT classification, not OPE coefficient bounds. ADJACENT: shares the "modular" vocabulary but different sub-area (RCFT classification vs. OPE bounds). No direct impact on ECI's MSS bound claim.
**NOTE:** Live-verified at https://arxiv.org/abs/2604.11277.

---

## P5-A2: ADJACENT

**ID:** 2604.01275v2
**DATE:** 2026-04-01 to 2026-05-04 (revised multiple times)
**AUTHORS:** Nathan Benjamin, A. Liam Fitzpatrick, Wei Li, Jesse Thaler
**TITLE:** Descending into the Modular Bootstrap
**ABSTRACT (verified):** Machine-learning optimization searches for 2D CFT solutions to modular bootstrap equations. Loss function from modular invariance. Novel singular-value-based optimizer (Sven). Explores central charges c ∈ (1, 8/7) — previously unexplored range devoid of known CFT examples. Finds candidate CFTs and improved spectral gap constraints near c=1.
**CLASSIFICATION: ADJACENT**
**ECI RELEVANCE:** Machine-learning modular bootstrap for 2D CFTs at low c — this is the exact sub-area that ECI's modular shadow conjecture operates in (MSS bound applies to 2D CFTs). The improved spectral gap constraints near c=1 are potentially relevant: ECI's Cardy paper works in the regime of large c (Cardy universality), while this paper focuses on small c. No direct challenge to ECI's MSS-bound result or Cardy ρ=c/12 universality. ADJACENT.
**STRATEGIC NOTE:** Benjamin-Fitzpatrick-Li-Thaler is a significant group (Benjamin, Fitzpatrick, Thaler all prominent). This paper could generate followup that directly addresses MSS bounds. Monitor.
**NOTE:** Live-verified at https://arxiv.org/abs/2604.01275.

---

## P5-A3: ADJACENT

**ID:** 2604.25495v1
**DATE:** 2026-04-28
**AUTHORS:** Mozib Bin Awal, Prabwal Phukon
**TITLE:** Phase Transitions and Chaos Bound in Horava Lifshitz Black Holes using Lyapunov Exponents
**ABSTRACT (verified):** Lyapunov exponent analysis for Horava-Lifshitz black holes. Multivalued dependence on temperature during first-order phase transitions (small/intermediate/large BH phases). Tests MSS/Maldacena chaos bound λ_L ≤ 2πT.
**CLASSIFICATION: ADJACENT**
**ECI RELEVANCE:** Tests chaos bound λ_L ≤ 2πT in Horava-Lifshitz geometry. ECI's MSS connection is through the Modular Shadow finite-rank theorem (A11/A61), not through Lyapunov exponents directly. The Horava-Lifshitz setting is non-standard (Lorentz-violating). No direct impact on ECI's modular shadow claim.
**NOTE:** Live-verified at https://arxiv.org/abs/2604.25495.

---

## P5-A4: ADJACENT

**ID:** 2604.26600v1
**DATE:** 2026-04-29
**AUTHORS:** Levy B. N. Batista, Nicolò Bragagnolo, Rhys Holmes
**TITLE:** Entanglement Revivals and Scrambling for Evaporating Black Holes
**ABSTRACT (verified):** Entanglement spreading and memory effects in 2D CFT on evaporating black hole backgrounds. Memory effects causing late-time spikes in mutual information for widely separated intervals.
**CLASSIFICATION: ADJACENT**
**ECI RELEVANCE:** Scrambling in evaporating black hole context — tangentially related to MSS bound (scrambling time). No direct connection to ECI's modular shadow or Cardy result. ADJACENT.
**NOTE:** Live-verified at https://arxiv.org/abs/2604.26600.

---

## Searches returning no results post-2026-04-01:

- Direct MSS (Maldacena-Shenker-Stanford) followups: none found
- "OPE coefficient bound" papers: none in 2026
- "lightcone bootstrap" papers: none in 2026
- Higher-genus modular bootstrap: none (consistent with A77 finding that g≥2 is not active)

---

## Area 5 — Meta-assessment

**Key finding:** No 2026 paper directly improves or challenges the MSS bound. No higher-genus (g≥2) modular bootstrap paper found, confirming A77's conclusion that g≥2 bootstrap is dormant.

**Most significant finding:** Benjamin-Fitzpatrick-Li-Thaler (2604.01275) machine-learning modular bootstrap explores c ∈ (1, 8/7) — a new region of CFT space. This could eventually intersect with MSS-related constraints but doesn't yet. ECI's modular shadow paper remains at the frontier.

**ECI's Cardy ρ=c/12 paper** (proved for unitary diagonal MIP CFTs): No 2026 challenger found. The holomorphic modular bootstrap (Govindarajan-Sadanandan) focuses on rational CFTs with c_eff ≤ 24, not on asymptotic density of states.

**Recommended action:** Cite Benjamin et al. 2604.01275 in modular shadow LMP §1 (introduction) as showing the modular bootstrap landscape is being explored with new methods. Note A77's confirmed finding that g≥2 bootstrap doesn't extend ECI's A61 pillars.
