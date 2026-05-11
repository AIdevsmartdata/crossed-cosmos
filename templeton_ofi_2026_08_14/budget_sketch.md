---
name: Budget sketch — ECI portfolio grant application
description: ~$220K 18-month budget for independent researcher programme. Updated with specialist consultation honoraria (Kings/Sprang, Fonseca, Castella, Lei, Sagnier), conference travel, and honest compute profile.
type: document
---

# Budget Sketch — ECI Portfolio Grant Application (18 months)

**Applicant**: Kevin Remondière, Independent Researcher, Tarbes, France  
**Programme duration**: 18 months (Phase 1–3)  
**Total requested**: ~$218,000 USD  
**Currency note**: Amounts in USD; for ANR JCJC applications, convert to EUR at prevailing rate (~0.92, ~€200K)

---

## Summary Table

| Category | Amount (USD) | % Total |
|---|---|---|
| Researcher living stipend | $90,000 | 41% |
| Specialist consultation honoraria | $36,000 | 16.5% |
| Conference travel (2–3 papers) | $24,000 | 11% |
| Computational infrastructure | $18,000 | 8.2% |
| Open-access publication fees (APCs) | $12,000 | 5.5% |
| Administrative / institutional overhead | $18,000 | 8.2% |
| Contingency (10%) | $20,000 | 9.2% |
| **TOTAL** | **$218,000** | **100%** |

---

## Line-item Justifications

### 1. Researcher Living Stipend — $90,000 (18 months)

**$5,000/month × 18 months = $90,000**

France cost-of-living basis (Tarbes, Hautes-Pyrénées): rent ~€700-900/month in Tarbes, significantly below Paris/Lyon rates. This stipend covers:
- Living expenses (rent, food, utilities, health insurance)
- Home office infrastructure (internet, UPS for VPS work)
- Standard equipment maintenance (laptop, peripherals)

*Rationale*: French CNRS chargé de recherche CR2 entry-level net salary is ~€2,300/month (2026). The stipend of ~€4,600/month (at €1 = $1.10) reflects the premium appropriate for an independent researcher without institutional benefits (no health insurance subsidy, no pension contribution, no IT/library support). This is below standard French DR-level salary (~€5,500/month net equivalent) and comparable to an experienced postdoc salary at a French university.

*Grant institution note*: For grants requiring an institutional host (JTF, ANR), this line becomes salary disbursed via CNRS/Université Paul Sabatier/IHES. For FQXi (no affiliation required), disbursed directly to researcher.

---

### 2. Specialist Consultation Honoraria — $36,000

These are paid consultation agreements with domain specialists for specific technical questions that can be resolved in 1–4 weeks. NOT co-authorship fees — rather, paid advisory hours with deliverable (written technical opinion, computation, or literature pointer).

| Specialist | Institution | Topic | Hours | Rate | Total |
|---|---|---|---|---|---|
| Guido Kings or Johannes Sprang | Regensburg/Mainz | e*_{2,2} Eisenstein-Kronecker Laurent coefficient for Z[i]; α₂ = 1/12 closure (M116) | 15 hr | $400/hr | $6,000 |
| Tiago Fonseca | U. Vienna / Brown-Fonseca | (B1) μ₆ stratum Γ₁(4) level verification (M113) | 20 hr | $400/hr | $8,000 |
| Francesc Castella | UC Santa Barbara | Fan-Wan ± extension for ∞-type (k-1,0) odd k, p=2 ramified (M119-Q1) | 25 hr | $400/hr | $10,000 |
| Antonio Lei | Université Laval | Same M119-Q1 question from Lei's side; ± Wach module for higher-weight CM | 15 hr | $400/hr | $6,000 |
| Loïc Merel or Aurel Page (Sagnier group) | Paris-Cité / Bordeaux | R-3 Geometric Langlands / polylogarithm implications of 6/5 | 15 hr | $400/hr | $6,000 |

**Total: $36,000**

*Rationale*: Hourly rates of $400/hr are standard for paid mathematical consulting (comparable to NSF supplementary consulting rates and legal expert witness rates in mathematics). Each specialist is asked a sharply-defined technical question (see M116, M113, M119 summaries) with expected resolution time 3-25 hours. These are not requests for letters of support (those are voluntary) but paid technical consultations.

*Note*: These honoraria are offered *after* the programme has enough preliminary results to make the question well-posed. None of the outreach should occur before P-NT and R-6 are posted to arXiv.

---

### 3. Conference Travel — $24,000

Targeting 2-3 conference presentations for the most significant results:

| Conference | Target date | Papers to present | Budget |
|---|---|---|---|
| Modular Symmetry Workshop (European) | Q2 2027 | P-NT uniqueness + R-6 lemniscate | $4,000 |
| Number Theory Conference (ANR/GDR) | Q3 2026 | R-6 Galois descent results (M108) | $3,000 |
| Strings 2027 or PASCOS 2027 | Q3 2027 | P-KS proton-decay prediction; Hyper-K coordination | $5,000 |
| IHES/IHP workshop visit (3× short) | Rolling 2026-2027 | ECI v8 synthesis discussions | $6,000 |
| Satellite visit: Oxford (Schäfer-Nameki) | Q4 2026 | SymTFT conditional paper scoping | $3,000 |
| Innsbruck (Nägerl group, BEC/Cardy) | Q1 2027 | Cardy ρ = 1/18 experimental prediction | $3,000 |

