# M1-C Theorem-Attempt via Vardian (2602.02675) + Hollands (2503.21385)

**Date:** 2026-05-02
**Method:** Direct PDF read of both papers + arXiv API verification + cross-check against repo's `notes/m1_audit_2026_05_02.md` and `paper/frw_typeII_note/frw_note.tex`.
**Discipline:** Verbatim quotation only. No paraphrase passed off as theorem.

---

## (1) Triangulation: both papers exist

- **Vardian arXiv:2602.02675v1** — *"Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands"*, single author Niloofar Vardian (Sharif University, hep-th). Submitted 2 Feb 2026, 5 pages + supp + appendix. arXiv API confirms `<opensearch:totalResults>1</opensearch:totalResults>`.
- **Hollands arXiv:2503.21385v1** — *"Modular Time Evolution and the QNEC"*, single author Stefan Hollands (Leipzig + MPI MiS, hep-th/math-ph/math.OA). Submitted 27 Mar 2025, 18 pages, no figures. arXiv API confirms.

Note: the existing repo bib already has **Hollands-Longo 2025 = arXiv:2503.04651** (joint "A New Proof of the QNEC"). The target Hollands paper here, **2503.21385**, is the *single-author follow-up* posted 23 days later that derives the chaos-bound inequality from the QNEC machinery. They are distinct papers; the audit chain has not yet considered 2503.21385.

---

## (2) Verbatim Vardian "main theorem"

Vardian has no formal `\begin{theorem}` block — it is a 5-page PRL-style note. The closest thing to a main statement is the construction summary (equation 26, p.4):

> "Finally, we introduce our procedure to find the area operator directly from the boundary data as:
> O ∈ A → {a^O_n, b^O_n} → (L_S)_{mn} = [tridiagonal Lanczos matrix] → P_O K|_A P_O : spectrum of K|_A → Area Operator."  (eq. 26)

Together with the structural identity (eq. 27, p.4):

> "L_A = ⊕_α S(χ_α, M_A) P_α = K_A ⊗ I_{Ā} − K|_A"  (eq. 27)

The setting (eq. 33–35, supplemental) is operator-side modular Krylov complexity defined by

> "L_S O := [K_A ⊗ I_{Ā}, O], O(s) = e^{is L_S} O = e^{isK|_A} O e^{−isK|_A}"  (eqs. 33–34, 36)

with C_k defined via the Lanczos coefficients of this Liouvillian (eq. A9 for operator Krylov complexity, eq. A25 for state modular Krylov complexity).

**Algebra type Vardian works in.** OAQEC + AdS/CFT boundary CFT Hilbert space `H = H_A ⊗ H_Ā` (eq. 2). The CFT boundary algebra is implicitly **type-I tensor factor on a finite-dimensional code subspace** (the unitaries U_A, U_Ā in eq. 9 are between *finite-dimensional Hilbert spaces*). The non-trivial center comes from superselection over semi-classical saddles (eq. 14), not from a true type-II/III structure. The "modular Hamiltonian" K_A is well-defined because ρ_A is a density matrix, requiring tensor-product decomposition.

---

## (3) Verbatim Hollands main theorem

Hollands states a sharp theorem (Theorem 4.1, p.9), which I quote essentially verbatim:

> **Theorem 4.1.** Suppose that for some a ∈ ℝ, ∂S(a) exists, Φ ∈ D(P) ∩ D(log Δ_a), that u_s Φ ∈ D(P) for all s ∈ ℝ, and that cφ ≤ ω ≤ c^{−1} φ for some c > 0. Then the flowed state φ_s (eq. 34) satisfies
> **S_meas(φ_s ‖ φ_s ◦ T ◦ R)_{M(a,b)} ≤ (a − b) ∂S(a) · e^{2πs} + o((b−a) e^{2πs})**  (eq. 39)
> for a, b, s ∈ ℝ such that (b − a) e^{2πs} → 0+. Likewise, if ∂S̄(a) exists, … then
> **S_meas(φ'_s ‖ φ'_s ◦ T ◦ R)_{M(b,a)} ≤ (a − b) ∂S̄(a) · e^{−2πs} + o((a−b) e^{−2πs})**  (eq. 40)

The chaos-bound interpretation (p.10):

> "|ψ_s(δ_ε m)| ≤ 2ε ∂S̄(a) e^{2πs} + o(ε e^{2πs}) + ξ"  (eq. 48)
> "This expresses a chaos bound, i.e. the expectation value of δ_ε m in the evolved state ψ_s, grows exponentially at most at rate e^{2πs} … In this sense, we can say that the **Lyapunov exponent is ≤ 2π**."

