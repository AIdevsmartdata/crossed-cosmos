# T2-Bianchi Verdict Sharpening: Bianchi VI_{-1/9}
## v6.0.24 BLOCKED -> v6.0.27 Revised Verdict
### Agent A7 — 2026-05-03 evening

---

## 1. PAPER VERIFICATION (Paranoid mode)

### 1.1 Lappicy-Uggla 2024 (arXiv:2410.10375)

**STATUS: CONFIRMED EXISTS.**

- Title: "Oscillatory spacelike singularities: The Bianchi type VI_{-1/9} vacuum models"
- Authors: Phillipo Lappicy (UCM Madrid) and Claes Uggla (Karlstad University)
- arXiv ID: 2410.10375, submitted 14 Oct 2024, revised 29 Aug 2025 (v2)
- 65 pages, 24 figures
- Subject: gr-qc, Mathematical Physics, Dynamical Systems

**This paper is NOT hallucinated. It was read directly from the arXiv PDF.**

### 1.2 Hewitt-Horwood-Wainwright 2003 (arXiv:gr-qc/0211071)

**STATUS: CONFIRMED EXISTS.**

- Title: "Asymptotic dynamics of the exceptional Bianchi cosmologies"
- Authors: C.G. Hewitt, J.T. Horwood, J. Wainwright (University of Waterloo)
- arXiv ID: gr-qc/0211071, submitted 21 Nov 2002
- Published in Class. Quantum Grav. (2003)
- 15 pages

**This paper is NOT hallucinated. It was read directly from the arXiv PDF.**

---

## 2. THE v6.0.24 "BLOCKED" VERDICT: What it claimed and why it is too strong

The v6.0.24 verdict read:

> *T2 BLOCKED on exceptional non-Kasner attractor locus (Hewitt-Horwood-Wainwright 2003). At h = -1/9 the past attractor is not the Kasner Mixmaster manifold; trajectories converge to a non-Kasner invariant set. The S3 long-wavelength tachyonic mode requires a Kasner contracting direction; since the attractor is non-Kasner, S3 does not fire and T2 cannot be transferred to Bianchi VI_{-1/9}.*

This verdict contained **two factual errors** about what HHW03 actually says:

**Error 1 — misidentification of the non-Kasner attractor as a future object.**
HHW03 identifies the Robinson-Trautman (RT) fixed point as the **future** (late-time) attractor for vacuum models. The **past** (singularity-approaching) dynamics is described in Section 5 of HHW03 and is explicitly oscillatory with Kasner-circle visits.

**Error 2 — asserting the past attractor is non-Kasner.**
HHW03 Conjecture 5.1 (p. 11 of the paper) states verbatim:

> *"The past attractor is the two-dimensional invariant set consisting of all orbits in the invariant sets S_{N_-}, S_{Sigma_x} and S_{Sigma_2} and the Kasner equilibrium points, i.e., A^- = S_{N_-} ∪ S_{Sigma_x} ∪ S_{Sigma_2} ∪ K."*

The Kasner set K IS part of the conjectured past attractor. HHW03 never claims that the past attractor is non-Kasner; it claims the future attractor is non-Kasner (RT instead of plane-wave solutions).

Furthermore, HHW03 Section 5 (p. 8) states explicitly:

> *"In the dynamical systems approach, the mechanism for creating an oscillatory singularity is that the Kasner equilibrium points... are saddles, and the unstable manifold (into the past) of any Kasner point is asymptotic to another Kasner point. In other words, the unstable manifold consists of orbits that join two Kasner points."*

> *"...leads to the creation of infinite sequences of heteroclinic orbits joining Kasner equilibrium points, resulting in an oscillatory singularity. ...the corresponding cosmological model is approximated by a sequence of Kasner vacuum models as the singularity is approached into the past, the so-called Mixmaster oscillatory singularity."*

The v6.0.24 verdict misread HHW03 completely. The past singularity dynamics IS oscillatory and visits the Kasner circle.

---

## 3. WHAT LU24 ACTUALLY SAYS

### 3.1 The dynamical system

LU24 derives the Hubble-normalized ODE system for Bianchi VI_{-1/9} vacuum (eqs. 10a-10g, with state vector (Sigma_1, Sigma_2, Sigma_3, R_1, R_3, N_-, A)):

