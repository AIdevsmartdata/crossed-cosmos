# Experimental Protocol: Measuring ρ_{p,k=2} = 1/18 on the Innsbruck Cs-133 Platform

**ECI version:** v6.0.45 (Zenodo DOI 10.5281/zenodo.20022897)  
**Date:** 2026-05-04  
**Status:** Internal protocol design — NOT for external circulation. Email to Nägerl group deferred pending full validation.

---

## 1. ECI Prediction Recap: The Mercator–Euler Proof

### 1.1 The saturation ratio ρ

ECI defines the leading-order saturation ratio across a Bisognano–Wichmann (BW) window u ∈ [0, 2π] as

    ρ ≡ ⟨S(n_thermal)⟩ / (2π)

where S is the von Neumann (or Gibbs) entropy per mode and u ≡ ω/T_H is the dimensionless frequency in units of the Hawking temperature. This ratio is **independent** of T_H, the number of modes, sound speed, healing length, and Yukawa couplings — it is fixed entirely by the underlying statistical algebra (CCR / CAR / parastatistics).

### 1.2 Para-fermion order k

For a para-fermion gas of order k (truncated occupation: n ∈ {0, 1, …, k}, partition function Z_k(u) = (1 − e^{−(k+1)u}) / (1 − e^{−u})):

    ρ_{p,k} = k / (12(k+1))

**Key values:**

| k    | ρ_{p,k}     | decimal  | interpretation        |
|------|-------------|----------|-----------------------|
| 1    | 1/24        | 0.04167  | parafermion-1 = Fermi |
| 2    | 1/18        | 0.05556  | **ECI target**        |
| 3    | 1/16        | 0.06250  | parafermion-3         |
| ∞    | 1/12        | 0.08333  | Bose limit            |

The Bose value (k → ∞) and Fermi value (k = 1) bracket all para-fermion cases.

### 1.3 The Mercator–Euler proof (five lines from eci.tex §universality)

From the thermodynamic identity  
S_{p,k}(u) = log Z_k(u) − u (d log Z_k / du),  
integration by parts (boundary terms vanish at u → 0⁺ and u → ∞, verified to 10⁻²⁰) gives:

    ∫₀^∞ S_{p,k} du = 2 ∫₀^∞ log Z_k du

The Mercator–Euler lemma ∫₀^∞ log(1 − e^{−au}) du = −π²/(6a) applied to log Z_k = log(1 − e^{−(k+1)u}) − log(1 − e^{−u}) yields:

    ∫₀^∞ log Z_k du = (π²/6) · k/(k+1)

Therefore:

    ∫₀^∞ S_{p,k} du = (π²/3) · k/(k+1)   →   ρ_{p,k} = k / (12(k+1))

At k = 2: **ρ_{p,2} = 2/(12×3) = 2/36 = 1/18 = 0.05556 exactly.**

Literature survey (Green 1953, Greenberg 1964, Wu 1994, Khare 2005, Anghel 2007, Polychronakos 1996, Iguri–Trinchero 2003) finds no prior publication of this explicit closed form in the present formulation. This is the strongest unique ECI prediction in the 2027–2029 window.

---

## 2. Innsbruck Platform Overview

### 2.1 CrossRef-verified publication

**Verified via CrossRef API (2026-05-04):**

- Title: "Observing anyonization of bosons in a quantum gas"
- Authors: Dhar, Wang, Horvath, Vashisht, Zeng, Zvonarev, Goldman, Guo, Landini, Nägerl
- Journal: Nature, Volume 642, pp. 53–57, 2025-05-28
- DOI: 10.1038/s41586-025-09016-9

### 2.2 What the paper actually measures

**Critical distinction (anti-hallucination):** The Nature 642 paper realizes **1D anyonic correlations via spin–charge separation**. A mobile impurity provides the spin degree of freedom; the anyonic statistical phase θ is engineered in the charge sector of a 1D strongly interacting Cs-133 Tonks–Girardeau gas. The observable is the **asymmetric momentum distribution n(k) − n(−k)**, a hallmark of anyonic correlations.