**Algebra type Hollands works in.** Section 3, p.6: "(N ⊂ M, Ω) a half-sided modular inclusion" — these are **type III_1** local von Neumann algebras of a chiral CFT (or any half-sided modular inclusion). The type-II structure does **not** appear; in fact the proof relies on M(a, b) being a type III_1 factor and on the modular flow being ergodic in that case (eq. 43).

---

## (4) Explicit chain attempt for M1-C

M1-C target (from `notes/m1_audit_2026_05_02.md` line 13, with frw_note.tex Theorem 3.5 supplying the algebra):

> dS_gen[R] / dτ_R ≤ κ_R · C_k[ρ_R(τ_R)] · Θ
> in the type-II_∞ crossed product A_R = A(D_O)_FRW ⋊_σ ℝ.

The audit identifies **two independent decisive gaps** (Gap 1: transplant of complexity entropy to type-II_∞; Gap 2: source-identification lemma `|d⟨H_mod⟩/dτ| ≤ κ · C_k` in a type-II factor).

**Proposed Vardian + Hollands chain (Step A → B → C):**

- **Step A (Vardian).** On the FRW comoving diamond, conformal-pullback to Minkowski + reduce to a boundary-CFT-style modular Krylov C_k of an operator O in A(D_O)_FRW ≃ A(M_O)_Mink. Using Vardian eq. 26, extract spectrum of K|_A from C_k Lanczos data.
- **Step B (Hollands).** Apply Theorem 4.1 (eq. 39–40) to the half-sided modular inclusion derived from the Hislop–Longo modular structure of the conformally identified Minkowski diamond. This gives `|⟨ψ_s, δ_ε m ψ_s⟩| ≤ 2ε ∂S̄(a) e^{2πs}`, i.e. modular-Lyapunov ≤ 2π.
- **Step C (composition).** Combine: identify modular-Lyapunov bound with `|d⟨H_mod⟩/dτ_R|`-type bound and substitute into Faulkner–Speranza/Kirklin GSL to extract dS_gen/dτ_R ≤ κ_R · C_k.

---

## (5) Obstruction analysis (where the chain breaks)

**Obstruction O1 — Algebra-type mismatch (Vardian).** Vardian's K|_A reconstruction (eqs. 21, 23, 27) requires the OAQEC tensor decomposition `H = H_A ⊗ H_Ā`. This **only works in type-I** (where ρ_A = tr_Ā |ψ⟩⟨ψ| is a density matrix). On a type-III_1 local algebra (which is what A(D_O)_Mink is by Hislop–Longo and what Theorem 3.5 identifies the FRW algebra with), there is **no such tensor decomposition** and no density matrix; K_A is the *Tomita modular operator*, not −log ρ_A. Vardian implicitly works in a finite-dim code subspace of holographic CFT and never actually constructs C_k on a type-II_∞ algebra.

**Obstruction O2 — Half-sided inclusion ≠ FRW diamond inclusion (Hollands).** Hollands Theorem 4.1 requires a half-sided modular inclusion `(N ⊂ M, Ω)` with Wiesbrock's structure (Theorem 3.1, p.6). Concretely: M = A([0,∞)), N = A([1,∞)), with one-parameter translation U(a) generated by *positive* P (a *chiral* half-line structure). The FRW comoving causal diamond A(D_O)_FRW (Theorem 3.5 of `frw_note.tex`) gives a Hislop–Longo Möbius modular flow on a *bounded* diamond, **not** a half-sided modular inclusion of the chiral-CFT type. The Möbius group SO(2,1) on the diamond does not produce the required positive-spectrum translation generator P inside M. So the hypothesis of Theorem 4.1 *fails* on the FRW diamond as constructed.

**Obstruction O3 — Different objects (Lyapunov ≠ dS_gen/dτ).** Even granting O1 and O2 hypothetically, Hollands eq. 48 bounds `|ψ_s(δ_ε m)|` (the change of an observable expectation under modular flow). M1-C wants `dS_gen/dτ_R`, which is *entropy* growth, not observable growth. Hollands' bound is *of the form* of a chaos bound but is **not** a bound on `d⟨H_mod⟩/dτ` — the audit's Gap 2 specifically. The Hollands ant formula (eq. 32) ∂S(a) appears, but as the *coefficient* on the right-hand side (the QNEC slope of relative entropy), not as the LHS being bounded by C_k. There is no equation in 2503.21385 that has the form `|d⟨K⟩/dτ| ≤ κ · C_k`. Krylov complexity C_k does not appear anywhere in 2503.21385 (full-text confirmed: zero occurrences of "Krylov", "Lanczos", or "complexity").