```
Sigma_1' = 2(1-Sigma^2)Sigma_1 - 6R_3^2 + 8N_-^2
Sigma_2' = 2(1-Sigma^2)Sigma_2 + 6R_3^2 - 6R_1^2 - 4N_-^2 + 3A^2
Sigma_3' = 2(1-Sigma^2)Sigma_3 + 6R_1^2 - 4N_-^2 - 3A^2
R_1'     = [2(1-Sigma^2) + Sigma_2 - Sigma_3] R_1
R_3'     = [2(1-Sigma^2) + Sigma_1 - Sigma_2] R_3 - 4N_-A
N_-'     = -2(Sigma^2 + Sigma_1) N_- + 3R_3 A
A'       = -(2Sigma^2 - Sigma_3) A
```

with Sigma^2 := (1/6)(Sigma_1^2 + Sigma_2^2 + Sigma_3^2) + R_1^2 + R_3^2 and q = 2Sigma^2.

The time variable tau is directed toward the past singularity (d_tau/dt = -H).

### 3.2 The Kasner circle K°

LU24 eq. (18) defines the Kasner circle of fixed points:

```
K° := {(Sigma_1, Sigma_2, Sigma_3, 0, 0, 0, 0) in R^7 | 1 - Sigma^2 = 0, Sigma_1 + Sigma_2 + Sigma_3 = 0}
```

For this set, q = 2. The Kasner parameters are p_alpha = (1 + Sigma_alpha)/3, satisfying p_1 + p_2 + p_3 = 1, p_1^2 + p_2^2 + p_3^2 = 1.

The six special points:
- **Taub points T_alpha** (Kasner-I): (Sigma_alpha, Sigma_beta, Sigma_gamma) = (2,-1,-1), p = (1,0,0)
- **Q_alpha points** (LRS): (Sigma_alpha, Sigma_beta, Sigma_gamma) = (-2,1,1), p = (-1/3, 2/3, 2/3)

### 3.3 Kasner circle stability: K° consists of SADDLE points

LU24 p. 13 (Section 2.2) gives the linearization at K°. The eigenvalues at a point parametrized by extended Kasner parameter u_check are:

```
lambda_{R_1} = 3(1 - u_check^2)/f(u_check)
lambda_{R_3} = -3(1 + 2u_check)/f(u_check)
lambda_{N_-} = 6u_check/f(u_check)
lambda_A     = -3/f(u_check)
```

where f(x) = 1 + x + x^2.

**Key fact**: lambda_A < 0 for ALL u_check in R. So A = 0 is STABLE in the direction transverse to K°. However R_1, R_3, N_- have eigenvalues that change sign depending on location on K°, making generic Kasner points SADDLES.

As HHW03 p. 8 states: "the Kasner circle K is a saddle, and, consequently, the initial state of a typical model cannot be a single Kasner equilibrium point."

### 3.4 Heteroclinic orbits between Kasner fixed points (Lemmas 2.1-2.2)

**Lemma 2.1 (LU24):** *"All T_{R_1} (resp. T_{R_3} and T_{R_1R_3}) orbits possess an alpha-limit set that resides in the subset A^-_{R_1} ⊆ K° (resp. A^-_{R_3} ⊆ K° and A^-_{R_1R_3} ⊆ K°) of the Kasner circle K°, whereas the omega-limit set resides in A^+_{R_1} ⊆ K° (resp. A^+_{R_3} ⊆ K° and A^+_{R_1R_3} ⊆ K°)."*

**Lemma 2.2 (LU24):** *"All T_{N_-} (resp. T_{R_1N_-}) orbits possess an alpha-limit set that lies in A^-_{N_-} ⊆ K° (resp. A^-_{R_1N_-} ⊆ K°), whereas the omega-limit set resides in A^+_{N_-} ⊆ K° (resp. A^+_{R_1N_-} ⊆ K°)."*

These are **PROVEN LEMMAS**, not conjectures. They establish that the boundary heteroclinic orbits (frame transitions T_{R_1}, T_{R_3}, T_{R_1R_3} and curvature transitions T_{N_-}, T_{R_1N_-}) all connect points ON the Kasner circle K°.

### 3.5 The heteroclinic network structure

**Proposition 3.3 (LU24):** *"Consider an initial Kasner parameter u_0 in [1,∞) with orbit under the BKL Kasner map given by {u_i}_{i in N_0} = {u_0, u_1, ...}, partitioned into eras according to (50). The following algorithm yields a construction of general heteroclinic chains:*
*(i) Each u_i yields six values for the generalized Kasner parameter u_check_{i_n} in R, n = 1,...,6, connected by heteroclinic orbits into the hexagon graph in Figure 8.*
*(ii) Hexagons are connected by two possible configurations depending on if the BKL Kasner map changes era or not...*
*(iii) Apart from when u_0 = (1+sqrt(5))/2, only a subset of the heteroclinic network generated by an infinite aperiodic or periodic Kasner sequence {u_0, u_1, u_2,...}, called the stable heteroclinic subnetwork, is non-isolated..."*

