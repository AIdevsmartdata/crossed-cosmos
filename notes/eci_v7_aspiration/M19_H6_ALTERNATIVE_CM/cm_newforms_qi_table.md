# CM-by-Q(i) Newforms: Full LMFDB List
**Sub-agent M19 — Phase 3.C-early**
**Date:** 2026-05-06
**Source:** LMFDB live-fetch (self_twist_discs=-4, weight 2–10, level 1–200)
**Total found:** 187 forms within those bounds

---

## Methodology

Live LMFDB query:
```
https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/?self_twist_discs=-4&search_type=List&count=100&weight=2-10&level=1-200
```
(two pages, 187 total). All CM disc = -4 forms verified by LMFDB's self-twist field.

---

## Dim = 1 forms (eligible for Damerell ladder analysis)

These are the algebraically simplest — Hecke eigenvalues are rational integers. The Damerell ladder computation requires a single eigenform.

### Weight 2, dim=1
| Label | N | k | char | notes |
|-------|---|---|------|-------|
| 32.2.a.a | 32 | 2 | 32.a | trivial char; eta = η(4z)²η(8z)² |
| 64.2.a.a | 64 | 2 | 64.a | non-minimal twist |

### Weight 3, dim=1
| Label | N | k | char | twist-minimal? |
|-------|---|---|------|----------------|
| 16.3.c.a | 16 | 3 | 16.c | YES (eta = η(4z)⁶) |
| 36.3.d.a | 36 | 3 | 36.d | YES |
| 36.3.d.b | 36 | 3 | 36.d | YES |
| 64.3.c.a | 64 | 3 | 64.c | no (min twist = 16.3.c.a) |
| 100.3.b.a | 100 | 3 | 100.b | — |
| 100.3.b.b | 100 | 3 | 100.b | — |
| 144.3.g.a | 144 | 3 | 144.g | — |

### Weight 4, dim=1
| Label | N | k | char | twist-minimal? |
|-------|---|---|------|----------------|
| 32.4.a.b | 32 | 4 | 32.a | YES (trivial char) |
| 64.4.a.c | 64 | 4 | 64.a | — |

### Weight 5, dim=1 (KEY WEIGHT — same as 4.5.b.a)
| Label | N | k | char | twist-minimal? | min-twist |
|-------|---|---|------|----------------|-----------|
| **4.5.b.a** | 4 | 5 | 4.b | **YES** | — (is minimal) |
| 36.5.d.a | 36 | 5 | 36.d | no | 4.5.b.a |
| 64.5.c.a | 64 | 5 | 64.c | no | 4.5.b.a |
| 100.5.b.a | 100 | 5 | 100.b | no | 4.5.b.a |
| **144.5.g.a** | 144 | 5 | 144.g | **YES** | — (is minimal) |
| **144.5.g.b** | 144 | 5 | 144.g | **YES** | — (is minimal) |
| 196.5.c.a | 196 | 5 | 196.c | no | 4.5.b.a |
| 196.5.c.b | 196 | 5 | 196.c | — | — |
| 196.5.c.c | 196 | 5 | 196.c | — | — |

**Critical:** 144.5.g.a and 144.5.g.b are LMFDB-confirmed twist-minimal and do NOT appear in 4.5.b.a's twist table (which ends at level 576.5.g.b via character 24.f). Their |a_p| values differ from 4.5.b.a at all primes (|a_29|=1680 vs. 82), confirming genuine Hecke-character independence.

### Weight 7, dim=1
| Label | N | k | char | twist-minimal? |
|-------|---|---|------|----------------|
| 16.7.c.a | 16 | 7 | 16.c | YES |
| 64.7.c.a | 64 | 7 | 64.c | — |
| 36.7.d.a | 36 | 7 | 36.d | YES |
| 36.7.d.b | 36 | 7 | 36.d | YES |
| 144.7.g.a | 144 | 7 | 144.g | — |
| 100.7.b.a | 100 | 7 | 100.b | — |
| 100.7.b.b | 100 | 7 | 100.b | — |

### Weight 9, dim=1
| Label | N | k | char | twist-minimal? |
|-------|---|---|------|----------------|
| **4.9.b.a** | 4 | 9 | 4.b | YES |
| 36.9.d.a | 36 | 9 | 36.d | YES |
| 144.9.g.a | 144 | 9 | 144.g | — |
| 144.9.g.b | 144 | 9 | 144.g | — |
| 100.9.b.a | 100 | 9 | 100.b | — |

---

## Dim > 1 forms (sample)

These are not amenable to the direct Damerell ladder (eigenvalues in number fields). Listed for completeness only; not pursued in M19 stress-test.

| Label | N | k | dim | notes |
|-------|---|---|-----|-------|
| 20.2.e.a | 20 | 2 | 2 | — |
| 52.2.f.a | 52 | 2 | 2 | — |
| 52.2.l.a | 52 | 2 | 4 | — |
| 68.2.i.a | 68 | 2 | 8 | — |
| 52.5.j.a | 52 | 5 | 4 | twist-minimal, char order 6 |
| 100.5.d.a | 100 | 5 | 2 | twist of 4.5.b.a via quartic char |
| 116.5.j.a | 116 | 5 | 12 | — |
| 148.5.i.a | 148 | 5 | 4 | — |
| 148.5.p.a | 148 | 5 | 12 | — |

---

## Key structural note

The LMFDB's CM disc = -4 filter at weight 5, level ≤ 200 yields exactly **two** twist-minimal dim=1 families:
1. **Family I:** 4.5.b.a (level 4) with twist class covering 36.5.d.a, 64.5.c.a, 100.5.b.a, 196.5.c.a...
2. **Family II:** 144.5.g.a / 144.5.g.b (level 144) — a distinct Hecke Grössencharacter family

This is the central finding of M19. The 3-filter analysis of A78 must be extended to Family II.
