# T2 Bianchi IX — Mixmaster residual closure (Opus 4.7, max-effort)

**Date**: 2026-05-02
**Companion to**: `/tmp/T2_bianchi_extension.{md,tex,py}` (T2 for Bianchi I,
which left Bianchi IX as residual conjecture).
**Sympy script**: `/tmp/T2_bianchi_IX.py` (all checks pass).
**Full writeup**: `/tmp/T2_bianchi_IX.tex`.

---

## 1. Heinzle–Uggla invariant-measure setup

**BKL Kasner u-map.** Vacuum Bianchi IX near the past singularity follows the
Lifshitz–Khalatnikov sequence of Kasner epochs parametrised by
\(u\in[1,\infty)\):
\[
p_1(u)=-\frac{u}{1+u+u^2},\quad
p_2(u)=\frac{1+u}{1+u+u^2},\quad
p_3(u)=\frac{u(1+u)}{1+u+u^2}.
\]
Sympy verifies \(\sum p_i=1=\sum p_i^2\) for all \(u\). One direction is
always contracting (\(p_1\in(-1/3,0)\)); two are expanding.

**Mixmaster map.** Era step \(u\to u-1\); transition \(u\to 1/u\). Iterating
the fractional part of \(1/u\) is the Gauss map \(T(x)=\{1/x\}\) on
\((0,1)\).

**Invariant measure** (Heinzle–Uggla 2009, arXiv:0901.0776, after lifting
the classical Gauss–Kuzmin density). On the Kasner u-line:
\[
d\mu_{\rm HU}(u)=\frac{1}{\ln 2}\,\frac{du}{u(u+1)},\qquad u\in[1,\infty).
\]
Sympy verifies normalisation \(\int_1^\infty d\mu_{\rm HU}=1\) and
Perron–Frobenius invariance under the Gauss map (telescoping series). The
empirical Lyapunov exponent matches \(\pi^2/(6\ln 2)\) (Khinchin–Lévy) to
<1% on \(2\!\times\!10^5\) Gauss-iterations.