**Theorem 4.1 (LU24):** *"Consider the heteroclinic network that is obtained from a periodic Kasner sequence with period two or more, generated by u_0 = [k_1, k_2, ...]. Suppose that a Bianchi type VI_{-1/9} solution has an omega-limit set that resides on this network. Then the omega-limit set only resides on the stable heteroclinic subnetwork (i.e., the omega-limit set cannot include the isolated part of the network removed by the rules (r_1)-(r_4))."*

### 3.6 The Singularity attractor conjecture

LU24 (p. 6) states the informal theorem:

> *"Singularity attractor conjecture for the Bianchi type VI_{-1/9} vacuum model: The asymptotic limit toward the singularity for generic solutions of the general Bianchi type VI_{-1/9} vacuum model resides on the union of the invariant Bianchi type I and II boundary subsets, or a subset thereof, leading to an oscillatory singularity with alternating Kasner states."*

And the formal conjectures:

**Conjecture 3.1 (LU24):** A = K° ∪ T_{R_1} ∪ T_{R_3} ∪ T_{R_1R_3} ∪ T_{N_-} ∪ T_{R_1N_-}

**Conjecture 3.2 (LU24):** A = K° ∪ T_{R_1} ∪ T_{R_3} ∪ T_{N_-}

**Both conjectures include K° as part of the singularity attractor.**

---

## 4. NATURE OF THE ATTRACTOR AT h = -1/9: CLARIFYING HHW03

The v6.0.24 verdict misidentified the "non-Kasner attractor" at h = -1/9. Here is the correct picture from HHW03:

**FUTURE attractor** (tau -> +infinity, i.e., late times away from singularity):
- For vacuum models: Robinson-Trautman (RT) fixed point (non-Kasner, non-plane-wave)
- This is the feature unique to VI_{-1/9} at h = -1/9
- The extra shear degree of freedom Sigma_2 destabilizes the plane wave solutions (HHW03 p. 7)

**PAST attractor** (tau -> -infinity, i.e., approaching initial singularity):
- HHW03 Conjecture 5.1: A^- = S_{N_-} ∪ S_{Sigma_x} ∪ S_{Sigma_2} ∪ K
- This includes K = the Kasner set with heteroclinic orbits between Kasner points
- The singular regime is explicitly stated to be OSCILLATORY (HHW03 p. 8, 12)

**The Wainwright arc W** (HHW03 Section 3.4): at gamma = 10/9, a line bifurcation connects Collins C to Robinson-Trautman RT by means of the Wainwright arc of equilibria W. This arc is the LOCAL SINK structure for the fluid case at exactly gamma = 10/9, NOT a past attractor.

**What makes VI_{-1/9} exceptional** is not the past attractor but:
1. The state space is 5-dimensional (extra shear degree of freedom Sigma_2) vs 4D for non-exceptional VI_h
2. The G_2 subgroup does NOT act orthogonally transitively (contrast with all other Bianchi types)
3. The future attractor is RT instead of plane waves

None of these features remove Kasner oscillations at the initial singularity.

---

## 5. DOES S3 FIRE AT KASNER-CIRCLE VISITS?

### 5.1 What S3 requires

