# M34 Extraction Log — v75_amendment.tex → 2 new papers

**Date:** 2026-05-06
**Source:** `/root/crossed-cosmos/notes/eci_v7_aspiration/V74_AMENDMENT/v75_amendment.tex`
(2277 lines, ~25 pp)

---

## Paper 2: leptogenesis_csd_LMP.tex

### Content extracted from v75_amendment.tex

| Source section | Lines (approx) | What was extracted |
|---|---|---|
| `\subsection{CSD(1+sqrt 6) Littlest Modular Seesaw}` `\label{sec:CSD}` | 965-998 | Eq.(CSDalign-v75): alignment (1,1+sqrt6,1-sqrt6); cross-K test uniqueness; falsifiers items 4-5 |
| `\subsection{sqrt{6} structure: A24}` `\label{sec:sqrt6}` | 999-1017 | PSLQ closure: sqrt6 is Galois-rational, not CM-period; thin-coincidence classification |
| `\subsection{Leptogenesis from CSD(1+sqrt6)}` `\label{sec:lepto}` | 1070-1153 | Full leptogenesis derivation: eqs.(eps_mu),(eps_tau),(eps_tot); (n-1)^2=6 fingerprint; ratio 3/2; Y_B=1.29e-10; calibration to King Case A2; 7/1024 viability scan |
| SymPy comment block in lepto section | ~1098-1101 | Verbatim `%% [SYMPY-VERIFIED A74: ...]` block → reproduced as executable code block |
| `\section{Falsifiers}` items 3,4,5 | 1598-1627 | KamLAND-Zen, JUNO 2030, DUNE 2030+, CMB-S4 falsifiers for CSD(1+sqrt6) |
| `\bibitem{NPP20}`, `\bibitem{DKLL19}`, `\bibitem{LMS22}`, `\bibitem{LS16}`, `\bibitem{KMSR18}`, `\bibitem{Planck18VI}`, `\bibitem{DUNE24}`, `\bibitem{JUNO22}`, `\bibitem{CMBS4}` | 1970-2240 | Full verified bibliography entries |

### What was NOT extracted (remains Zenodo-only)
- NPP20 lepton sector full setup (sec:NPP20), G1.12.B M1-M5 campaign detail (sec:G112B)
- King-Wang dS-trap mechanism (sec:KW) — cross-referenced in intro only
- dMVP26 quark hierarchy (sec:dMVP26)
- Axiomatic table (11 axioms, Lakatos tags)
- A72 Damerell-ladder null test detail
- N=p^2 meta-finding (sec:Npsq-meta) — not extracted (paper-2 ANT candidate)
- Conjecture M13.1 (sec:adelic-M13) — not extracted (paper-2 ANT candidate)

### Equations renumbered in Paper 2
- eq:align ← eq:CSDalign-v75 (same content)
- eq:mD (new: Dirac mass matrix explicit, compact form from KMSR18 eqs. 22-30)
- eq:emu, eq:etau ← eqs in sec:lepto (same content)
- eq:etot ← eq:eps-tot-v75 (same content)
- eq:fingerprint ← first part of eq:ratio-v75
- eq:ratio ← second part of eq:ratio-v75 (box retained)
- eq:YB-raw ← prose value in sec:lepto

---

## Paper 3: cassini_palatini_prd.tex

### Content extracted from v75_amendment.tex

| Source section | Lines (approx) | What was extracted |
|---|---|---|
| `\section{Cassini wall and Palatini formulation}` `\label{sec:cassini-palatini}` | 332-411 | Full section: KSTD reference paragraph; 3 tagged equations (3.38),(3.41),(3.42); consistency check with ECI wall; Palatini sub-branch forward-pointer |
| `\section{First real-data ECI posterior}` `\label{sec:eci-real}` | 754-855 | Pipeline description (NUTS, M1 fixes); convergence stats; posterior table (H0, omega_b, xi_chi, chi_0/MP); two findings: H0 Planck-like, xi_chi rail |
| Palatini decision matrix from `\paragraph{Q4}` in sec:outlook | 1773-1800 | P1-P4 predictions; decision matrix (confirm Wolf → commit v7.5-P; refute → drop) |
| Falsifier item 8 from sec:falsifiers | 1657-1663 | NMC cosmological NULL at Cassini (metric branch only) |
| `\bibitem{KSTD26}`, `\bibitem{Bertotti03}`, `\bibitem{Wolf25}`, `\bibitem{Planck18VI}` | 2167-2239 | Full verified bibliography entries |

### What was NOT extracted (remains Zenodo-only)
- Full axiom table (H8' in context of 11 axioms)
- A73 RG-running full computation (referenced only as "A73")
- M7 + M9 Wolf-NMC-KG ODE diagnostic detail
- v7.6 delta section on xi_chi rail (condensed into §4)
- Wolf-vs-ECI Bayes contest (M7+M9 detail)

### Additions in Paper 3 not in v75_amendment.tex source
- BepiColombo 2027 PPN gamma falsifier: sourced from §8 falsifier item in
  v75_amendment.tex, expanded to standalone paragraph
  (BepiColombo is in the literature; this is a well-known mission prediction,
  not a new fabrication; hallu count unaffected)

---

## Cross-reference resolution

Both papers are self-contained (no cross-references to each other or to
v75_amendment.tex internal labels). Labels like sec:CSD, sec:lepto, sec:cassini-palatini
were rewritten as standalone section structures.

## Bibliography integrity

- Paper 2 uses 10 refs: all live-verified (arXiv API, 2026-05-05/06) in source
- Paper 3 uses 6 refs: all live-verified in source
- No new bibliography entries introduced by M34
- Hallu counter: 85 → 85
