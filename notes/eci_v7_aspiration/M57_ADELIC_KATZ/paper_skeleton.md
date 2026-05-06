---
name: M57 paper skeleton — Adelic Katz short note (ANT 10-12pp)
description: ANT short-note skeleton for adelic Katz / M13.1 paper. Companion to M32 paper-2.
type: project
---

# Paper skeleton: Adelic Katz formulation of Conjecture M13.1

**Provisional title**: "An adelic Katz conjecture for the CM newform 4.5.b.a: Tate-thesis interpolation and Pollack-type rescue at p=2"

**Target**: *Algebra & Number Theory* (primary); fallback *Research in NT*, *Compositio*

**Length**: 10-12pp short note / research announcement

**Companion to**: M32 paper-2 (22pp full proof-strategy); M39 Beilinson note (14pp)

**Status**: CONJECTURE paper — must be framed as precise open problem + computational evidence

---

## §1 Introduction (1.5pp)

CM newform f = 4.5.b.a (LMFDB) at weight k=5, level N=4, CM by K=Q(i) — exhibits Frobenius zero-root degeneracy at p=2 obstructing all standard p-adic L-function constructions (Katz 1978, Pollack 2003, LLZ 2010, BBL 2023). Obstruction is "Steinberg-edge" a_2 = -4 = -2^((k-1)/2), arising because p=2 ramifies in K and N = p².

We state Conjecture M13.1 in adelic Tate-thesis language: ∃ L_2^±(f) ∈ D(Γ, Z_2) interpolating Damerell critical values α_m^ren with Pollack-type renormalisation. UNCONDITIONAL: strict monotone v_2 = (-3,-2,0,+1). OPEN: existence requires Kriz 2021 + Fan-Wan 2023 framework extension to ramified principal series at p=2.

Honest scoping: precise conjecture + computational evidence, NOT a proof.

## §2 Adelic setup (1.5pp)

- K = Q(i), O_K = Z[i], d_K = -4, (2) = (1+i)²
- Adele ring A_K = ∏'_v K_v
- Hecke Grössencharacter ψ: A_K^×/K^× → C^× of ∞-type (4,0), conductor (1+i)²
- Theta-lift f = θ(ψ) ∈ S_5(Γ_0(4), χ_-4) — the LMFDB form 4.5.b.a
- Anticycl Iwasawa algebra Λ(Γ) = Z_2[[Γ]], Γ ≅ Z_2

## §3 Theta-lift + LMFDB identification (1pp)

LMFDB 4.5.b.a verified: a_2 = -4, q-expansion q - 4q² + 16q⁴ - 14q⁵ - 64q⁸ + …, eta quotient η(z)⁴η(2z)²η(4z)⁴, Sato-Tate U(1)[D_2].

Local L-factor at p=2: L_2(f, X) = 1/(1 + 4X) since χ_-4(2) = 0. Frobenius char poly X² + 4X (one zero root, no unit root) = Steinberg-edge obstruction.

## §4 Conjecture M13.1 statement (adelic) (2pp)

§4.1 Damerell critical values: α_m = (1/10, 1/12, 1/24, 1/60). Pair-sums α_2 + α_3 = 1/8 (v_2 = -3); α_1 + α_4 = 7/60 (v_2 = -2).

§4.2 **Conjecture M13.1.A** (Existence): formal statement (see SUMMARY).

§4.3 **Conjecture M13.1.B** (Boundedness): Pollack-type rescue ω(γ) = log_2(γ)/(γ-1).

§4.4 The Kriz-Fan-Wan framework. Two open steps: [TBD-A1] Kriz extends to p|N; [TBD-A2] Fan-Wan PS condition at p=2.

## §5 Functional equation + Atkin-Lehner (1pp)

§5.1 Classical: Λ(f, s) = ε(f) · (4/π²)^... · L(f, 5-s) with ε(f) = +1.

§5.2 Adelic Tate-thesis: Λ(π_f, s) = ε(1/2, π_f) · Λ(π_f^v, 1-s).

§5.3 Consequences for ± distributions: L_2^+ and L_2^- complex-conjugate.

## §6 Computational evidence (1.5pp)

§6.1 **THEOREM M13.1.C(i)** (UNCONDITIONAL, sympy-verified, M22):
F1 renormalisation α_m^ren = α_m × (-2)^(m-1) × (1 + 2^(m-3)) gives:
(α_1^ren, ..., α_4^ren) = (1/8, -1/4, 1/3, -2/5)
v_2 monotone: (-3, -2, 0, +1)

§6.2 N=p² structural (M21 verified): pair-sum rationality requires N square.

§6.3 M27.1 regulator (M39, conditional [TBD-M39-1]): KLZ Eisenstein classes give motivic corroboration if regulator pairings 2-adic-match v_2 ladder.

§6.4 F4 KLZ test plan (1000 CPU-hr; cluster needed): explicit Eisenstein symbols at level 4, p=2.

## §7 Open problems (1pp)

§7.1 [TBD-A1]: Kriz framework extends to p|N (Steinberg-edge). Hodge-filtration well-defined for ramified principal series? Ω_2 ∈ Q_2^× non-zero?

§7.2 IMC at p=2 (long-term). All published anticycl IMC results (Hsieh, Chida-Hsieh, Arnold, P-W) exclude p ramified or p|N. M13.1 (L-function) is necessary first step.

§7.3 Buyukboduk-Neamti 2026 connection: BDP formula via Heegner; potential alternative route to L_2^±(f) if applicable to p=2 ramified.

## §8 Bibliography (15 entries)

1. Tate 1967 Cassels-Frohlich
2. Katz 1978 Invent. Math. 49, 199-297 [VERIFY-NEEDED]
3. Damerell 1970 Acta Arith. 17, 287-301
4. Pollack 2003 Duke 118, 523-558 [VERIFY-NEEDED]
5. Shimura 1971 Princeton (CM theory)
6. LLZ 2010 Asian J. Math. 14 / arXiv:0912.1263 ✓
7. KLZ 2017 Camb. J. Math. 5, 1-122 / arXiv:1503.02888 ✓
8. Kriz 2021 Princeton AMS-212 [VERIFY-NEEDED]
9. Fan-Wan 2023 arXiv:2304.09806 ✓
10. BBL arXiv:2310.06813 ANT to appear ✓
11. Buyukboduk-Neamti 2026 arXiv:2604.13854 ✓
12. Hsieh 2014 Doc. Math. 19, 709-767
13. Chida-Hsieh 2018 J. Reine Angew. Math. 741, 87-131
14. LMFDB 4.5.b.a ✓
15. Silverman 1994 GTM 151 (CM theory)

## Collaborator priority
1. **Kriz (MIT)** — PRIMARY, Hodge-filtration [TBD-A1]
2. Fan/Wan — [TBD-A2]
3. Lei (Ottawa) — LLZ framework
4. Castella (UCSB) — anticycl Selmer
5. Buyukboduk (UC Dublin) — θ-critical + BDP

Outreach: Q3 2026 post-arXiv submission of P-NT companion.

## Discipline
- M13.1.C(i) clearly UNCONDITIONAL THEOREM
- M13.1.A, B, C(ii), C-full clearly OPEN CONJECTURES
- 6 refs live-verified, 4 VERIFY-NEEDED flagged
- Mistral STRICT-BAN observed
- Hallu 86 → 86