**Total: $24,000**

*Note*: These are estimated at economy airfare + budget accommodation. Tarbes → Paris TGV (~€100) is baseline for French conferences. Tarbes → Oxford via Paris (€200-400 economy), Tarbes → Innsbruck (~€300 economy), Tarbes → US conference (~€700-900). Budget is conservative.

---

### 4. Computational Infrastructure — $18,000

| Item | Amount | Justification |
|---|---|---|
| Cloud GPU (Vast.ai): MCMC production runs | $8,000 | C4 v6 production MCMC for ECI ξ=0.001 cosmological constraint (A57 spec); ECI-only cosmopower-jax emulator; ~$500/run × 16 runs |
| Cloud CPU: PARI/GP large-scale verification | $3,000 | Extended lemniscate period computations, 9-field 80-digit verification at higher precision, M95/M97 follow-up |
| VPS renewal (Hostinger): 18 months | $2,000 | Primary workspace; primary compute for symbolic algebra |
| Storage, backup, Zenodo archiving | $1,000 | Versioned snapshots every major milestone |
| Software licenses / subscriptions | $2,000 | Overleaf, Mathematica/SageMath cloud, specialized numerics |
| Hardware contingency (RTX 5060 Ti replacement/upgrade) | $2,000 | Current machine operational; contingency for hardware failure |

**Total: $18,000**

*Note*: Local RTX 5060 Ti (386 cosmopower-jax pred/sec with JAX 0.10 patch) handles most cosmological work. Cloud GPU is for extended production runs only. Compute is modest by physics standards — the programme is primarily mathematical.

---

### 5. Open-Access Publication Fees (APCs) — $12,000

| Venue | Papers | APC estimate | Total |
|---|---|---|---|
| Bull. London Math. Soc. (Gold OA) | P-NT | $2,500 | $2,500 |
| Phys. Rev. D (APS) | P-KS | $3,000 | $3,000 |
| Letters in Mathematical Physics (Springer) | 3 papers (LMP) | $2,500 ea | $7,500 |
| J. Phys. A | Cardy/BEC | $1,500 | $1,500 |
| Zenodo archiving (open) | All versions | $0 | $0 |
| arXiv preprint (open) | All | $0 | $0 |

**Total: ~$12,000** (some papers may qualify for waiver via CNRS/institution affiliation)

*Note*: If institutional affiliation (CNRS associate status) is obtained before paper submission, APC costs may be substantially reduced via institutional agreements. This budget assumes no such reduction as a conservative baseline.

---

### 6. Administrative / Institutional Overhead — $18,000

- Institutional overhead (if hosted by CNRS/UPS Toulouse/IHES): standard 15-20% on direct costs excluding stipend = ~$15,000 of overhead
- Legal/accounting for independent research status (auto-entrepreneur France): ~$500/year × 1.5 = $750
- Translation/editing assistance (one paper may require professional English editing): $1,500
- Research library access (HAL/Jstor subscriptions for paywall PDFs): $750

**Total: $18,000**

---

### 7. Contingency — $20,000

10% of total direct costs as contingency for:
- Unexpected conference invitations
- Specialist consultation overruns
- Hardware failure
- Additional arXiv revisions requiring compute

---

## Comparison to Standard Academic Funding

For reference:
- **ANR JCJC** typical range: €250,000–350,000 over 4 years. The proposed budget of ~€200,000 over 18 months is higher per-month but covers a focused sprint to 9 paper submissions with specialist outreach — not a 4-year exploratory programme.
- **FQXi Zenith Grant** typical range: $31,000–$1.8M (wide). The $218K request is in the mid range, comparable to ~$150K FQXi mid-tier grants.
- **JTF OFI** range: $10K–$300K. At $218K this is near the top of the range; a first application might target $150K with the remaining $70K covered by a second-stage supplementary grant or ANR.

---

## Cost-Reduction Scenario (FQXi first application: $150K)

If submitting to FQXi with $150K cap:
- Reduce researcher stipend to $60K (12 months at $5K/month)
- Reduce specialist honoraria to $20K (focus on Kings/Sprang + Fonseca)
- Reduce conference travel to $15K (2 conferences)
- Compute: unchanged at $12K
- APCs: $10K
- Overhead: $12K
- Contingency: $11K
- **Reduced total: ~$140K** (fits comfortably in $150K range)

The reduced scenario still covers the programme's critical path: P-NT submission, R-6 upgrade with M108+M114+M116, and M113 specialist consultation.

---

*Prepared: 2026-05-06 | Hallu count: 97 | Budget line items estimated from public rates; verify salary rates with actual French regulatory guidance before submission | Mistral STRICT-BAN*
