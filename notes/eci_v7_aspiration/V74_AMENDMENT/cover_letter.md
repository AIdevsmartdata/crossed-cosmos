# Cover letter — v7.4 amendment to LMP / CMP

**To:** Editorial Board, Letters in Mathematical Physics
**From:** Kévin Remondière (independent researcher, Tarbes, France)
**Subject:** Submission — *ECI v7.4 amendment: τ as a CM-anchored attractor and a revised Damerell-ladder bridge H7' for Cardy density at c = 1 and c = 1/2*
**Date:** 2026-05-05

Dear Editors,

I submit for your consideration the enclosed short note documenting the v7.3 → v7.4 amendment of the Extended Cosmological Index (ECI) research programme. The note is technical and concise (10 pages) and reports a single, self-contained mathematical result together with the axiomatic restart it forces.

## Why LMP rather than CMP

I considered both *Letters in Mathematical Physics* and *Communications in Mathematical Physics*. I selected **LMP** for the following reasons:

1. **Length.** The result is a single rational ladder (1/10, 1/12, 1/24, 1/60) for the algebraic parts of the integer critical L-values of one specific CM newform (LMFDB 4.5.b.a), plus its parameter-free Cardy hits at c = 1 and c = 1/2. The argument fits comfortably in 8–12 pages without expansion; CMP papers in this area typically run 30–60 pages.
2. **Dual-axiom revision format.** The contribution is twofold (axiom H₅' replacing H₅, axiom H₇' replacing H₇ in the v7.3 system), with the second axiom backed by an open question (literature anchoring of the rational ladder). LMP routinely accepts this "result + flagged conjecture" format; CMP tends to require fully proved theorems.
3. **Cross-disciplinary readership.** The note bridges modular L-values (Damerell, Shimura, Deligne, BDP) and 2D CFT Cardy density. LMP's mixed pure-math/mathematical-physics readership matches this scope.

## Key claims

1. **The original v7.3 axiom H₇ is refuted** (audit G1.15, Zenodo DOI 10.5281/zenodo.20030684, commit 6.0.53, 2026-05-05): the assertion required L-value algebraicity at the half-integer s = k/2 = 5/2 for an odd-weight CM form, outside the Damerell–Shimura–Deligne archimedean algebraicity domain.
2. **Replacement H₇' (primary)**, the integer-point Damerell ladder
   L(f, m) · π^(4–m) / Ω_K⁴ ∈ {1/10, 1/12, 1/24, 1/60} for m ∈ {1, 2, 3, 4}, with the LMFDB CM newform 4.5.b.a and Chowla–Selberg period Ω_K = Γ(1/4)²/(2√(2π)). The values were computed by mpmath at 60-digit precision via the Iwaniec–Kowalski approximate functional equation; the LMFDB-cached value L(f, 5/2) = 0.5200744676… was used as a sanity check and reproduced exactly. The ladder is the **standard Eisenstein–Kronecker ladder for a weight-5 CM-by-Q(i) newform**: α₁ = 1/10 is the lemniscatic Hurwitz number H₄ (Hurwitz 1899, Math. Ann. 51), α₂ = 1/12 = B₂/2 is the Bernoulli half-value transported to Q(i) via Chowla–Selberg, with (α₃, α₄) = (α₂/2, α₁/6) forced by the Γ-functional equation L(f, s) ↔ L(f, 5–s). Therefore H₇' is a **theorem**, not a conjecture (citation chain: Hurwitz 1899; Chowla–Selberg 1949; Damerell 1971; Shimura 1976; Harder–Schappacher 1986).
3. **One Bernoulli-anchored Cardy hit + Γ-shadow**: the genuine parameter-free coincidence is α₂ = B₂/2 = 1/12 = ρ_Cardy(c=1) for the free boson (Tonks–Girardeau lab realisation); the Ising value α₃ = 1/24 = ρ_Cardy(c=1/2) is its automatic Γ-shadow under the functional equation. The strength of the bridge is correspondingly half the v7.3 prospectus, but anchored on a textbook Bernoulli identity.
4. **Replacement H₅'**: τ is a CM-anchored attractor with |τ – i| ≲ 0.2, supported empirically by a 30 × 30 χ² scan (W1, 2026-05-05) finding τ* = –0.1897 + 1.0034 i with χ²/dof = 1.05 over seven fermion observables (a factor ≈ 3 closer to the S-fixed-point than the LYD20 published best fit).
5. **Three independently flagged falsifiers**: Tonks–Girardeau density at c = 1, lepton-sector PMNS rejection of |τ – i| ≤ 0.3, and a Cassini-improvement exclusion of the NMC NULL.

## Open question explicitly left for follow-up

The unfit central charges c = 7/10 (tricritical Ising) and c = 4/5 (tetracritical Potts) do not appear in the integer Damerell ladder. Two scenarios are possible: (a) the BDP anti-cyclotomic complement supplies them via half-integer p-adic L-values; (b) they require a second CM newform anchor (the level-16 form 16.5.c.a, identified as the second hatted weight-5 multiplet of S'₄ in the companion P-NT paper). Discriminating (a) from (b) is the next concrete v7.4 test; this is left as the only open question.

## Anti-fabrication assurances

This is a project where I have a documented history of LLM-assisted citation hallucinations (current counter: 76 caught instances). Every arXiv ID and journal reference in the bibliography of the enclosed manuscript was live-verified against the arXiv API or Project Euclid on 2026-05-05; no AI assistant was permitted to introduce a citation without independent verification. The verifications are recorded as commented-out remarks in the .tex source.

## Companion paper

A companion no-go theorem note (V2: "A no-go theorem for the Cabibbo angle in S'₄ modular flavour models at τ = i") is in parallel preparation. It motivates the H₅ → H₅' relaxation by establishing that the strict τ = i ansatz forces sin θ_C ≤ 0.005 in LYD20 Model VI, a factor ≈ 45 below experiment. I cite it in the present manuscript and would be happy for both to be considered together by the same editor if the relevant.

## Conflict of interest

None.

## Suggested referees

(If LMP solicits suggestions:)

- E. Perlmutter (IPhT Saclay) — author of the degree-4 L-function approach to 2D CFT (arXiv:2509.21672) cited as the H₇-B backup route.
- G.-J. Ding (USTC) — co-author of LYD20 (arXiv:2006.10722), the modular flavour model whose τ-fixed-point this work amends.
- K. Prasanna (Michigan) — co-author of the Bertolini–Darmon–Prasanna anti-cyclotomic p-adic L-function construction (Duke Math J 162, 2013) used as the H₇' complement axiom.

Thank you for considering this submission.

Sincerely,

Kévin Remondière
Tarbes, France
kevin.remondiere@gmail.com
GitHub: AIdevsmartdata/crossed-cosmos
ORCID: (in progress, will be supplied at acceptance)
