# v8 bridge v5 ↔ v6 — Claude app extended audit of agent 6 finding

**Date.** 2026-04-22.
**Source.** Claude-app memo on Jacobson-EGJ bridge attempt.
**Relation to this repo.** Independent analysis confirming CLI agent 6
`v8_agent_06_report.md` (verdict DERIVATION-OBSTRUCTED) with 4 granular
sub-obstructions and 2 key literature anchors not previously surfaced.

**Verdict concur.** BRIDGE-FAILURE. Already codified in FAILED.md F-14;
this memo is the extended technical justification.

---

## Added value of this memo vs agent 6

Agent 6 reported **Req A fatal** (C_k state functional vs d_iS extrinsic
horizon geometric). Claude-app decomposes that same blocker into **four
independent obstructions**:

- **F-10a — Structural obstruction EGJ.** $d_iS$ in Eling-Guedens-Jacobson
  is imposed by Bianchi closure on an already-modified entropy
  $S_W = f'(R) A/(4G)$. Substituting $\kappa_R C_k \Theta d\tau_R$ for
  $d_iS$ with $S = A/(4G)$ unchanged cannot generate new tensor
  structure. **Auto-consistency tautology, not derivation.**

- **F-10b — Gaussian obstruction on coherent states.** $C_{\rm spread}[|\alpha\rangle\langle\alpha|]$
  of a coherent scalar field state is insensitive to $|\alpha|^2$ at
  leading order (covariance matrix invariant under coherent shift).
  The $\chi^2$ required for NMC coupling does not emerge from
  $\delta C_{\rm spread}/\delta g_{\mu\nu}$. The Krylov-Nielsen
  confusion (Guo-Hernandez-Myers-Ruan arXiv:1807.07677 finds
  $\Delta C_{\rm Nielsen}^2 \approx |\alpha|^2/2$ for Nielsen complexity,
  but Nielsen and Krylov are different beasts) resolves toward Krylov
  in our case.

- **F-10c — C_k Ma-Huang/Haferkamp without $g_{\mu\nu}$ dependence.**
  Ma-Huang 2024 (arXiv:2410.10116) and Haferkamp 2021 (arXiv:2106.05305)
  define $C_k$ in an abstract qubit framework with no reference to
  $g_{\mu\nu}$. Assimilating $C_k$ to a functional of $\rho_R$ on curved
  QFT is an **unsupported terminological identification** — same pattern
  as F-6 (PH ≠ HP). Structural blocker.

- **F-10d — Crossed product does not predict coupling coefficients.**
  CLPW 2206.10780, Faulkner-Speranza 2405.00847, Kirklin 2412.01903,
  DEHK 2024-2025 all take matter action as *input*, regularize the QFT
  entropy, and prove the GSL. None predict $\xi_\chi$. Jensen-Sorce-Speranza
  arXiv:2306.01837 is closest but confirms presupposition of action.

Each sub-obstruction is rigorously documented with primary citations.

## New literature anchors this memo introduces

1. **Casini-Galante-Myers 2016** (arXiv:1601.00528, *JHEP* 03:194).
   MVEH derivation of Einstein equations (Jacobson 2016 arXiv:1505.04753)
   fails for operators with conformal weight $\Delta$ in the window
   $(d-2)/2 < \Delta < d/2$. **A massive scalar in d=4 has $\Delta = 1$,
   precisely in this critical window.** Non-conformal matter (where
   quintessence sits) is outside the clean entropic-gravity regime.
   Adjacent obstruction, not primary, but reinforces the verdict.

2. **Brustein-Hadad 2009** (*PRL* 103:101301). Formal statement that
   $\delta Q = T \delta S$ with Wald entropy is EQUIVALENT to the EOM of
   ANY diff-invariant theory. I.e. thermodynamics cannot predict what
   was put into the action. This is the **deep reason** all three voies
   (A, B, C) of the bridge fail: it's not that we chose the wrong
   substitution, it's that the substitution mechanism is structurally
   tautological.

## Naive dimensional estimate

Claude-app reports: for $\xi_\chi = \alpha (T_{dS}/M_P)^2 \lambda_L^{\rm mod} \ell_{\rm PH}$
with $T_{dS} \approx 2.66 \times 10^{-30}$ K, $(T_{dS}/M_P)^2 \approx 3.5 \times 10^{-124}$,
$\lambda_L^{\rm mod} = 2\pi$ universal, one gets $\xi_\chi \sim 10^{-123}$
as a naive baseline.

This is **128 orders of magnitude below** the DESI DR2 posterior
$\xi_\chi = 0.003 +0.065/-0.070$ (v5). While technically compatible with
the null result (in the sense that both are consistent with zero), the
prediction is not distinguishable from $\xi = 0$. **Not a Popperian
prediction.**

This numerical observation is concurrent with the structural verdict:
even if the bridge existed, the prediction would be below observational
threshold by 128 orders. Good-faith falsifiers at DESI / Euclid / CMB-S4
resolution cannot reach it.

## Three honest next steps (not to be pursued for v6.1)

Claude-app proposes three chantiers, each bounded in scope:

1. **Wald entropy self-consistency check.** $S_W = F(\chi) A/(4G)$ with
   $F(\chi) = 1 - 8\pi G \xi_\chi \chi^2$; check via Chirco-Eling-Liberati
   arXiv:1011.1405 that $d_iS$ reproduces the NMC EOM. Technical
   confirmation at EOM level, not action derivation. **Not a new paper.**

2. **Explicit $\langle T_{\mu\nu}\rangle_{\rm ren}$ computation** via
   CLPW for NMC scalar in dS static patch. Extends Jensen-Sorce-Speranza
   2306.01837. Useful exercise, does not predict $\xi$. **Not a new
   paper.**

3. **Reorient: does v6 constrain observables OUTSIDE cosmology?**
   Tabletop systems where $T_R$, $\tau_R$ controllable; lattice QFT
   simulations. V6-4 compliant (non-cosmological). **Most interesting
   of the three; requires new work, not a re-derivation.**

## What the memo explicitly rules out

Quote: « Présenter cette tentative comme un succès partiel ou suggérer
qu'une "saturation observationnelle" de l'inégalité v6 serait établie
par le null result de v5 violerait les règles V6-1 (pas d'égalité
promue sans preuve) et V6-4 (pas de nouveau falsifier). »

This is correct and binding. The null result of v5 is compatible with
$\xi = 0$ (strict ΛCDM) and with any theory predicting small $\xi$;
it has no specific probative value for v6.

## Action for the repo

- Keep this memo as `v8_bridge_v5_v6_claude_app.md` — complementary
  to `v8_agent_06_report.md` and `v8_synthesis.md` §B.6.
- Update FAILED.md F-14 with the four sub-obstructions and new literature
  anchors.
- No v6 modification.
- No new paper.
- The owner-facing takeaway: v5 and v6 remain defensible, independent,
  and disjoint. **That is the honest scientific result.**
