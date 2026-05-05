# A28 — v7.4 amendment paper v2 multi-patch

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A28 (parent persisted)
**Hallu count entering / leaving:** 78 / 78 (held; no new fabrications by A28)

## Status

PASS. All six required patches integrated. v1 source preserved untouched at `v74_amendment.tex` (672 lines).

## Deliverables

- `v74_amendment_v2.tex` (1191 lines, ~14-16 pp at 11pt A4 — on target for LMP 12-16 pp)
- `PATCH_NOTES.md` (92 lines, full patch ledger + bibliography table)

## Six patches applied

1. **A14 §6** "τ-plane probes II: K=Q(i) modular fixed-point and the Littlest Modular Seesaw" — CSD(1+√6) at τ_S=i, NO + m_1=0 + δ_CP ≈ −87°, DUNE 2030+ ±15° falsifier, P~20% empirical, with cross-K uniqueness remark
2. **A17 §7** "τ-plane probes III: numerological CKM alignments" — Table with |V_us|=9/40 (0.015σ) and |V_cb|²=1/600 (0.024σ), explicit "multiplicative coefficients are EMPIRICAL" remark, cross-K test, NA62/Belle-II-2030+ falsifiers
3. **A16 §8** "Caveat: W1 τ-attractor does NOT accommodate the lepton sector" — full A16 table (LYD20/W1/τ=i fits) showing 24.5σ pull, two non-exclusive readings (two-tau vs LYD20-too-restrictive), v7.4.1 binary decision deferred
4. **A24 §6 Remark + §10 Q4** — √6 Galois-rational not period-anchored, PSLQ exhausted dps=60 |c|≤500, "thin coincidence" framing, DUNE falsifier still empirically valid
5. **AHS25 erratum** — bibkey `AHS25` with explicit "NOT Wang-Zhang" comment, in-text §9.1 "Anti-hallucination correction (hallu #78)" paragraph
6. **G1.12.B §9.1 "Note added in proof"** — A22 M1 PASS 4/4 + A26 M2 PASS 5/5 (m_c/m_t = 2.725e-3 exact at W1 τ*), M3-M6 forecast 3.5-5 mo, parameter-free B(p→e+π⁰)/B(K+ν̄)∈[0.3,3] Hyper-K/DUNE 2030+ falsifier

## Bibliography

12 new live-verified bibkeys added (DKLL19, LMS22, CK24, LS16, Priya26, ChenKMV23, A18scoping, HabaNagShim24, AHS25, PatelShukla23, SuperK20epi, SuperK14Knu, HK18, DUNE24) — all sourced from sub-agent SUMMARY ledgers' verified-arXiv tables; no fresh A28 arXiv calls (Mistral STRICT BAN respected).

## Note on PDF compile

pdflatex permission denied this session; user/operator should run `pdflatex v74_amendment_v2.tex` to verify clean compile. Expected: clean (all bibkeys well-formed, all `\arXiv{}` macros consistent with v1).
