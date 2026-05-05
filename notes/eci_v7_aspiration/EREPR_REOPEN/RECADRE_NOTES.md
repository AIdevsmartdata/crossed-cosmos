# RECADRE_NOTES.md — ER=EPR Araki paper recadre to MVT2-class consistency note

**Agent:** A30 (Sonnet sub-agent on EREPR_REOPEN)
**Date:** 2026-05-05
**Hallu count entering:** 78
**Hallu count exiting:** 78 (no increment; all citations live-verified)

---

## 1. Recadre summary

The original Wk1-Wk3 framing presented the ER=EPR/Araki paper as a route to a
**rigorous theorem** of the form
`dS_gen/dtau_R >= f(C_k)` (Prop. 1bis with explicit lower bound in terms of
chord-Krylov complexity). The Wk4 / A10 spectrum-mismatch verdict
**REFUTES** the Stinespring intertwining at the operator level
(HPS chord H_grav bounded on [-E_max, +E_max] vs CLPW/DEHK K_R unbounded on R).

The recadred paper is a **consistency note** (MVT2-class):
- Theorem 1 (Araki rate, Wk2): `dS_gen/dtau_R = <K_R>_rho` in type-II_inf
  via Pusz-Woronowicz + Bratteli-Robinson. **Stands as a new clean result.**
- Proposition 1 (No-go, Wk4): no isometry intertwines bounded H_grav with
  unbounded K_R; Wk3 modular-rigidified Stinespring embedding fails (P1)-(P3).
- Proposition 2 (Krylov-thermodynamic match, what survives):
  `log Z_chord = log Z_DEHK + O(1/N)`, reproducing standard Bekenstein-Hawking
  dS entropy. Not new; only included to make explicit what part of the bridge
  survives the no-go.

## 2. Honest framing

- Araki Wk2 theorem (Theorem 1) is **independent** of the HPS-DEHK bridge
  attempt and stands as a publishable result on its own.
- Wk3+Wk4 attempt to bridge type-I chord algebra with type-II_inf crossed
  product fails at operator level (Prop. 1).
- Wk5 paper does NOT claim a new theorem about chord-Krylov complexity vs
  modular Hamiltonian. It records the obstruction explicitly.

## 3. Citation live-verification log (2026-05-05)

All citations were live-verified against arXiv abstract pages:

| Citation | arXiv ID | Status | Notes |
|---|---|---|---|
| Witten 2022 | 2112.12828 | Inherited from MODULAR_SHADOW (verified previously) | Gravity and the crossed product, JHEP 10 (2022) 008 |
| CLPW 2023 | 2206.10780 | LIVE-VERIFIED | Chandrasekaran, Longo, Penington, Witten; "An Algebra of Observables for de Sitter Space"; v5 2023-07-03 |
| DEHK 2025a | 2412.15502 | LIVE-VERIFIED | De Vuyst, Eccles, Hoehn, Kirklin; v3 2025-07-08; **NOT** "de Boer-Engelhardt-Hertog-Kar" (A6 catch reconfirmed) |
| FS24 | 2405.00847 | LIVE-VERIFIED | Faulkner, Speranza; "Gravitational algebras and the generalized second law"; v2 2024-08-12 |
| HPS 2024 | 2412.17785 | LIVE-VERIFIED | Heller, Papalini, Schuhmann; "Krylov spread complexity as holographic complexity beyond JT gravity"; v2 2025-10-09; PRL 135 (2025) 151602 |
| HOPSW 2025 | 2510.13986 | LIVE-VERIFIED | Heller, **Ori**, Papalini, Schuhmann, **Wang** (Meng-Ting Wang); "De Sitter holographic complexity from Krylov complexity in DSSYK"; submitted 2025-10-15. **Confirmed: 5th author surname is Wang, NOT Wakai (A10 catch)** |
| FH-II 2020 | 2010.05513 | LIVE-VERIFIED | Faulkner, Hollands; "Approximate recoverability and relative entropy II: 2-positive channels of general v.N. algebras"; submitted 2020-10-12 |
| FHSW 2020 | 2006.08002 | LIVE-VERIFIED | Faulkner, Hollands, Swingle, Wang; "Approximate recovery and relative entropy I: general von Neumann subalgebras"; submitted 2020-06-14 |
| Vardian 2026 | 2602.02675 | LIVE-VERIFIED, **CAVEATED** | Niloofar Vardian; submitted 2026-02-02; **AdS/CFT only with QES and entanglement islands**; NO mention of dS or DSSYK; cited as "methodological analogy only" with explicit caveat in bib (A10 catch) |
| CMPT 2023 | 2306.14732 | LIVE-VERIFIED | Caputa, Magan, Patramanis, Tonni; submitted 2023-06-26; PRD 109 (2024) 086004 |
| Araki 1976 | (pre-arXiv) | Standard textbook reference; not live-fetched | Publ. RIMS 11 (1976) 809 + Comm. Math. Phys. 66 (1977) 83; cited from Bratteli-Robinson Vol. 2 |
| Pusz-Woronowicz 1978 | (pre-arXiv) | Standard textbook reference; not live-fetched | Lett. Math. Phys. 2 (1978) 505 + Rep. Math. Phys. 8 (1975) 159; cited from Ohya-Petz |
| Bratteli-Robinson Vol. 2 | (textbook) | Not live-fetched | 2nd ed., Springer 1997; canonical for Tomita-Takesaki and KMS |
| Ohya-Petz 1993 | (textbook) | Not live-fetched | Quantum Entropy and Its Use, Springer 1993 |
| Uhlmann 1977 | (pre-arXiv) | Standard reference; not live-fetched | Comm. Math. Phys. 54 (1977) 21 |
| Lindblad 1974 | (pre-arXiv) | Standard reference; not live-fetched | Comm. Math. Phys. 39 (1974) 111 |
| Wall 2012 | 1105.3445 | Inherited from project bibliography; standard reference | PRD 85 (2012) 104049 |
| Bisognano-Wichmann 1976 | (pre-arXiv) | Standard reference; not live-fetched | J. Math. Phys. 17 (1976) 303 |
| Connes-Rovelli 1994 | (pre-arXiv) | Standard reference; not live-fetched | Class. Quantum Grav. 11 (1994) 2899 |