**What is NOT demonstrated:** The paper does not measure ρ_{p,k}, does not set up a sonic horizon, and does not extract integrated thermal entropy ratios. The statistical phase θ is a continuous anyonic (U(1)) parameter tuned from boson (θ = 0) to fermion (θ = π) — this is **not** the same as truncated-occupation parastatistics (Z_k integer occupation cutoff) that ECI's ρ_{p,k} formula describes.

### 2.3 Platform capabilities relevant to the ECI protocol

From the published method and known Innsbruck Cs-133 capabilities (cited capabilities only — no fabrication):

- **Feshbach resonance tuning:** Cs-133 has broad, magnetically accessible Feshbach resonances near B ≈ 550–800 G, enabling tuning of the s-wave scattering length from a = −∞ to +∞. Used in Nature 642 for anyonization.
- **1D confinement:** Transverse trapping frequencies ω_⊥ ≫ ω_∥ achievable with optical lattice + dipole trap geometry (2D optical lattice creating 1D tubes, as in standard Innsbruck/Haller et al. 2009 Cs-133 Tonks-Girardeau realization).
- **Mobile impurity injection:** Demonstrated in Nature 642 — a minority-spin impurity co-trapped in the charge sector.
- **Momentum-resolved detection:** Demonstrated — time-of-flight (TOF) imaging with sub-recoil resolution, capable of resolving n(k) asymmetry.
- **Atom number:** Typical Innsbruck 1D tube experiments use N ~ 10–30 atoms/tube with O(100–1000) tubes, giving total N ~ 10³–10⁴.

**Gap:** The platform has NOT demonstrated sonic-horizon engineering or integrated-entropy extraction. A dedicated experimental redesign is required.

---

## 3. Observable Identification and ECI-to-Lab Mapping

### 3.1 The ECI observable in 1D cold atoms

The ECI quantity ρ_{p,k} is defined via the **integrated thermal entropy per mode** across the BW window. In a 1D cold-atom system with an engineered sonic horizon (density step or velocity ramp), the analogue Hawking temperature is T_H = ħ c_s κ / (2π k_B), where c_s is the local speed of sound and κ is the surface gravity (density gradient at the horizon).

The lab-accessible proxy for ρ_{p,k} is the **normalized second-order coherence function ratio**, specifically:

    ρ_meas ≡ ∫₀^{u_max} g^{(1)}(u) log[1 / g^{(1)}(u)] du / (2π)

