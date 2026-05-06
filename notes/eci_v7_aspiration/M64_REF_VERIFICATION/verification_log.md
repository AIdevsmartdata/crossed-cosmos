---
name: M64 verification log
description: Per-ref API query log for M64 reference verification mission
type: log
date: 2026-05-06
---

# M64 Verification Log

## Tool methodology

- CrossRef REST API: curl https://api.crossref.org/works?query=...
- CrossRef DOI direct: curl https://api.crossref.org/works/DOI
- Semantic Scholar Graph API: /graph/v1/paper/DOI:...
- arXiv export HTML: curl https://export.arxiv.org/abs/ARXIVID
- Annals of Math DOI scan: 10.4007/annals.YEAR.VOL.ISSUE.ART pattern enumeration

---

## REF 1: Chowla-Selberg 1967

**Query:** CrossRef ?query=Epstein+zeta+function+Chowla+Selberg&filter=from-pub-date:1966,until-pub-date:1968  
**Hit rank 2 in results:**

```
DOI: 10.1515/crll.1967.227.86
Title: "On Epstein's Zeta-function."
Publisher: Walter de Gruyter GmbH
Issue: 227
Container: Journal fur die reine und angewandte Mathematik (Crelles Journal)
Published: 1967-07-01
Pages: 86-110
Volume: 1967
is-referenced-by-count: 37
```

**Author check:** CrossRef record has no author field. Semantic Scholar query DOI:10.1515/crll.1967.227.86 returns:
```
authors: [{"name": "A. Selberg"}, {"name": "S. Chowla"}]
```

**Verdict: CONFIRMED.** DOI 10.1515/crll.1967.227.86. Pages 86-110 exact match.

---

## REF 2: Damerell 1970

**Query:** CrossRef ?query=L-functions+elliptic+curves+complex+multiplication+Damerell&filter=1969-1972  
**Top hit:**

```
DOI: 10.4064/aa-17-3-287-301
Title: "L-functions of elliptic curves with complex multiplication, I"
Author: R. Damerell
Journal: Acta Arithmetica
Volume: 17, Issue 3
Pages: 287-301
Year: 1970
is-referenced-by-count: 37
```

**Verdict: CONFIRMED.** Exact journal/volume/pages match.

---

## REF 3: Damerell 1971

**Query:** Same CrossRef query as REF 2. Top hit:

```
DOI: 10.4064/aa-19-3-311-317
Title: "L-functions of elliptic curves with complex multiplication, II"
Author: R. Damerell
Journal: Acta Arithmetica
Volume: 19, Issue 3
Pages: 311-317
Year: 1971
is-referenced-by-count: 16
```

**Cross-check:** Shimura 1976 (DOI 10.1002/cpa.3160290618) cites both Damerell I and II in its reference list with DOIs 10.4064/aa-17-3-287-301 and 10.4064/aa-19-3-311-317 — independently confirms both.

**Verdict: CONFIRMED.** Exact journal/volume/pages match.

---

## REF 4: Shimura 1976

**Query:** CrossRef ?query=special+values+zeta+functions+cusp+forms+Shimura&filter=1975-1977  
**Top hit:**

```
DOI: 10.1002/cpa.3160290618
Title: "The special values of the zeta functions associated with cusp forms"
Author: Goro Shimura
Journal: Communications on Pure and Applied Mathematics
Volume: 29, Issue 6
Pages: 783-804
Published: 1976-11
is-referenced-by-count: 221
Received: 1976-06-01
```

**Verdict: CONFIRMED.** Exact title, journal, volume, pages match.

---

## REF 5: Katz 1976

**Query:** CrossRef ?query=p-adic+interpolation+real+analytic+Eisenstein+series+Katz&filter=1975-1977  
**Top hit:**

```
DOI: 10.2307/1970966
Title: "p-adic Interpolation of Real Analytic Eisenstein Series"
Author: Nicholas M. Katz
Journal: The Annals of Mathematics
Volume: 104, Issue 3
Start page: 459
Year: 1976-11
is-referenced-by-count: 114
```

**Pages 459-571:** CrossRef record shows page "459" only (JSTOR deposit often omits end page). Cross-reference: Koblitz (1977) book chapter DOI 10.1007/978-1-4684-0047-2_2 explicitly cites "Ann. of Math., 104 (1976), 459–571."

**Verdict: CONFIRMED.** DOI 10.2307/1970966, Annals Math. 104 (1976), pages 459-571.

---

## REF 6: CHHN II (arXiv:2009.07224)

**Query:** CrossRef ?query=Hermitian+K-theory+stable+categories+II+Cobordism+Calmes  
**Top hit:**