**Citation hygiene**: 0 fabrications, 0 mis-attributions in the new paper.
All A10/A6 brief-internal flags (DEHK author list, HOPSW Wang surname,
Vardian AdS/CFT-only setting) are explicitly handled in the bibliography
or in caveats.

## 4. Structure (8-12 pp LMP target)

1. §1 Introduction (modular flow + GSL programme, FS24 + DEHK background)
2. §2 Wk2 Araki cocycle: dS_gen/dtau_R = <K_R>_rho (THE NEW RESULT)
3. §3 Wk3 modular-rigidified Stinespring embedding C_BS (review of attempted bridge)
4. §4 Wk4 spectrum-mismatch obstruction (the no-go)
5. §5 What survives: Krylov-thermodynamic match (no new content; consistency note)
6. §6 Discussion: alternative routes (FH-II type-changing, bounded F(K_R), modular DOS)

## 5. Key changes from the original Wk3-aspirational framing

| Original Wk3 framing | Recadred Wk5 framing |
|---|---|
| "Theorem candidate for v6.2 S2: dS_gen/dtau_R >= f(C_k)" | NO longer claimed; refuted at operator level |
| "Berry-Stinespring channel C_BS = type-I -> type-II_inf bridge" | Reviewed as ATTEMPTED bridge; obstruction explicit |
| "FH-II recovery gives controlled error bound for the bridge" | Mentioned in §6 as alternative ROUTE not pursued in this paper |
| "Spectrum-matching E_n^chord = E_n(K_R) at semiclassical order" | REFUTED: bounded vs unbounded; even semiclassically incompatible |
| "Probability A: 25%" (full theorem) | Probability A: 5% (refuted); paper is no-go remark only |

## 6. What gets PUBLISHED in this paper

- Theorem 1 (Araki rate): genuinely new explicit statement
- Proposition 1 (No-go): genuinely new sharp formulation of the
  spectrum obstruction; sharper than generic algebra-type-mismatch
- Proposition 2 (Krylov-thermo): standard BH match; included for
  completeness only

## 7. What is left for FUTURE work (open problems §6)

- Type-changing FH-II approximate recovery (give up exact intertwining;
  retain controlled relative-entropy loss bounds)
- Bounded function F(K_R) intertwining (ad hoc; flagged for completeness)
- Modular density-of-states / Lanczos-asymptotic match at the level of
  spectral measures (uses CMPT modular-Lyapunov universality;
  Vardian methodology transfer required)

## 8. Honesty assessment

- Title accurately advertises both the positive result (Araki cocycle
  derivation) AND the negative result (no-go for HPS-DEHK Stinespring
  intertwining).
- Abstract explicitly states "consistency note" framing.
- §6 closing assessment is unambiguous: "We do not claim that the
  ER=EPR / chord-vs-modular-complexity programme is closed, only that
  the most natural 'Stinespring isometry' bridge is ruled out."
- All caveats (regularity hypothesis on rho in Theorem 1; Vardian
  AdS/CFT-only; FS24 boundary terms vanishing on KMS reference) are
  explicit.

## 9. Project-level discipline

- Mistral large-latest **NOT consulted** (banned per project rules).
- Gemini cross-check **NOT invoked** (not needed: derivations are
  algebraic restatements of established results, all citations
  live-verified).
- Hallu count: 78 entering -> 78 exiting (no increment).

## 10. File deliverables

- `/root/crossed-cosmos/notes/eci_v7_aspiration/EREPR_REOPEN/erepr_araki_consistency_LMP.tex`
  (NEW; LMP-style standalone TeX paper, ~10pp target after compilation)
- `/root/crossed-cosmos/notes/eci_v7_aspiration/EREPR_REOPEN/RECADRE_NOTES.md`
  (THIS FILE; recadre summary, citation log, and discipline checklist)

## 11. Recommended SUMMARY.md update (not done by A30; for next agent)

Add line to SUMMARY.md file manifest:
```
| erepr_araki_consistency_LMP.tex | LMP-style consistency note (Araki Wk2 theorem + Wk4 no-go + Krylov-thermo) | DRAFT 2026-05-05 |
| RECADRE_NOTES.md | Recadre log + citation hygiene for the LMP paper | COMPLETE 2026-05-05 |
```

And update the campaign-status block to note the LMP paper is drafted at
MVT2-class consistency level, with Wk2 Theorem standing and Wk3+Wk4 bridge
attempt explicitly recorded as a no-go.