**Obstruction O4 — κ_R is undetermined.** The "2π" in Hollands is the chaos-bound prefactor on the Lyapunov exponent (Maldacena–Shenker–Stanford analogue in modular time). Even if Steps A–C composed, the resulting prefactor would be 2π (or 2π·∂S̄(a)), not κ_R. There is no canonical map from "Lyapunov ≤ 2π" to "κ_R · C_k bound coefficient", because κ_R in v6 is a Brown–Susskind heuristic constant set by the gate-cost normalisation, while 2π is a kinematic Tomita prefactor. The two prefactors live in different conceptual layers.

---

## (6) Verdict

**M1-C theorem-grade status: FAILS.**

The Vardian + Hollands pairing does **not** upgrade M1-C from conjecture to theorem. Of the four obstructions, **O1 (algebra-type mismatch in Vardian) and O3 (Lyapunov ≠ entropy-derivative) are independent and decisive**; either alone breaks the chain. O2 and O4 are additional independent obstructions on the Hollands side and on the κ_R identification.

This pairing was identified by the prior crypto-Sonnet lit-check as the strongest single connection — and it is genuinely the strongest published connection to the M1-C territory in 2025–2026. But it does not close the gap: it merely re-localises the audit's Gap 1 (transplant) into Vardian and Gap 2 (modular-energy lemma) into Hollands. Both gaps survive intact.

The repo's existing position (`notes/m1_audit_2026_05_02.md`: "M1 must remain Conjecture M1-C") is correct and is *reinforced*, not weakened, by careful reading of the Vardian + Hollands pair.

---

## (7) Clean obstruction statement (for v8-bis)

The clean obstruction can be stated categorically (compatible with `notes/m1_c_categorical_2026_05_02.md`):

> **Obstruction (Vardian–Hollands non-composition).** Let A_R = A(D_O)_FRW ⋊_σ ℝ be the FRW type-II_∞ crossed-product (frw_note.tex Theorem 3.5). Then:
>
> (i) Vardian's modular Krylov C_k construction (arXiv:2602.02675, eq. 26) does not lift to A_R, because OAQEC requires a tensor factorisation H = H_A ⊗ H_Ā that does not exist for type-III_1 local algebras (and a fortiori not for their type-II_∞ crossed product), so K|_A as defined by Vardian has no analogue on A_R.
>
> (ii) Hollands's chaos-bound (arXiv:2503.21385, Theorem 4.1) does not apply to A_R, because the FRW diamond modular structure is Möbius (Hislop–Longo) on a bounded diamond, not a Wiesbrock half-sided modular inclusion of the chiral-CFT type required by Hollands Theorem 3.1.
>
> (iii) Even granting (i) and (ii) hypothetically, Hollands's bound is on observable expectation flow, not on dS_gen/dτ; the conversion would require an unpublished bridge between modular Lyapunov-on-observables and modular-energy-derivative-on-entropy in a type-II_∞ algebra. No such bridge exists in the literature as of 2026-05-02.

---

## (8) Recommendation

1. **Do not promote M1 to theorem in v8-bis.** Reaffirm Conjecture M1-C.
2. **Do** cite Vardian 2602.02675 as a *programmatic* reference for "boundary modular Krylov C_k could probe geometry in holographic settings" — but flag that the OAQEC type-I limitation prevents direct transplant to type-II_∞.
3. **Do** cite Hollands 2503.21385 as a *modular-time chaos-bound result on chiral CFTs* — but flag that the half-sided modular inclusion hypothesis is not satisfied by the FRW diamond modular structure.
4. **Do** add the Vardian + Hollands pair to the `notes/m1_audit` "candidate composition attempts that fail under careful hypothesis-checking" appendix, with the four obstructions O1–O4 explicitly enumerated. This protects v8-bis from future reviewers who notice the same pairing and ask why it wasn't tried.
5. **Open problem to state in v8-bis Section "Open problems":** "Is there a complexity-bounded modular GSL on a type-II_∞ crossed product (M1-C)? The Vardian + Hollands pairing reduces the problem to two specific bridges — extending OAQEC-style modular Krylov to type-II_∞ (open), and proving a Wiesbrock-like half-sided modular structure for FRW comoving diamonds (open) — and these reductions may guide a future construction."

---

## Appendix: arXiv API verification logs (saved to `/tmp/{vardian,hollands}_api.xml`)

- Vardian 2602.02675v1: title "Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands", author Niloofar Vardian, published 2026-02-02T19:00:24Z, primary hep-th, comment "5 pages + supplemental material + appendix". Confirmed.
- Hollands 2503.21385v1: title "Modular Time Evolution and the QNEC", author Stefan Hollands, published 2025-03-27T11:33:35Z, primary hep-th (also math-ph, math.OA, quant-ph), comment "18 pages, no figures". Confirmed.

Both PDFs downloaded (411 KB and 247 KB respectively) and read in full.
