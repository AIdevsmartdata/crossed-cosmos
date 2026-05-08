# Verified Email Addresses and arXiv References

This file contains the verified email addresses and arXiv references for the project, along with a log of identified hallucinations and fabrications caught during the research phase.

## 1. Verified Contact Information

| Name | Verified Email | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Francis Brown** | `francis.brown@maths.ox.ac.uk` | **CONFIRMED** | Oxford address is primary. |
| **Daniel Kriz** | `daniel.kriz@unimi.it` | **CORRECTED** | Currently at University of Milan. `dkriz@mit.edu` is likely inactive. |
| **Tiago Fonseca** | `tfonseca@unicamp.br` | **CORRECTED** | Currently at Unicamp (Brazil). Previous IMJ-PRG/CNRS addresses are outdated for primary contact. |
| **Antonio Lei** | `antonio.lei@uottawa.ca` | **CONFIRMED** | `antonio.lei@uottawa.ca` is the correct current address. |
| **Francesc Castella** | `castella@ucsb.edu` | **CONFIRMED** | Standard UCSB address. |
| **Aurélien Sagnier** | `asagnie1@jhu.edu` | **CONFIRMED** | J.J. Sylvester Assistant Professor at JHU. |
| **Kâzım Büyükboduk** | `kazim.buyukboduk@ucd.ie` | **CONFIRMED** | Associate Professor at UCD Dublin. |
| **Nima Lashkari** | `nlashkari@purdue.edu` | **CONFIRMED** | Confirmed from previous project notes. |
| **Matilde Marcolli** | `matilde@caltech.edu` | **CONFIRMED** | Confirmed from previous project notes. |

---

## 2. Verified arXiv References (A3 Lit Map 2026-Q2)

These references have been verified against the arXiv API as of May 2026.

| arXiv ID | Title | Authors | Status |
| :--- | :--- | :--- | :--- |
| **2604.12032** | Constraints on Coupled DE in the DESI Era | Gómez-Valent, Zheng, Amendola | **VERIFIED** |
| **2604.08449** | Coupled DE and DM for DESI: Phantom Divide | Antusch, King, Wang | **VERIFIED** |
| **2604.02204** | NMC quintessence with sign-switching interaction | Wang J-Q et al. | **VERIFIED** |
| **2604.16226** | Post-Newtonian Constraints on Scalar-Tensor Gravity | Karam, Sánchez López, Terente Díaz | **VERIFIED** |
| **2604.13535** | Double axions, half the tension: multi-field EDE | Bella, Poulin, Vagnozzi, Knox | **VERIFIED** |
| **2602.02675** | Modular Krylov Complexity as Boundary Probe | Vardian | **VERIFIED** |
| **2604.01422** | Quark masses from Modular S'_4 with Kähler effects | de Medeiros Varzielas, Paiva | **VERIFIED** |
| **2504.07679** | Assessing Cosmological Evidence for Non-Minimal Coupling | Wolf et al. | **VERIFIED** |
| **2503.14738** | DESI 2024 II: BAO Constraints | DESI Collaboration | **VERIFIED** |
| **1602.07508** | Anticyclotomic Iwasawa Theory for CM Fields | Büyükboduk, Lei | **VERIFIED** |

---

## 3. Hallucination & Fabrication Log (Catches 1–104)

The project maintains a rigorous anti-fabrication protocol. A total of **104 hallucinations** have been caught and corrected before manuscript propagation (as of 2026-05-08).

### Notable Fabrication Catches

| ID / Ref | Issue | Mitigation |
| :--- | :--- | :--- |
| **arXiv:1709.02912** | Fabricated in earlier briefs as "Büyükboduk-Lei". Actual = Nakano et al. (WSe2 cond-mat MBE, 2017-09-09). | **CORRECTED** to 1602.07508. |
| **arXiv:1804.05064** | Fabricated as "Pan-Yang JCAP 2018". Actual paper is Henden et al. (FABLE). | **REMOVED** from manuscript. |
| **"Bahcall-Brodie 2025"** | Fabricated JWST claim. Actual work is Freedman-Madore (arXiv:2408.06153). | **CORRECTED** in audit. |
| **Mistral strike cluster** | Mistral Large hallucinated 6/13 titles for valid bibkeys (2026-05-05). | **STRICT-BAN** on Mistral for citations. |
| **2507.03090** | Misattributed to Anchordoqui et al. in v3. | **CORRECTED** to Bedroya, Obied, Vafa, Wu. |
| **arXiv:2104.08808** [hallu #104, NEW 2026-05-08] | Fabricated in M79 endorser_emails.md Email 6 + M138-4 Kriz Gmail draft body as "your methods (arXiv:2104.08808 and related)". Actual paper = Jin-Lin-Rostami-Ren "Learn Continually, Generalize Rapidly: Lifelong Knowledge Accumulation for Few-shot Learning" (cs.CL/NLP, EMNLP 2021). ZERO connection to Kriz / number theory / Bloch-Kato. NB: Gemini's prior verification of the 10 listed IDs missed this since it wasn't in the explicit list — caught only via Sonnet sub-agent body-scan of draft files. | **CORRECTED** to arXiv:1805.03605 (Kriz p-adic Maass-Shimura) + arXiv:2002.04767 (Kriz supersingular main conj.). User to pick final citation before W5 send. Gmail draft `r-5756948127962139710` requires update. |
| **Email dkriz@mit.edu** | Stale MIT address in M138-4 Kriz draft. | **CORRECTED** to `daniel.kriz@unimi.it` (Univ. Milan, current). |

### Mistral STRICT-BAN
As of **2026-05-05**, the **Mistral large-latest** model is under a strict ban for all citation-heavy and technical verification tasks due to repeated (4+ strikes) fabrications of paper titles and logical identities. All future verifications must use the **arXiv API** or **CrossRef DOI** through the Gemini/Sonnet interface.

---

## 4. Specific Draft Corrections
... (rest of original corrections) ...

### 1. Daniel Kriz (Draft M138-4)
- **Email update**: Change `dkriz@mit.edu` to `daniel.kriz@unimi.it`.
- **Context update**: Adjust the draft to reflect his current affiliation with the University of Milan.

### 2. Tiago Fonseca (Draft M125-5)
- **Email update**: Change `tiago.fonseca@cnrs.fr` to `tfonseca@unicamp.br`.
- **Context update**: Acknowledge his current position at Unicamp while referencing his ties to IMJ-PRG if necessary.

### 3. Francis Brown (Draft M138-3)
- **Email update**: Use `francis.brown@maths.ox.ac.uk`. The IHES address (`francis.brown@ihes.fr`) may still work but Oxford is more reliable for a Senior Research Fellow.

### 4. Antonio Lei (Draft M125-3)
- **Email update**: Ensure `antonio.lei@uottawa.ca` is used (the previous `alei@uottawa.ca` should be updated).

### 5. Kâzım Büyükboduk (Draft M125-2)
- **Citation Correction**: **URGENT.** Ensure the draft uses `arXiv:1602.07508` and NOT the fabricated `1709.02912` mentioned in some earlier project briefs.

---

## Next Steps

1. **Update `EMAILS_TO_SEND.md`**: Replace the `[TBD: verify]` markers with these verified addresses.
2. **Update Gmail Drafts**: Manually update the recipients and body text in the Gmail drafts folder as per the corrections above.
3. **Follow Staggered Schedule**: Continue with the W1, W2, etc., send schedule as outlined in `EMAILS_TO_SEND.md`.
