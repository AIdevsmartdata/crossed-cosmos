---
name: M59 citation additions — exact text added per paper
type: log
date: 2026-05-06
---

# M59 — Citation additions log

## Paper 1: P-NT BLMS (`PNT/paper_lmfdb_s4prime.tex`)

### Insertion point
After `\subsection{Future directions}` enumerate list (end of §6 Discussion).

### Added text (Remark block)
```latex
\begin{remark}[Anticyclotomic $p$-adic $L$-function gap]\label{rem:anticycl}
The companion paper-2 (Conjecture~M13.1) targets a Pollack-type
$p$-adic $L$-function for $f = \mathtt{4.5.b.a}$ at the prime $p=2$
(ramified in $K=\Q(i)$, $k=5$ odd, $a_2 = -4 \ne 0$).
We observe that all recent anticyclotomic Iwasawa main-conjecture
frameworks explicitly exclude this parameter regime:
Sano~\cite{Sano2510} (Tamagawa anticyclotomic, $p$ split, $k$ even),
Lee~\cite{Lee2508} (CM Euler systems, $p$ odd ordinary),
Isik~\cite{Isik2412} (Hecke characters, $p$ odd ordinary),
Longo--Pati--Vigni~\cite{LPV2603} (anticyclotomic IMC, $p$ odd ordinary, $k \ge 4$ even),
and Nguyen~\cite{Nguyen2503} (congruences anticyclotomic).
The triple $\{p=2 \mid N,\; k \text{ odd},\; a_p \ne 0\}$ remains a
genuine open case in the literature, confirming that Conjecture~M13.1
targets new arithmetic territory.
\end{remark}
```

### New bibitems added (5)
- `\bibitem{Sano2510}` — arXiv:2510.01601
- `\bibitem{Lee2508}` — arXiv:2508.05861
- `\bibitem{Isik2412}` — arXiv:2412.10980
- `\bibitem{LPV2603}` — arXiv:2603.22483 (Longo-Pati-Vigni)
- `\bibitem{Nguyen2503}` — arXiv:2503.00247