```
DOI: 10.4310/acta.2025.n235.n2.a1
Title: "Hermitian K-theory for stable infty-categories II: Cobordism categories and additivity"
Authors: Calmes, Dotto, Harpaz, Hebestreit, Land, Moi, Nardin, Nikolaus, Steimle (9 authors)
Journal: Acta Mathematica
Volume: 235, Issue 2
Pages: 149-400
Year: 2025
```

**arXiv:2009.07224 v5 comment:** "149 pages. v5: major revision following an editorial request."

**Verdict: CONFIRMED.** M49 B4 "Acta Math. 235:2 (2025)" claim is CORRECT.

---

## REF 7: CHHN III (arXiv:2009.07225)

**arXiv:2009.07225 comments field:** "63 pages v2: updated references; to appear in Annals of Mathematics"  
**arXiv last revision:** April 27 2026

**CrossRef scan for published DOI:**
- Searched CrossRef with: Hermitian K-theory stable infinity-categories III Grothendieck-Witt groups rings Calmes Dotto — NO match found for Annals of Mathematics.
- Direct DOI enumeration of 10.4007/annals.YEAR.VOL.ISSUE.ART: scanned all accessible articles in Annals vols 202 (2025, issues 1-3) and 203 (2026, issues 1-3). CHHN III not found in any CrossRef-indexed article.

**Conclusion:** Paper accepted in Annals (per author annotation), specific vol/issue/pages not yet indexed by CrossRef as of 2026-05-06. Likely forthcoming in 2026 (given April 2026 revision for editorial requirements).

**Verdict: PARTIALLY CONFIRMED.** Acceptance confirmed via arXiv metadata. Publication vol/issue/pages: NOT YET AVAILABLE.

---

## REF 8: Buyukboduk-Neamti arXiv:2604.13854

**arXiv HTML metadata verified:**
- Title: "A proof of p-adic Gross-Zagier theorem via BDP formula"
- Authors: Kazim Buyukboduk, Peter Neamti
- Submitted: 2026-04-15, 34 pages
- MSC: Primary 11G40, Secondary 11G18, 11F67, 11R23, 11F33
- No journal-ref field yet (preprint)

**Abstract text (full):**
"This paper provides a new proof of the p-adic Gross-Zagier formula for the p-adic L-function associated with the base change of a normalised cuspidal eigen-newform f of weight k >= 2 (and families of such) to an imaginary quadratic field K. Our results encompass both the classical p-ordinary cases and non-ordinary scenarios, including new cases where k > 2 and ord_p(a_p(f)) > 0. Unlike the traditional approach of comparing geometric and analytic kernels, we employ a wall-crossing strategy centred on the BDP formula and the theory of Beilinson-Flach elements."

**K=Q(i) restriction check:** The abstract applies to general imaginary quadratic field K. No "K=Q(i)" or "K≠Q(i)" restriction appears. The abstract is more general than Q(i).

**Verdict:** arXiv:2604.13854 EXISTS and authors are confirmed CORRECT. K=Q(i)-exclusion claim is NOT CONFIRMED FROM ABSTRACT. If prior ECI session noted "K≠Q(i) explicit in abstract," this was incorrect; only a full PDF §1 read can determine whether this restriction appears in the body of the paper.

---

## REF 9: Loualidi-Miskaoui-Nasri arXiv:2503.12594

**CrossRef query:** ?query=Nonholomorphic+A4+modular+invariance+fermion+masses+SU5+GUT+Loualidi  
**Top hit:**

```
DOI: 10.1103/1py2-cmfx
Title: "Nonholomorphic A_4 modular invariance for fermion masses and mixing in SU(5) GUT"
Authors: Mohamed Amin Loualidi, Mohamed Miskaoui, Salah Nasri
Journal: Physical Review D
Volume: 112, Issue 1
Article number: 015008
Year: 2025-07-09
```

**arXiv metadata (WebFetch):**
- arXiv:2503.12594, submitted March 16 2025 (v2 revised Aug 4 2025)
- 27 pages, 5 figures, CC BY 4.0

**Verdict: CONFIRMED.** Title, all three authors, PRD 112 (2025) 015008 exact match. M59 attribution correction is correct.

---

## Summary statistics

| Category | Count |
|---|---|
| CONFIRMED with DOI | 7 |
| PARTIALLY CONFIRMED (acceptance confirmed, DOI not yet indexed) | 1 |
| UNCONFIRMED (K restriction claim not verified from abstract) | 1 |
| Fabricated DOIs introduced by M64 | 0 |

Hallu 91 → 91 (held).