> **Reference correction (audited).** The parent agent cited
> "Heinzle–Uggla arXiv:0901.2891" — that ID is a **chemistry paper** on
> water in nanopores. The actual Heinzle–Uggla 2009 papers are
> **arXiv:0901.0776** ("Mixmaster: Fact and Belief") and
> **arXiv:0901.0806** ("A new proof of the Bianchi type IX attractor
> theorem"). Both verified via arXiv API this session. DHN
> hep-th/0212256 and Hartnoll–Yang 2502.02661 verified.

---

## 2. T2 µ-pathwise verification — succeeds STRONGER than µ-a.e.

**Key technical fact** (Heinzle–Uggla 2009 attractor theorem / Wainwright–
Ellis 1997 / Ringström 2001 PhD): along **every** vacuum Bianchi IX
trajectory whose past attractor is the Mixmaster Kasner-circle locus,
there exist constants \(0<c_1<c_2\) such that for \(t\) small,
\[
c_1\,t \le V(t)=a_1 a_2 a_3 \le c_2\,t.
\]
This is a **pathwise** bound, not a µ-a.e. one — it follows from the
attractor structure plus the bounded-from-above Mixmaster wall potential,
without invoking the invariant measure.

**Theorem T2-Bianchi IX (volume-divergence form, conditional).** Let
\((M,g)\) be vacuum Bianchi IX with Mixmaster past attractor and let
\(\phi\) be the conformally coupled massless scalar on \((M,g)\). Assume a
Hadamard quasifree state \(\omega\) exists on the AQFT net. Then the
inductive-limit local algebra
\[
\mathcal A(D_{\rm BB})_{\rm B\text{-}IX}
=\overline{\bigcup_{t_i>0}\mathcal A(D_{t_i})}^{C^*}
\]
does **not** admit \(\omega\) (nor any state in its BFV folium) as a
cyclic-separating vector in any GNS representation.

**Proof.** Smear the Wightman 2-pt against
\(f(t,\vec x)=\chi_{[\delta,\epsilon]}(t)\,h(\vec x)\) with \(h\) carrying
nonzero \(S^3\)-zero-mode. The SLE Hadamard state on Bianchi IX (assumed)
yields the volume normalisation \(1/\sqrt{V(t_x)V(t_y)}\). Using the
Heinzle–Uggla pathwise bound \(V(t)\le c_2 t\):
\[
\langle\phi(f)^2\rangle \;\ge\; \frac{K}{c_2}\!\!
\int_\delta^\epsilon\!\!\int_\delta^\epsilon \frac{dt_x\,dt_y}{t_x t_y}
=\frac{K}{c_2}\bigl[\ln(\epsilon/\delta)\bigr]^{2}\to+\infty \text{ as }\delta\to 0^+.
\]
By Verch (1994) local quasi-equivalence + BFV (2003) covariant locality,
the divergence holds for the entire BFV folium. Cyclic-separating vectors
carry normal states; contradiction. ∎

**This is STRONGER than the µ-a.e. statement requested by the parent
agent**: pathwise bound, not measure-theoretic. The Heinzle–Uggla
invariant measure is **not** required for the volume-form T2.

The µ measure becomes necessary only for finer spectral questions
(Lyapunov rates, mode-by-mode UV averaging, higher-n-point functions).

---

## 3. DHN / Hartnoll–Yang short-circuit — FAILS

Hartnoll–Yang 2025 (arXiv:2502.02661, verified) maps BKL dynamics on
Bianchi IX, **at each spatial point**, to a particle in a
half-fundamental-domain of \({\rm PSL}(2,\mathbb Z)\) on \(\mathbb H\).
Semiclassical quantisation gives a conformal QM whose dilatation
eigenstates are odd automorphic L-functions on \({\rm Re}\,s=1/2\).

**Why it doesn't short-circuit T2.** This is a **1d quantum mechanics on
the Bianchi IX minisuperspace** \((\alpha,\beta_+,\beta_-)\), built from a
**single wavefunctional** ψ. T2 needs the **type-classification** of a
**net of vN algebras** \(\{\mathcal A(D)\}\) — an infinite-dimensional
QFT-on-curved-spacetime structure. There is no functorial map from
\(\mathcal A(D_{\rm BB})_{\rm B\text{-}IX}\) to the L-function Hilbert
space that preserves modular structure. Restricting to homogeneous \(k=0\)
modes that survive the BKL truncation yields an abelian
\(C(\beta_+,\beta_-)\) — a Type I subalgebra, not the Type III\(_1\) BFV
folium we need to obstruct. The Hartnoll–Yang dilatation operator has
continuous spectrum on \({\rm Re}\,s=1/2\), giving a Type I\(_\infty\)
representation whose modular flow is not outer.

**Verdict.** Beautiful framework, wrong category. Cannot short-circuit
the algebraic-AQFT obstruction.

---

## 4. Best result

**Theorem T2-Bianchi IX (pathwise rigorous, conditional on Hadamard).**
Stated above. Status:

| Step | Status |
|------|--------|
| Volume bound \(V(t)\le c\,t\) pathwise | RIGOROUS via Heinzle–Uggla 2009 attractor thm |
| Smeared 2-pt log² divergence | sympy-VERIFIED |
| BFV folium quasi-equivalence | RIGOROUS (Verch 1994 + BFV 2003) |
| Hadamard state existence on B-IX | **OPEN** (Banerjee–Niedermaier 2023 covers B-I only) |

So Bianchi IX joins Bianchi V as **conditional on Hadamard existence**,
which is a single open problem in the AQFT-on-curved-spacetime literature
(not specific to our framework). Bianchi I remains the only fully
unconditional case.

---

## 5. Effort estimate

- Section addition to `algebraic_arrow.tex` (B-I T2 + B-IX pathwise T2 +
  Open Q for Hadamard): **1–2 weeks** (reuse `/tmp/T2_bianchi_*.{py,tex}`).
- Standalone Comment paper (FRW + B-I + B-IX, with Hadamard noted as
  open): **2–3 months**.
- Resolving Hadamard existence on B-IX: **6–12 months** for an expert in
  microlocal AQFT (would interface with Banerjee–Niedermaier and the
  Sahlmann–Verch/Hollands–Wald framework on \(S^3\)).
- Full Hartnoll–Yang ↔ AQFT bridge (different goal — would need a new
  "automorphic-L-function" folium concept): **multi-year programme**.

---

## 6. Next step

**Recommended.** Add a new **Section 6.3** to `algebraic_arrow.tex` titled
"Theorem T2 for Bianchi I and IX (vacuum, conditional on Hadamard)",
combining the B-I result from `/tmp/T2_bianchi_extension.tex` with the
B-IX pathwise extension from `/tmp/T2_bianchi_IX.tex`. List the four
residual gaps explicitly:

1. Hadamard state existence on B-IX (S³ spatial slice).
2. Hadamard state existence on B-V (H³ spatial slice, non-compact).
3. Whether the pathwise bound \(V(t)\le c\,t\) extends to **matter**
   Bianchi IX (e.g. with a stiff fluid that does not bring the trajectory
   to the Kasner attractor — Belinski–Khalatnikov 1973 universality may
   or may not survive).
4. The Heinzle–Uggla invariant measure µ becomes relevant if the proof
   is upgraded to track higher-order Wightman functions, where the
   averaging over Kasner exponents enters explicitly.

**Do NOT** start a standalone CQG-Comment paper yet: gaps 1–2 are
literature-open and would diminish the claim. Better to consolidate as a
section of the existing FRW companion, then watch the literature for B-V
or B-IX Hadamard-existence results.

---

## 7. Files produced

- `/tmp/T2_bianchi_IX.md` — this summary (~485 words effective content).
- `/tmp/T2_bianchi_IX.py` — sympy verification of C1–C7 (clean run).
- `/tmp/T2_bianchi_IX.tex` — full proof writeup.

## 8. Sources verified this session

- Damour, Henneaux, Nicolai, "Cosmological Billiards", CQG 20 (2003) R145,
  **arXiv:hep-th/0212256** — VERIFIED via arXiv API.
- Hartnoll & Yang, "The Conformal Primon Gas at the End of Time",
  **arXiv:2502.02661** (2025) — VERIFIED via arXiv API.
- Heinzle & Uggla, "Mixmaster: Fact and Belief", CQG 26 (2009) 075016,
  **arXiv:0901.0776** — VERIFIED via arXiv author search (the parent
  agent's "0901.2891" was wrong — that ID is a chemistry paper).
- Heinzle & Uggla, "A new proof of the Bianchi type IX attractor
  theorem", CQG 26 (2009) 075015, **arXiv:0901.0806** — VERIFIED.
- Banerjee & Niedermaier, "States of Low Energy on Bianchi I spacetimes",
  J. Math. Phys. 64 (2023) 113503, arXiv:2305.11388 — relied on prior
  verification in T2_bianchi_extension session.
- Verch (CMP 1994), BFV (CMP 2003 / arXiv:math-ph/0112041) — relied on
  prior verification in T2_bianchi_extension session.
- Damour & Nicolai, arXiv:hep-th/0410245 — NOT re-verified this session
  (arXiv API rate-limited); cited via T2_bianchi_extension chain.
- Bogoyavlenskaya & Brindejonc (Mixmaster ergodicity, 2014) — search
  did not return a unique hit; not cited in the writeup.
