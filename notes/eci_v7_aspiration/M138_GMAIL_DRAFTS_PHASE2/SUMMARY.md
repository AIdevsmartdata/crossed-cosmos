---
name: M138 Gmail Drafts Phase 2 — 4 outreach emails (Lashkari, Marcolli, Brown, Kriz)
description: 4 Gmail drafts created 2026-05-06. WebFetch blocked — Brown and Kriz addresses unverified [TBD]. Hallu 98 held.
type: project
---

# M138 — Gmail Drafts Phase 2 (2026-05-06)

**Hallu count: 98 held** | **Mistral STRICT-BAN observed** | **WebFetch: BLOCKED (permission denied)**

## Summary table

| # | Recipient | Email used | Draft ID | Words | Addr verified | Send gate |
|---|---|---|---|---|---|---|
| 1 | Nima Lashkari (Purdue) | nlashkari@purdue.edu | `r6651936878748037327` | ~160 | YES (M79 source) | READY W3 (stagger 2-3 wk after Booker) |
| 2 | Matilde Marcolli (Caltech) | matilde@caltech.edu | `r-3141832382031850011` | ~175 | YES (M79+M101) | READY after P1+P2 confirmed |
| 3 | Francis Brown (Oxford) | francis.brown@maths.ox.ac.uk | `r-796492079938292922` | ~150 | [TBD: verify] | READY once address confirmed |
| 4 | Daniel Kriz (MIT) | dkriz@mit.edu | `r-5756948127962139710` | ~185 | [TBD: verify] | DRAFT_GATED W5 (R-2 finalized) |

---

## Draft M138-1: Nima Lashkari (Purdue) — hep-th endorsement

- **Gmail ID**: `r6651936878748037327`
- **To**: nlashkari@purdue.edu
- **Subject**: arXiv hep-th endorsement — Araki-cocycle derivation of S_gen + modular shadow
- **Address**: CONFIRMED — listed in M79 endorser_emails.md Email 4
- **Word count**: ~160
- **Content**: Araki cocycle + Pusz-Woronowicz derivation of d/dt S_gen = <K_R>; no-go for Stinespring/DEHK; companion 19-page type-II_inf cosmology paper; second endorsement staggered 2-3 weeks.
- **Send gate**: READY W3 — send 2-3 weeks after Booker (W1)

---

## Draft M138-2: Matilde Marcolli (Caltech) — Bianchi IX

- **Gmail ID**: `r-3141832382031850011`
- **To**: matilde@caltech.edu
- **Subject**: Bianchi IX BKL x type-II_inf modular shadow — follow-up to your 2015 papers
- **Address**: CONFIRMED — M79 Email 5 + M101 SUMMARY
- **Word count**: ~175
- **M101 updates integrated**:
  - F1 lambda_BKL: h_KS = pi^2/(6 log 2) ~ 2.3731 verified to 1e-3 (Birkhoff, 10^6 Gauss-shift trajectories, Lochs-Khinchin confirmed)
  - M78 section 4.1: type-III_1 classification sketch of wedge algebra in 15-page draft
  - CMP target stated; six [TBD: prove] markers acknowledged
- **Send gate**: READY — M101 verdict: gate MET after P1 (lambda_BKL Python run) + P2 (M78 merge into M45 stub). Kevin must confirm P1+P2 done.

---

## Draft M138-3: Francis Brown (Oxford/IHES) — single-valued periods

- **Gmail ID**: `r-796492079938292922`
- **To**: francis.brown@maths.ox.ac.uk [TBD: VERIFY]
- **Subject**: Single-valued periods at weight 5, level 4, CM Q(i) — pi*L(f,1)/L(f,2) = 6/5
- **Address**: [TBD] — WebFetch BLOCKED. Candidate from M89 pattern. Verify at https://people.maths.ox.ac.uk/brownf/ or All Souls staff page. Alternative: francis.brown@ihes.fr
- **Word count**: ~150
- **M113/M129 updates integrated**:
  - Conditional theorem M113: (B1) [integral Cho12 Lemma 3.1 at p=3] + (B2) [conservativity for S_4(Gamma_1(4))=0] => M(M-bar_{1,3}^{Gamma_1(4)}) mixed Tate over Z[i,1/2]
  - BF25 section 10.5.2 "arguments go through" cited as green-light (NOT proof of integral lift — per M129 correction)
  - Pet12 Rem 6.4 explicit reference; direct specialist question to Brown
  - Address warning in draft body (visible on Kevin's review)
- **Send gate**: READY once address verified

---

## Draft M138-4: Daniel Kriz (MIT) — Bloch-Kato Tamagawa (GATED)

- **Gmail ID**: `r-5756948127962139710`
- **To**: dkriz@mit.edu [TBD: VERIFY]
- **Subject**: Bloch-Kato Tamagawa for 4.5.b.a — collaboration inquiry (Omega-independent 6/5 ratio)
- **Address**: [TBD] — WebFetch BLOCKED. Standard MIT pattern but NOT confirmed. Verify at https://math.mit.edu/people
- **Word count**: ~185
- **Content**: 80-digit PARI/GP + SageMath verification of pi*L(f,1)/L(f,2) = 6/5 for 4.5.b.a; uniqueness among d in {1,3,7,11}; three conjectures R-2.1/R-2.2/R-2.3; complete p=2 obstruction documented; collaboration ask (not endorsement).
- **DRAFT_GATED W5**: Gate notice in draft body. DO NOT SEND until R-2 finalized + address verified.

---

## Address verification action items

| Recipient | Address | Action required |
|---|---|---|
| Lashkari | nlashkari@purdue.edu | None — confirmed |
| Marcolli | matilde@caltech.edu | None — confirmed |
| Brown | francis.brown@maths.ox.ac.uk | Check https://people.maths.ox.ac.uk/brownf/ or All Souls; update draft if different |
| Kriz | dkriz@mit.edu | Check https://math.mit.edu/people; update draft if different |

---

## Pre-send checklist

1. **Lashkari** (r6651936878748037327): Review OK. Send at W3.
2. **Marcolli** (r-3141832382031850011): Confirm P1 (VPS Python lambda_BKL run) + P2 (M78 s4_1 merge) done, then send.
3. **Brown** (r-796492079938292922): Verify email address; update draft To: if needed; then send.
4. **Kriz** (r-5756948127962139710): GATE W5. Do NOT send until R-2 ready. Verify address first.

---

## Discipline log

- Hallu 98 held — M138 0 fabrications
- Mistral STRICT-BAN observed
- WebFetch permission denied — 2 addresses flagged [TBD]
- All drafts: "numerically verified" not "proven"; [TBD: prove] markers preserved
- Kriz: DRAFT_GATED W5 in both body and summary
- Brown: M113 conditional theorem accurate per M129 correction (B1.alpha + B1.beta sub-claims)
- Marcolli: F1 lambda_BKL 1e-3 + M78 s4.1 type-III_1 sketch included
- Sign-off: "With respect and gratitude, Kevin Remondiere, kevin.remondiere@gmail.com"