NOTE: `\Q` macro not defined in this file; this paper uses `\Q` (need to verify it's defined or fix to `\mathbb{Q}`). Check compile.

---

## Paper 3: Modular Shadow LMP v2.5 (`MODULAR_SHADOW/modular_shadow_LMP_v2.5.tex`)

### Insertion point
In §1 Introduction, before `\paragraph{Literature status as of 2026-05-06.}`

### Added text (paragraph block)
```latex
\paragraph{Related work on arithmetic chaos and Krylov complexity.}
De~Clerck--Hartnoll--Santos~\cite{HartnollDCS2024}
studied the AdS black-hole interior via a Mixmaster Bianchi~IX
reduction, identifying the BKL bounce sequence with geodesic flow
on the $\Gamma(2)$ arithmetic modular surface (the same arithmetic
substrate as the Gauss-map correspondence).
Their work establishes the arithmetic chaos connection but does
\emph{not} employ a type-II$_\infty$ crossed-product completion
and does not derive a Krylov-complexity bound; our Theorem~\ref{thm:bound}
supplies the natural quantum-information completion of that programme.
In the cosmological direction, Speranza~\cite{Speranza2025} constructed
an intrinsic observer Hilbert space applicable beyond static de~Sitter,
and Requardt~\cite{Requardt2501} examined the role of type-II$_\infty$
von~Neumann algebras in quantum gravity.
Motaharfar--Siebersma--Singh~\cite{MSS2511} computed Krylov complexity
in canonical FRW (isotropic) quantum cosmology; their setting is
isotropic and does not capture the anisotropic BKL structure
studied here.
```

### New bibitems added (3; Speranza2025 was pre-existing)
- `\bibitem{HartnollDCS2024}` — arXiv:2312.11622, JHEP 07 (2024) 202
- `\bibitem{Requardt2501}` — arXiv:2501.06009
- `\bibitem{MSS2511}` — arXiv:2511.17711 (Krylov FRW — distinct from Bianchi IX)

---

## Paper 7: Proton-decay PRD (`OPUS_G112B_M6/proton_decay_prediction_PRD.tex`)

### Insertion point
Added as 4th item in the "Comparison to recent literature" itemize in §6 Discussion.

### Added item text
```latex
\item {\em Loualidi-Miskaoui-Nasri}~\cite{LMN2503} construct a
nonholomorphic $A_4$ modular SU(5) GUT
[Phys.~Rev.~D~\textbf{112} (2025) 015008, arXiv:2503.12594].
This framework uses $A_4$ (not $S'_4$) and does not evaluate the
proton-decay ratio at the modular fixed point $\tau=i$; the
$\kappa_u$-INDEPENDENT prediction
$B = f^{uu}(\tau=i)/f^{uc}(\tau=i) = 1.077$
is therefore specific to the present $S'_4$ framework.
```

### Correction to M48 text
M48 stated "JHEP Jan 2026" — live verification shows Phys.Rev.D 112 (2025) 015008. Corrected.
M48 called authors "Chen-Li-Liu-Ratz" which is a DIFFERENT existing bibitem. Actual authors: Loualidi, Miskaoui, Nasri.

### New bibitems added (1)
- `\bibitem{LMN2503}` — arXiv:2503.12594, Phys.Rev.D 112 (2025) 015008

---

## Paper 8: M45 Bianchi IX (`M45_BIANCHI_IX_PAPER/bianchi_ix_modular_shadow.tex`)

### Insertion point
In §1 Introduction, after the Fan-Fathizadeh-Marcolli sentence, before `\paragraph{Aim of this paper.}`

### Added text
```latex
De~Clerck--Hartnoll--Santos~\cite{HartnollDCS2024} studied AdS
Mixmaster chaos via the $\Gamma(2)$ arithmetic substrate
(arXiv:2312.11622), focusing on Hamiltonian-quantization eigenvalues
of the interior geometry.
Our framework provides the natural type-II$_\infty$ crossed-product
$+$ Krylov-complexity completion of that programme: we identify the
Speranza modular flow with the BKL Gauss-shift rate, and conjecture
a sharp $\lambda_K \le \lambda_{\mathrm{BKL}}$ bound.
```

### New bibitems added (1)
- `\bibitem{HartnollDCS2024}` — arXiv:2312.11622, JHEP 07 (2024) 202

---

## Paper 9: v7.6 amendment (`V74_AMENDMENT/v75_amendment.tex`)

### Insertion point
At end of §10 (Adelic Katz section), after `\paragraph{Paper-2 plan.}`, before `\section{Falsifiers}`.

### Added text (new paragraph)
Full unification paragraph per M49/M53/M54 corrections:
1. Weight-2 companion is 32.2.a.a (level 32), NOT 4.2.a.a (does not exist)
2. Two distinct characters of same Q(i) CM tower (ψ_5 z^4 vs ψ_2 z^1)
3. Tavartkiladze 2512.24804 = TENSION not corroboration (Γ_2≃S_3 → inverted vs ECI S'_4 → normal)
4. New sharp prediction m_1 = 0 exact (rank-2 M_ν, testable KamLAND-Zen 2027 / nEXO 2030+)
5. JHEP 01(2019)234 for 1511.05321 confirmed (CrossRef DOI 10.1007/JHEP01(2019)234)

### New bibitems added (3)
- `\bibitem{FFM2015}` — arXiv:1511.05321, JHEP 01(2019)234
- `\bibitem{Fan2017}` — arXiv:1709.08082, Lett.Math.Phys 108 (2018)
- `\bibitem{Tavartkiladze2512}` — arXiv:2512.24804 "Minimal Modular Flavor Symmetry and Lepton Textures Near Fixed Points"

---

## Post-edit checks needed (for parent)

1. **Paper 1**: Verify `\Q` macro is defined in `paper_lmfdb_s4prime.tex`; if not, replace `$\Q(i)$` with `$\mathbb{Q}(i)$` in the new remark. (Other papers use `\Q` without trouble in that file — check preamble.)
2. **Paper 9**: The `\paragraph{Modular unification note:...}` has `\label{para:unification}` — LaTeX \paragraph cannot take \label directly in some setups; remove `\label` if compile fails.
3. **All**: pdflatex compile to check undefined references and undefined commands.
