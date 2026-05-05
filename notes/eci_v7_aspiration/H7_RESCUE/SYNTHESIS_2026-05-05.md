# H7 Rescue Synthesis — 2026-05-05 early morning

After G1.15 REFUTED the original H7 (Damerell-CS bridge at s=k/2=5/2 half-integer
outside Damerell/Shimura/Deligne algebraicity domain for k=5 odd), three Sonnet
sub-agents (H7-A, H7-B, H7-C) independently explored rescue paths. **All three
recommend KEEPING the LMFDB CM newform 4.5.b.a (CM by Q(i)) as the v7.4 anchor.**

## H7-A POSITIVE — Damerell ladder at INTEGER critical points

L(f, m) computed via approximate functional equation (Iwaniec-Kowalski Thm 5.3,
mpmath dps=60, sanity-check L(f, 5/2) = 0.5200744676 matches LMFDB exact):

| m | L(f, m)            | algebraic part L(f,m)·π^(4−m)/Ω_K⁴ | Cardy hit ρ=c/12 |
|---|--------------------|------------------------------------|------------------|
| 1 | 0.15244713359...   | **1/10**                           | (c=6/5, exotique non-CFT std) |
| 2 | 0.39910566245...   | **1/12**                           | ✅ **EXACT, c=1** (free boson) |
| 3 | 0.62691370859...   | **1/24**                           | ✅ **EXACT, c=1/2** (Ising) |
| 4 | 0.78780300053...   | **1/60**                           | matches via 1/5, 2/5, 2/7, 1/4 |

with Ω_K = Γ(1/4)² / (2√(2π)) = 2.62205755... = Chowla-Selberg period for Q(i).

**v7.4 H7' candidate (primary):** L(f, m) · π^(4−m) / Ω_K⁴ = c/12 with m ∈ {1,2,3,4}
INTEGER (in Damerell algebraicity domain), parameter-free hits at (m=2, c=1) and
(m=3, c=1/2). Caveats: ladder (1/10, 1/12, 1/24, 1/60) suspiciously clean → must
verify in Hida 1980s / Katz 1976 CM L-values literature; c=7/10 (tricritique) and
c=4/5 (Potts) NOT cleanly hit.

## H7-B POSITIVE — Rankin-Selberg via Perlmutter 2025

Perlmutter (arXiv:2509.21672, Sep 2025) attaches a **degree-4 L-function** to every
2D CFT torus partition function — same degree as L(f⊗f, s) for f modular weight
k. For k=5, L(f⊗f, s) has critical INTEGERS at s ∈ {5, 6, 7, 8, 9}. Petersson
norm ⟨f, f⟩ algebraic up to π^(2k-1) = π⁹.

**v7.4 H7' candidate (backup):** ρ_Cardy = c/12 = r · L(f⊗f, m₀) / ⟨f, f⟩ with
m₀ critical integer of L(f⊗f) and r ∈ Q(i). Bridge to be invented; published
precedent only at degree-4 level (not specifically Cardy).

Other angles: Eichler-Shimura (#2, mathematically OK but bridge to invent),
Borcherds/automorphic (#3, speculative), Kohnen-Zagier (#4, REFUTED — same parity
obstruction as Damerell-CS for odd k=5).

## H7-C STRUCTURAL THEOREM + p-adic alternative

**Theorem (LYD20 §3, Tab:Level4_MM):** all hatted irreps of S'_4 carry ODD-weight
forms; even-weight forms go into UNHATTED multiplets. The Z/2 grading by weight
parity descends from the double-cover Γ(4) ⊂ Γ'(4) (generator R ~ −I acts as (−1)^k).

**Consequence:** NO even-weight CM-by-Q(i) form can substitute for 4.5.b.a in the
3̂_{,2}(5) embedding — structural obstruction, not enumerative. The odd-weight is
imposed by the hatted-multiplet requirement of S'_4.

**v7.4 H7' candidate (alternative — preserves s=k/2 central):**
Bertolini-Darmon-Prasanna 2013 (Duke Math J 162) anti-cyclotomic p-adic L-functions
DO handle CM-by-imag-quad forms at HALF-INTEGER central points. Replace Damerell
archimedean by p-adic anti-cyclotomic. KEEPS the original s=5/2 central point
(physically natural).

## Ranking + v7.4 axiomatic restart H7'

1. **H7-A primary** — most concrete, exact parameter-free hits, but verify Damerell
   ladder formula in Hida/Katz literature before publication
2. **H7-C secondary** — preserves s=k/2 central, BDP standard
3. **H7-B tertiary** — most novel via Perlmutter, bridge to invent

**Combined v7.4 H7'** = H7-A primary + H7-C as central-point complement.

## Hallucination report

- Counter held at 76 (no manuscript-level fabrications introduced).
- H7-B caught one web-search misattribution (1907.08149 actually Halyo, NOT
  Mukhametzhanov-Zhiboedov) and DROPPED the citation rather than fabricate.
- H7-C caught wrong LYD20 arXiv ID (1907.04299) in the prompt I provided —
  corrected to 2006.10722 (verified via arXiv API). Wrong ID was NOT in any
  manuscript file (PNT, V2, eci.bib, memory all use 2006.10722 correctly), so
  not a manuscript hallucination.

## Sources

- arXiv:2509.21672 — Perlmutter, "An L-function Approach to Two-Dimensional CFT"
  (verified via arXiv API)
- arXiv:1508.02728 — Shaghoulian, "Modular forms and a generalized Cardy formula
  in higher dimensions" (verified)
- arXiv:1003.2248 — Heim & Murase, Borcherds Lifts and Automorphic Green
  Functions (verified)
- arXiv:1206.1100 — Bringmann-Kane-Kohnen, Locally harmonic Maass forms (verified)
- arXiv:2006.10722 — Liu-Yao-Ding 2020, S'_4 modular flavor models (verified)
- LMFDB 4.5.b.a — q-expansion + L-value 0.5200744676 + Hecke eigenvalues
  (live-verified by H7-A; cached by H7-C due to reCAPTCHA)
- Damerell, Acta Arith. 17 (1971); Shimura, CPAM 29 (1976) — UNVERIFIED that
  the (1/10, 1/12, 1/24, 1/60) ladder appears verbatim; the numerical fit to
  Ω_K⁴ powers is what's solid

## Next step

Draft v7.4 axiomatic restart with H7' (combined H7-A + H7-C). Verify the
Damerell ladder against Hida 1980s and Katz 1976 standard CM L-value
references. Assess whether the (m=2, c=1) hit needs a separate proof or
follows from Damerell's binomial structure.