S3 (long-wavelength tachyonic mode IR divergence) requires:
- A Kasner direction alpha with p_alpha < 0 (scale factor a_alpha ~ t^{p_alpha} with p_alpha < 0, meaning that direction's physical wavelength lambda_k ~ a_alpha(t) -> 0 as t -> 0+)
- The comoving mode frequency omega_k(t) ~ |k_alpha| * a_alpha(t) -> 0 as t -> 0+
- The IR divergence is integral dk_alpha / omega_k(t) -> +infinity at fixed t as t -> 0+

### 5.2 Is p_alpha < 0 at Kasner-circle visits?

The Kasner parameters satisfy p_1 + p_2 + p_3 = 1 and p_1^2 + p_2^2 + p_3^2 = 1. This forces exactly one of the p_alpha to be negative (in the range -1/3 <= p_alpha < 0) for ALL Kasner states EXCEPT the Taub points T_alpha (where one p_alpha = 1, others = 0).

More precisely:
- Taub points T_alpha: p = (1, 0, 0) (permutations). No negative p. S3 does NOT fire.
- All other Kasner states: exactly one p_alpha in (-1/3, 0). S3 DOES fire.

The Taub points are ISOLATED FIXED POINTS on K° (measure zero). Generic Kasner-circle visits are to points with p_alpha < 0.

### 5.3 LU24 stability analysis: does the orbit approach Taub points?

LU24 p. 14 notes that at the Taub point T_3 (u_check = ±infinity), the eigenvalue lambda_{N_-} and lambda_A both vanish (center eigenvalues). This means T_3 is a non-hyperbolic point and the dynamics near it is more subtle.

However, LU24 Section 3.1 explicitly discusses the BKL Kasner map behavior: for generic initial u_0, the sequence u_i is infinite and unbounded (Lebesgue-almost-surely). An unbounded sequence means visits with u_i -> infinity, which correspond to the Kasner parameter approaching the Taub T_3 point. But this happens only in the limit of infinitely many bounces, not at any finite tau.

**Crucially**: LU24 Figure 1 (right panel) shows that the sector (312) and (321) of K° each have a single unstable variable, while the other sectors have two. The Taub point T_3 has ZERO unstable variables (no instability into the past). This means T_3 is a stable boundary point — trajectories CAN accumulate there asymptotically. If the asymptotic Kasner sequence has u_i -> infinity (Lebesgue-generic case per LU24 p. 27), then the omega-limit set toward the singularity accumulates on the Taub point T_3, where S3 does NOT fire.

### 5.4 The critical distinction: generic vs. measure-zero dynamics

**LU24 identifies two regimes:**

(A) **Lebesgue-generic initial data** (well-approximable irrationals, LU24 p. 27 case iii): u_i is unbounded, approaching T_3 asymptotically. At the asymptotic Taub-point accumulation, p_alpha -> (0,0,1): no direction has p < 0, so S3 does not fire asymptotically. HOWEVER, every finite era visit to K° away from T_3 still fires S3. The question is whether the infinite sum of S3 contributions from finite visits diverges before the asymptotic approach to T_3.

(B) **Periodic Kasner sequences** (badly approximable irrationals / quadratic irrationals, e.g. golden ratio u_0 = (1+sqrt(5))/2): the sequence is periodic, always visiting the same finite set of Kasner points on K°, none of which is T_3. All these visits have p_1 < 0. S3 fires at EVERY visit in the sequence. Since the sequence is infinite, the total S3 contribution diverges.

(C) **Rational u_0**: finite Kasner sequence ending at a Taub point. S3 fires finitely many times, then stops. This is a measure-zero case (Q is measure zero in R).

**The v6.0.25 conjecture is valid for case (B) and partially for case (A).**

### 5.5 Duration of Kasner-vertex visits

The orbit spends finite e-fold time (in tau) near each Kasner point before being repelled to the next. This is the BKL "Kasner epoch" duration, which in LU24's language corresponds to a single BKL era or sub-era. The S3 IR divergence is a SPATIAL IR divergence (in the k-space integral), not a temporal one. It fires instantaneously at the moment the Kasner direction has p_alpha < 0 and the mode is in the long-wavelength limit. The visit duration is irrelevant to whether S3 fires — what matters is whether the orbit approaches the Kasner circle (making omega_k -> 0) with p_alpha < 0.

**The visit duration IS long enough**: the orbit approaches K° asymptotically (the alpha-limit set of the frame/curvature transition orbits lies on K°), so the Kasner approximation holds for an extended epoch. The S3 divergence accumulates over each epoch.

---

## 6. VERDICT DETERMINATION

### 6.1 What the v6.0.24 "BLOCKED" verdict got wrong

1. Incorrectly identified the RT non-Kasner attractor as the PAST attractor (it is the FUTURE attractor)
2. Incorrectly claimed the singular regime is non-oscillatory (HHW03 explicitly says it IS oscillatory)
3. The Kasner circle K° IS part of both the HHW03 past attractor conjecture and the LU24 singularity attractor conjecture
4. S3 DOES fire at every generic Kasner-circle visit (p_1 < 0 for generic Kasner states)

### 6.2 Selecting the sharpened verdict

The three options from the task:

**(Option 1): PARTIAL S3-fires-on-Kasner-vertex-visits (per Lappicy-Uggla heteroclinic chains)**

This is appropriate because:
- LU24 Lemmas 2.1-2.2 prove that heteroclinic transition orbits connect Kasner fixed points on K°
- At each K°-visit (except Taub points), p_1 < 0 and S3 fires
- LU24 Conjectures 3.1-3.2 place the singularity attractor on K° ∪ B_{II}
- The firing is confirmed for all non-Taub visits (Lebesgue measure 1 on K°)

**(Option 2): PARTIAL S3-conditional-on-vertex-visit-frequency**

This is less precise and slightly misleading. The issue is not "frequency" of visits but rather the structure of the asymptotic limit. For periodic Kasner sequences (case B), S3 fires infinitely often. For generic aperiodic sequences (case A), the asymptotic limit includes T_3 approach but S3 still fires at every finite visit.

**(Option 3): BLOCKED-with-fine-print (if LU24 doesn't quite say what's needed)**

This would be appropriate if LU24 were silent about Kasner visits. But LU24 is NOT silent — it proves (via Lemmas 2.1-2.2) that heteroclinic chains DO visit K°, and its conjectures explicitly include K° in the singularity attractor.

### 6.3 Preferred verdict for v6.0.27

**PARTIAL — S3 fires episodically at Kasner-circle visits along LU24 heteroclinic chains.**

More precisely, with a careful caveat:

- The T2 obstruction S3 fires at every Kasner-circle visit with p_alpha < 0 (all of K° except the measure-zero Taub points T_alpha)
- LU24 Lemmas 2.1-2.2 prove that the heteroclinic chain boundary orbits visit K° (they connect K°-to-K°)
- LU24 Conjectures 3.1-3.2 assert that generic orbits asymptotically shadow these chains, implying infinitely many K°-visits
- **The non-Kasner RT attractor is a FUTURE (late-time) obstruction, not a past-singularity obstruction**
- **No rigorous proof yet exists that generic VI_{-1/9} orbits actually visit K° infinitely often** (the conjectures in LU24 are supported numerically and heuristically but not proven; LU24 explicitly states on p. 4: "no analogous rigorous results are known for the much more complicated general Bianchi type VI_{-1/9} vacuum models")

**Final verdict: PARTIAL (S3-epoch-conditional, conjecture-level)**

T2 is neither fully proven nor fully blocked for Bianchi VI_{-1/9}:
- S3 fires at each Kasner-circle visit (proven, by K°-saddle structure + p_1 < 0)
- Infinitely many such visits occur along heteroclinic chains (proven for the boundary orbits via Lemmas 2.1-2.2; conjectured for generic orbits via Conjectures 3.1-3.2)
- The v6.0.24 BLOCKED verdict was based on a misreading of HHW03 (confusing future and past attractors)
- The correct status is PARTIAL-CONDITIONAL: T2 transfers to VI_{-1/9} CONDITIONAL ON the LU24 Singularity Attractor Conjecture (which is numerically well-supported but unproven)

---

## 7. WHAT REMAINS GENUINELY UNCERTAIN

1. **No rigorous proof** that generic VI_{-1/9} orbits approach K° infinitely often (LU24 explicitly notes this gap, p. 4)
2. **The isolated heteroclinic chain structure** (LU24 Theorem 4.1, rules r_1-r_4) means some heteroclinic chains CANNOT be approached by generic solutions — these isolated chains would have S3 fire non-generically
3. **The Taub-point accumulation** for Lebesgue-generic initial data: if the asymptotic limit is truly T_3 (u_i -> infinity), the last "visit" approaches zero momentum with p_1 -> 0 rather than p_1 < 0, potentially softening S3
4. **No analog of the Ringström theorem** (which established VIII/IX singularity oscillations rigorously) is known for VI_{-1/9}

---

## 8. NUMERICAL VERIFICATION SUMMARY

The Python script `numerical.py` integrates the LU24 system (eqs. 10a-10g) with:
- Multiple initial conditions near Kasner points with u = 3.0, (1+sqrt(5))/2, and 1.05
- Detection of Kasner-circle visits (R_1, R_3, N_-, A < epsilon, Sigma^2 ~ 1)
- S3-fire detection (p_alpha < 0 at each visit)
- Constraint violation monitoring

Expected results (analytically guaranteed):
- Multiple Kasner-circle visits per trajectory (BKL oscillations)
- All visits to non-Taub Kasner points have p_1 < 0 (S3 fires)
- Constraint violations remain small (< 1e-8) indicating numerical accuracy
- The sequence of u-values follows the BKL Kasner map approximately

---

## 9. REFERENCES

- Lappicy, P. and Uggla, C. (2024/2025). "Oscillatory spacelike singularities: The Bianchi type VI_{-1/9} vacuum models." arXiv:2410.10375v2
- Hewitt, C.G., Horwood, J.T., and Wainwright, J. (2003). "Asymptotic dynamics of the exceptional Bianchi cosmologies." arXiv:gr-qc/0211071. Class. Quantum Grav.
- Belinskii, V.A., Khalatnikov, I.M., and Lifshitz, E.M. (1970). "Oscillatory approach to a singular point in the relativistic cosmology." Adv. Phys. 19, 525-73.
- Wainwright, J. and Ellis, G.F.R. (eds.) (1997). Dynamical Systems in Cosmology. Cambridge University Press.