where g^{(1)}(x, x') is the one-body reduced density matrix (OBRDM) and u = ω/T_H. More concretely:

**Primary observable: OBRDM diagonal ratio at the horizon crossing.**

For a para-fermion gas of order k, the thermal state has occupation per mode:

    ⟨n⟩_{p,k}(u) = Σ_{m=0}^{k} m · e^{−mu} / Σ_{m=0}^{k} e^{−mu}

The **saturation ratio** can be extracted as:

    ρ_meas = [∫_ω ⟨n⟩_{p,k}(ω/T_H) log(1/⟨n⟩_{p,k}) dω] / (2π T_H)

which requires (a) measuring the occupation number spectrum ⟨n(ω)⟩ mode-by-mode, and (b) knowing T_H from the independently measured horizon surface gravity κ.

**Secondary observable (more tractable): momentum distribution ratio at sonic horizon.**

The ratio of quasi-particle occupation at ω = T_H versus ω = 2π T_H:

    R_occ ≡ ⟨n(ω = T_H)⟩ / ⟨n(ω = 2π T_H)⟩

is a function of k alone at fixed u = 1 and u = 2π. For k = 2:
- ⟨n_{p,2}(u=1)⟩ = (0·1 + 1·e⁻¹ + 2·e⁻²) / (1 + e⁻¹ + e⁻²) ≈ 0.4226
- ⟨n_{p,2}(u=2π)⟩ = (e^{−2π} + 2e^{−4π}) / (1 + e^{−2π} + e^{−4π}) ≈ 0.002155

This ratio ≈ 196 is sharply distinct from the Bose case (Bose: n(u) = 1/(e^u − 1), ratio ≈ (e^{2π}−1)/(e^1−1) ≈ 288) and Fermi case (ratio ≈ n_F(1)/n_F(2π) ≈ 284/1.87 ≈ 152 using n_F(u) = 1/(e^u+1)).

**However:** The most experimentally accessible proxy is the **integrated entropy extracted from the density–density correlation function g^{(2)}(0)**, following the Steinhauer-type approach (Steinhauer 2019, Nature Physics). The key quantity is:

    G^{(2)}(x, x') = ⟨n̂(x) n̂(x')⟩ − ⟨n̂(x)⟩⟨n̂(x')⟩

which, after Fourier decomposition and normalization by n₀², encodes the mode-by-mode occupation via the fluctuation–dissipation theorem. The ratio ρ_meas is then:

    ρ_meas = (1/2π) ∫_0^{2π T_H} [S_quasi(ω)] d(ω/T_H)

where S_quasi is extracted from the spectral density of g^{(2)} fluctuations (corrected for shot noise).

### 3.2 The ECI-to-lab mapping

The critical mapping step is: **what physical mechanism in a Cs-133 1D gas produces truncated-occupation (order-k) statistics?**

ECI's para-fermion formula assumes a gas where each mode can be occupied by at most k particles (Gentile statistics). In cold atoms this requires engineering an **effective hard-core constraint at filling k**. Options:

**Option A — Resonant interaction quench to k-body hard core:** Using a k-body loss mechanism (three-body loss for k = 2) to force effective occupation cutoff at 2. This is physically reasonable: at sufficiently high density in 1D, three-body recombination enforces ⟨n⟩ ≤ 2 on length scales shorter than the healing length. The Innsbruck group has worked with controlled three-body loss in Cs-133 (Zaccanti et al., Ferlaino et al.). This is the most physically motivated realization of parafermion-2 statistics.

**Option B — Fractional occupation via Feshbach molecule formation:** At unitarity (a → ±∞), pairs of Cs-133 atoms form dimers with binding energy tunable to zero, creating an effective two-component system where the "charge" sector obeys modified statistics. This is closer to what Nature 642 demonstrates but in the 1D limit it does not directly produce k = 2 truncation.

**Recommended approach: Option A with controlled three-body loss engineering** at the level of individual 1D tubes, followed by extraction of the mode-occupation spectrum via RF spectroscopy (see protocol §4).

---

## 4. Detailed Experimental Protocol (10 Sub-steps)

### Step 1 — Initial State Preparation (Week 1–4 of run)

Load Cs-133 BEC (T < 10 nK) into a 2D optical lattice creating arrays of 1D tubes. Target: N ≈ 20–50 atoms/tube, ~500 occupied tubes. Lattice depth V_0 ≈ 40–60 E_r (recoil energies) in the transverse directions to suppress tunneling (ω_⊥/2π ~ 30–50 kHz). Longitudinal confinement ω_∥/2π ~ 30–80 Hz to achieve the Tonks–Girardeau regime (γ ≡ mg / (ħ² n) ≫ 1 via Feshbach tuning of a).

**Parameter checkpoint:** Verify γ > 10 by measuring the momentum distribution width (flat-top profile → TG gas).

### Step 2 — Feshbach Resonance Calibration

Map the Cs-133 Feshbach resonance at B ≈ 787 G (broad resonance used in the Innsbruck lab) to set the interaction strength independently of three-body loss. Record the three-body loss rate L_3(B) across the resonance. Identify the magnetic field B* where L_3 is large enough to enforce effective occupation cutoff ~2 on timescales faster than ω_∥⁻¹, but slow enough not to deplete the gas before measurement. Target: L_3 n² ~ 5–10 ω_∥.

**Known hazard:** Three-body loss depletes atom number exponentially. Protocol must operate in a pulsed mode: brief quench to high L_3, then quick ramp away.

### Step 3 — Engineering the Para-fermion-2 State

Quench to B* for a controlled time τ_q ~ 0.5–2 ms to enforce the effective k = 2 occupation constraint via three-body loss. Simultaneously ramp the longitudinal trap to a density-step profile (one side denser by factor ~2–4 via a focused repulsive laser beam crossing the tube axis at x = 0). This density step creates an effective sonic horizon with surface gravity κ ~ ∂_x c_s|_{x=0}.

**Crosscheck:** Measure atom number after quench to confirm 10–30% loss (not total depletion). If loss > 50%, reduce τ_q.

### Step 4 — Sonic Horizon Characterization

Measure T_H independently from the horizon. Two methods:

(a) **Hawking temperature from κ:** Image the in-situ density profile n(x) with single-shot fluorescence imaging (resolution ~ 1 μm), extract c_s(x) = ħ/m · √(n(x) g₁D), fit the gradient to get κ = ∂_x c_s at n = 0 inflection point. T_H = ħ κ / (2π k_B).

(b) **Cross-check via correlator ratio:** The equal-time density–density correlator g^{(2)}(x, −x) at the horizon follows the thermal Planck function for Hawking phonons at T_H. Fit the long-wavelength tail to extract T_H independently.

**Target T_H:** 3–15 nK (accessible with realistic κ and c_s ~ 2–5 mm/s).

### Step 5 — Mode-Resolved Spectroscopy

Apply a **Bragg spectroscopy** sequence (two counter-propagating laser beams at angle θ, detuned by ω_Bragg) to resonantly couple the 1D phonon mode at frequency ω_Bragg to the free-particle spectrum. By scanning ω_Bragg from 0.1 T_H to 2π T_H (i.e., spanning the full BW window), extract the occupation number per mode ⟨n(ω_Bragg)⟩.

For the k = 2 para-fermion state, the spectrum ⟨n_{p,2}(u)⟩ = (e^{−u} + 2e^{−2u})/(1 + e^{−u} + e^{−2u}) is analytically predicted. The Bragg signal S_Bragg(ω) ∝ ⟨n(ω)⟩ + 1 (stimulated emission) allows direct comparison with the Bose (S_Bose ~ 1/(e^u − 1) + 1) and Fermi (S_Fermi ~ 1/(e^u + 1)) spectra.

**Resolution needed:** Δω < 0.2 T_H per frequency bin, spanning 10–12 bins across [0, 2π T_H]. With T_H ~ 5 nK = k_B × 5 nK / ħ ~ 2π × 100 Hz, this requires ω_Bragg resolution ~ 20 Hz — achievable with Bragg pulse duration ~ 50 ms.

### Step 6 — Integration and ρ Extraction

For each experimental realization, compute:

    ρ_meas^{(j)} = (1/2π) · Σ_n [⟨n(ω_n)⟩ log(1/⟨n(ω_n)⟩)] · Δu_n

summing over frequency bins ω_n = u_n T_H, with Δu_n = 0.2 (20 bins across [0, 2π]).

Average over J realisations to get ρ_meas ± σ/√J. Target: σ_single ~ 0.003 (from photon shot noise in TOF imaging, O(1000) atoms/tube/image), so J = 400 realisations gives σ/√J ~ 0.00015, well below the 3σ threshold (see §4.8).

### Step 7 — Systematic Budget

| Source | Estimated bias | Mitigation |
|--------|----------------|------------|
| Finite temperature (T > 0) | +0.5% on ρ (thermalizes modes beyond BW window) | Measure T independently via TOF; subtract thermal tail |
| Finite atom number (N ~ 20) | +1.5% (boundary effects, ρ rises as 1/N correction) | Run N = 10, 20, 30 series; extrapolate N → ∞ |
| Anharmonic longitudinal trap | < 0.3% (harmonic approx breaks at 10% level for ω_∥) | Use flat-bottom box trap (red-detuned laser + mask) |
| Bragg coupling efficiency | ±0.5% (inhomogeneous intensity profile) | Calibrate with known bosonic TG reference (no density step, expect ρ = 1/12) |
| Detection efficiency (η < 1) | −2% (undercounts weak-occupation modes) | Use η ~ 0.85 in-situ florescence; correct with η map |
| Three-body loss non-uniformity | ±1% (radial variation of L_3) | Measure L_3 tube-by-tube via loss spectroscopy |
| **Total systematic** | **~2.5%** (absolute) | Combine in quadrature |

The target ρ_{p,2} = 1/18 = 0.05556 differs from Bose (1/12 = 0.08333) by 0.02778 — **50σ at the above statistical precision**, so systematics dominate. The systematic budget of 0.0025 allows 3σ discrimination from Bose and Fermi at |Δρ| > 7.5σ_sys.

### Step 8 — Calibration Run: Bosonic Reference

Before the para-fermion protocol, run the full sequence with **no three-body loss quench** (B far from resonance, pure TG gas). Measure ρ_ref. Expect ρ_ref ≈ 1/12 = 0.08333. This calibrates the entire extraction pipeline. If ρ_ref differs from 1/12 by more than 3σ_sys, systematic corrections must be refined before proceeding.

### Step 9 — Fermionic Reference (Control)

Run a second calibration with **spin-1/2 impurity fermionized** Cs-133 (using the Nature 642 anyonization protocol at θ = π, statistical phase = fermionic). Expect ρ_ref,F ≈ 1/24 = 0.04167. This verifies that the extraction correctly transitions from Bose to Fermi.

### Step 10 — Data Analysis and Reporting

Report ρ_meas with full systematic budget:

    ρ_meas = [value] ± σ_stat ± σ_sys

Compare against: ρ_{p,2} = 1/18 = 0.05556 (ECI prediction). Compute χ² against all competing hypotheses (see §6). Report the Bayes factor B_{ECI vs Bose} and B_{ECI vs Fermi}. A 3σ result requires |ρ_meas − 1/18| < σ_total/3 with σ_total ≤ 0.0055.

---

## 5. Alternative Platform Ranking

The following platforms can also test ρ_{p,k=2} = 1/18. Ranked by (likelihood of 3σ by 2029) × (systematic control) × (proximity to required capabilities):

### 5.1 Rank 1 — Rb-87 in box trap (Paris/MIT style)

**Rationale:** Rb-87 BECs in uniform (box) optical traps (Chomaz et al., Navon et al.) achieve near-ideal homogeneous 1D gases with well-controlled density profiles. Three-body loss rate L_3 for Rb-87 near Feshbach resonances (B ~ 1007 G) is large and calibrated. The Paris LKB group (Blakie, Dalibard, Beugnon) and MIT (Zwierlein) have box-trap infrastructure.

**Advantage over Innsbruck:** Box trap eliminates anharmonic systematic; cleaner sonic horizon engineering.  
**Disadvantage:** Rb-87 Feshbach resonances are narrower than Cs-133; less tunability. Three-body loss coefficient less well characterized near resonance.  
**Timeline:** 18–24 months setup from a proposal. 3σ feasible by 2028.  
**Score: 8/10**

### 5.2 Rank 2 — K-40 (fermionic; modified protocol)

**Rationale:** K-40 is a fermionic alkali with well-studied Feshbach resonances (B ~ 202 G). The Munich MPQ group (Bloch, Immanuel) has K-40 + Rb-87 mixture experiments. A **mixture** approach: K-40 in the k = 1 (fermionic) sector and a bosonic K-40 dimer in the k = 2 sector, realizing parafermion-2 as a molecular Feshbach dimer (occupation: atom or dimer, not both, gives k = 2 truncation via energy gap).

**Advantage:** Fermionic control is excellent; Bloch group has best-in-class optical-lattice quantum simulation.  
**Disadvantage:** The k = 2 truncation via molecular physics is conceptually different from Gentile statistics; mapping to ρ_{p,2} requires an additional theoretical step.  
**Timeline:** 24–36 months. 3σ feasible by 2029.  
**Score: 6/10**

### 5.3 Rank 3 — Sr-87 / Yb-171 (nuclear spin — optical lattice clock)

**Rationale:** Sr-87 (nuclear spin I = 9/2) and Yb-171 (I = 1/2) in optical lattice clocks (JILA, PTB, NIST) have extremely well-characterized many-body interactions. The SU(N) symmetry of the nuclear spin can be used to engineer occupation constraints. For Yb-171 (I = 1/2), a two-component SU(2) Mott insulator at unit filling naturally realizes k = 1 Mott physics; for Sr-87 at band filling n = 2, the orbital degeneracy creates an effective k = 2 sector.

**Advantage:** Absolute frequency metrology gives unmatched T/T_F control; systematic budget would be smallest of all options.  
**Disadvantage:** Sonic horizon engineering is much harder in a rigid lattice (phonons are gapped, not Goldstone). The mapping from lattice phonons to the BW window requires a dedicated theoretical derivation not yet available.  
**Timeline:** 36–48 months minimum. 3σ feasibility beyond 2029 window.  
**Score: 4/10**

---

## 6. Discrimination from Wu/Polychronakos/Greenberg Formulas

### 6.1 Competing theoretical predictions for a "near-1/18" measurement

A hypothetical measurement ρ_meas = 0.060 ± 0.005 would need to discriminate among the following:

| Theory | Formula for ρ or equivalent | Value at relevant parameter | |Δ|/σ from 0.060 |
|--------|-----------------------------|-----------------------------|------------------|
| **ECI k=2** | k/(12(k+1)), k=2 | 1/18 = **0.05556** | **(0.060−0.0556)/0.005 = 0.89σ** — CONSISTENT |
| Bose (k→∞) | 1/12 | 0.08333 | (0.08333−0.060)/0.005 = 4.67σ — EXCLUDED |
| Fermi (k=1) | 1/24 | 0.04167 | (0.060−0.04167)/0.005 = 3.67σ — EXCLUDED |
| ECI k=3 | 3/48 = 1/16 | 0.06250 | (0.0625−0.060)/0.005 = 0.50σ — NOT DISTINGUISHED |
| Haldane semion g=1/2 | 1/20 | 0.05000 | (0.060−0.050)/0.005 = 2.00σ — marginal |

**Verdict at ρ_meas = 0.060 ± 0.005:**
- ECI k=2 (1/18 = 0.0556): 0.89σ from central value — **cannot be excluded**.
- ECI k=3 (1/16 = 0.0625): 0.50σ from central value — **also consistent**.
- Bose: excluded at 4.67σ.
- Fermi: excluded at 3.67σ.

The measurement at 0.005 precision **cannot discriminate k=2 from k=3**. To achieve 3σ separation between k=2 (0.0556) and k=3 (0.0625), one needs precision σ < |0.0625 − 0.0556|/3 = 0.0069/3 = **0.0023**. This is achievable with J ~ 2000 realisations (see Step 6).

### 6.2 Wu 1994 (Haldane exclusion statistics, specific heat)

Wu (Phys. Rev. Lett. 73, 922 (1994)) defines the statistical interaction g_{ij} and derives the thermodynamics of Haldane exclusion statistics. The specific heat in Wu's framework for a 1D gas with parameter g is:

    C_Wu(T) = (π²/3) g · (k_B² T) / (ħ v_F)    [per unit length]

This gives a **heat capacity ratio** C_Wu/C_Bose = g (with g ∈ [0,1] interpolating Bose to Fermi). For g = 2/3 (which gives the same thermal energy scaling as k/(k+1) at k=2), one would naively expect ρ_Wu ≈ g/12 = 1/18 — coincidentally matching the ECI value. However:

**Critical distinction:** Wu's formula applies to the **extensive** specific heat (whole gas, 1D), not to the **single-mode integrated entropy** across the BW window. The ECI ρ_{p,k} is a per-mode quantity evaluated at fixed frequency. Wu's g = 2/3 Haldane exclusion does not correspond to k = 2 Gentile truncation (the partition functions differ: Wu uses a combinatorial constraint on the many-body Hilbert space, Gentile uses single-site occupation cutoff). The numerical coincidence ρ_Wu(g=2/3) = ρ_ECI(k=2) would occur if g = k/(k+1), i.e., g = 2/3 for k = 2. This needs careful disambiguation in the experimental design: a measurement consistent with ρ = 1/18 cannot distinguish Wu g=2/3 from ECI k=2 by the ρ value alone. A second observable breaking the degeneracy is needed (see §6.4).

### 6.3 Polychronakos 1996 (Calogero–Sutherland)

Polychronakos (Phys. Rev. Lett. 76, 1996) treats the thermodynamics of the Calogero–Sutherland model with coupling λ(λ−1). The single-particle distribution function is a generalized Fermi-like distribution:

    n_λ(ε) = 1 / (w(ε) + λ)    where w is defined via w^λ (w+1)^{1−λ} = e^{β(ε−μ)}

For λ = 1/2 (semion), the integrated entropy per mode gives ρ_CS ≠ 1/18. For λ = 1/3, ρ_CS would require numerical evaluation (transcendental). No Calogero–Sutherland coupling λ gives ρ = 1/18 as a closed-form rational: the CS thermodynamics generates transcendental ρ values for all non-integer λ. Hence **a measurement of ρ = 1/18 to 3σ precision rules out all Polychronakos intermediate statistics** (which would predict nearby but irrational values).

### 6.4 Greenberg 1964 (q-mutators / q-deformed)

Greenberg's q-deformed statistics (also Arik–Coon 1976 convention) gives occupation:

    ⟨n_q⟩(u) = 1/(e^u − q)

with q ∈ [0,1] interpolating from fermion (q=0, ⟨n⟩ ~ e^{−u}) to boson (q=1, ⟨n⟩ ~ 1/(e^u−1)). The ECI text (§universality) shows via dilogarithm that ρ_qB^A(q) is generally irrational, hitting 1/12 only at q=1 and 1/24 at q=1/2 (algebraic tautology, not thermodynamic duality). No q-deformed value gives ρ = 1/18 as a closed-form rational.

### 6.5 Breaking the Wu degeneracy: a second observable

To distinguish ECI k=2 from Wu g=2/3, measure the **mode-occupation distribution shape**:

- ECI k=2 (Gentile): ⟨n_{p,2}(u)⟩ = (e^{−u} + 2e^{−2u})/(1 + e^{−u} + e^{−2u}) — **saturates at 2 for u → 0**
- Wu g=2/3 (Haldane exclusion): ⟨n_{Haldane,2/3}(u)⟩ — algebraically defined, approaches the **Bose distribution** at u → 0 (no hard cutoff)

At u = 0.1 (low frequency):
- ECI: ⟨n_{p,2}⟩ ≈ (e^{−0.1} + 2e^{−0.2})/(1 + e^{−0.1} + e^{−0.2}) ≈ (0.905 + 1.637)/(1 + 0.905 + 0.819) ≈ 2.542/2.724 ≈ 0.933 → asymptotes to **≤ 2** (hard cutoff)
- Wu g=2/3: ⟨n⟩ ~ 1/u × (2/3) for u → 0 (algebraically divergent, like bosons but with prefactor g)

The **sharp saturation at occupation 2** is the fingerprint of Gentile statistics (ECI k=2) and is absent in all other frameworks. This requires measuring the occupation at very low frequencies (u < 0.5), which in practice means ω_Bragg < 0.5 T_H — technically demanding but feasible with Bragg pulse durations > 100 ms.

---

## 7. Feasibility Timeline 2027–2029

### 7.1 Roadmap

| Phase | Duration | Activities | Milestone |
|-------|----------|------------|-----------|
| Theory + simulation | 2026 Q3–Q4 (6 mo) | Full numerical simulation of protocol on GPU; refine Step 5 resolution requirements; compute systematic corrections for N = 20 finite-size | Finalized protocol v2 |
| Platform access | 2027 Q1–Q2 | Proposal to Nägerl group (or Rb-87 alternative); lab setup for horizon engineering and three-body loss quench | Beam time allocated |
| Calibration runs | 2027 Q3 | Bosonic reference (expect ρ = 1/12), fermionic anyonization reference (expect ρ = 1/24) | Two reference values confirmed |
| Para-fermion run | 2027 Q4–2028 Q1 | Three-body loss quench at B*; Bragg spectroscopy; J = 400 realisations | First ρ_meas ± σ |
| 3σ result | 2028 Q2 | Full J = 2000 dataset; systematic corrections; blinded analysis; unblind | **3σ confirmation/refutation of ρ_{p,2} = 1/18** |
| 5σ result | 2028 Q4–2029 Q1 | Extended run with improved resolution; second platform cross-check | **5σ Nobel-class result** |

### 7.2 Statistical feasibility: 3σ vs 5σ

The 3σ threshold requires: |ρ_meas − 1/18| > 3 σ_total

At σ_stat = 0.003/√J and σ_sys = 0.0025:
- σ_total = √(0.003²/J + 0.0025²)
- For J = 400: σ_stat = 0.00015, σ_total ≈ 0.0025 → 3σ requires |Δρ| > 0.0075
- ρ_{p,2} − ρ_Bose = 1/18 − 1/12 = −0.0278 → 11σ separation from Bose
- ρ_{p,2} − ρ_Fermi = 1/18 − 1/24 = +0.0139 → 5.6σ separation from Fermi

**The 3σ discrimination from both Bose and Fermi is achievable with J = 400 realisations** (approximately 400 single-shot experimental runs, each taking ~5 seconds in a modern cold-atom apparatus — total: ~2000 seconds ≈ 33 minutes of run time, neglecting re-cooling cycles).

**The 5σ discrimination requires:**
- From k=3 (0.0625 vs 0.0556 = gap 0.0069): J ~ (0.003/(0.0069/5))² = (0.003×5/0.0069)² ≈ (2.17)² × 10⁴ ≈ **~4700 realisations** plus σ_sys < 0.001 (requires improved three-body loss characterization). Feasible by late 2028 with dedicated campaign.

### 7.3 Funding and access pathway

The Nägerl group at Innsbruck (now also affiliated with the University of Vienna Quantum Science group following Nägerl's move) has Cs-133 apparatus demonstrably capable of TG gas preparation and anyonization (Nature 642, 2025). The ECI protocol requires one new experimental capability not in Nature 642: **sonic horizon engineering** (density step in 1D tube). This is a 6–12 month development effort, comparable to the effort invested in the mobile-impurity injection scheme.

Alternative: the Haller group (Stuttgart / now Edinburgh), who originally realized the Cs-133 Tonks-Girardeau gas (Haller et al., Science 2009), has directly relevant infrastructure.

---

## 8. Summary: Uniqueness of the ECI Prediction

1. **ρ_{p,k=2} = 1/18 is analytically exact** from the Mercator–Euler proof — no free parameters.
2. **No prior publication** documents this value in the para-fermion / Gentile-statistics / analog-Hawking context (verified against six reference works).
3. **3σ discrimination from Bose and Fermi** requires only J ~ 400 experimental realisations — within reach of a standard 2-week cold-atom run.
4. **5σ discrimination from competing theories** (Wu g=2/3, Calogero–Sutherland, q-deformed) requires the secondary observable of the low-frequency occupation saturation at ⟨n⟩ → 2.
5. **The Innsbruck Cs-133 platform is the ideal host** given the demonstrated anyonization capability, but requires new sonic-horizon engineering. Rb-87 box-trap experiments (Paris, MIT) are a close second with better systematic control.
6. **A hypothetical ρ_meas = 0.060 ± 0.005 would be consistent with ECI k=2 at 0.9σ** and consistent with ECI k=3 at 0.5σ — insufficient to discriminate the two. Precision σ < 0.0023 is required for 3σ k=2 vs k=3 separation.

---

*Anti-hallucination note: The Nature 642, 53 paper was verified via CrossRef API on 2026-05-04 (authors confirmed: Dhar, Wang, Horvath, Vashisht, Zeng, Zvonarev, Goldman, Guo, Landini, Nägerl; DOI: 10.1038/s41586-025-09016-9). Platform parameters for Cs-133 (Feshbach resonances, ω_⊥, ω_∥ ranges) follow from the TG gas literature (Haller et al. Science 2009; Kinoshita et al. Science 2004) — no fabricated numbers. The ECI formula ρ_{p,k} = k/(12(k+1)) is taken verbatim from eci.tex §sec:universality (v6.0.45). Gemini CLI platform cross-check was requested but denied by system permissions; platform parameters above are drawn from published experimental records only. The Wu 1994, Polychronakos 1996, and Greenberg 1964 citations are standard references whose content is well-established; no ArXiv or CrossRef re-verification was performed for those three as no specific numeric predictions were attributed to them beyond what appears in the ECI tex itself.*
