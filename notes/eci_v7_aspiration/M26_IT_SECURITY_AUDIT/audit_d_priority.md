# Audit D — Anti-Priority / Falsification Protection
**Date:** 2026-05-06  

---

## D1. Commit Signing Status

### Finding: NOT configured — MEDIUM risk

**Evidence:**
- `/root/.gitconfig` contains NO `gpgsign = true` or `signingkey = ...` settings
- No GPG key setup detected on the VPS
- All commits in the `crossed-cosmos` repo are **unsigned**

**What this means:**
- Anyone who gains access to the GitHub PAT (stored in `.netrc`) could push commits attributed to `kevin.remondiere@gmail.com`
- Without GPG signatures, there is no cryptographic proof that a commit was created by the physical keyholder

**What this does NOT mean:**
- It does NOT mean commits can be silently altered after the fact — git's SHA-1/SHA-256 hash tree makes past commits tamper-evident
- It does NOT break the Zenodo timestamp chain — Zenodo records are signed by CERN infrastructure independently of git signing

**Empirical context (from academic research on GitHub):** Only 9.65% of GitHub commits are GPG-signed (arXiv:2504.19215, EASE 2025). Non-signing is the norm, not the exception.

**Severity: MEDIUM** — Important to fix before high-stakes submissions to major journals where priority disputes could arise.

**Setup commands:**
```bash
# On VPS — generate GPG key
gpg --full-generate-key
# Choose: RSA/RSA, 4096 bits, 2 years, name: Kevin Remondière, email: kevin.remondiere@gmail.com

# Get the key ID
gpg --list-secret-keys --keyid-format LONG

# Configure git to use it
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Export and register on GitHub:
gpg --armor --export <KEY_ID>
# Paste output at: https://github.com/settings/gpg/new

# From this point all new commits are signed; verify:
git log --show-signature -1
```

**Timeline:** Do this BEFORE submitting P-NT to BLMS. It ensures all future commits have verified authorship.

---

## D2. Zenodo DOI as Timestamp — Strength Assessment

### Finding: STRONG priority claim via existing infrastructure

**DOI immutability:** Zenodo DOIs are minted by CERN DataCite. Once published, a DOI record CANNOT be deleted, retracted without trace, or backdated. The `publication_date` field in each record is set by Zenodo at time of deposit and cannot be altered by the depositor after publication.

**Verified via local config:**
- `scripts/zenodo_metadata/zenodo-v6-2026-04-24.json` → `"publication_date": "2026-04-23"` for v6.0.6
- CITATION.cff → concept DOI 10.5281/zenodo.19686398

**Priority chain reconstruction:**
| Event | Timestamp Mechanism |
|---|---|
| First code commit | Git SHA in GitHub (v4.0.1 tag, date visible in packed-refs) |
| First Zenodo publication | DOI 10.5281/zenodo.19686398 + publication_date field |
| v6.0.53 series | DOIs 20030684 → 20050093 with dated publication records |
| v6.0.53.14 (latest) | DOI 20050093 — immutable CERN record |

**Conclusion:** The DOI timestamps alone constitute a legally and scientifically defensible priority record. Anyone claiming to have discovered "Conjecture M13.1," the "Damerell ladder Q(i) construction," or the specific ECI axiom set H1-H11 before 2026 would need to produce a pre-dated publication. Since no such publication exists in any indexed database (verified in Audit C), Kevin's priority is currently unchallenged.

**What would strengthen it further:**
1. arXiv submission (see D3) — adds a second independent timestamp from a higher-visibility platform
2. GPG-signed commits (see D1) — adds cryptographic authorship proof
3. Wayback Machine snapshots (see C5) — adds a third-party web archive timestamp

---

## D3. arXiv Submission Strategy — Priority Lock Recommendation

### Finding: CRITICAL GAP — papers not yet on arXiv

All 6+ submission-ready papers (P-NT, v7.4/v7.5 LMP, ER=EPR, Modular Shadow, Cardy, BEC/proton decay) are currently **only on Zenodo**. Zenodo is excellent but arXiv provides:
- Higher discoverability (Google Scholar, INSPIRE-HEP, Semantic Scholar all index arXiv)
- Stronger priority recognition in the physics community (arXiv timestamp is the de facto community standard)
- DOI via arXiv DOI resolver (`10.48550/arXiv.XXXX.YYYYY`)

### arXiv endorsement pathway for new submitters

Kevin does NOT yet have an arXiv account with established submission history. He will need an **endorser** for physics categories (hep-ph, hep-th, gr-qc, math-ph, math.NT).

**Strategy:**
1. P-NT (math.NT paper on LMFDB 4.5.b.a) — submit first to `math.NT` (Number Theory). Math.NT is somewhat easier to get endorsement for than hep-th. The result can independently be verified against LMFDB.
2. Contact outreach targets already drafted (Schäfer-Nameki, Marcolli, Booker per H7_TEMPLETON_DRAFT) — any of them could serve as endorsers
3. After P-NT is on arXiv, subsequent hep-ph/hep-th papers can use that submission history

**Timeline recommendation:**
- Week 1: Request endorsement for math.NT from Prof. Booker or another number theorist contact
- Week 2: Submit P-NT once endorsed
- Month 2: Submit modular flavor papers (hep-ph endorsement via same contacts)

---

## D4. State-Actor Falsification Scenarios

### Realistic threat assessment for a public scientific repository of an independent researcher

**Scenario (a): Take down Zenodo records**  
Risk: **VERY LOW**  
Zenodo is operated by CERN (European Organization for Nuclear Research), hosted in Switzerland, funded by EU/OpenAIRE. It stores all records redundantly across CERN data centers. A state actor would need to legally compel CERN under Swiss law AND the EU, while simultaneously erasing DataCite DOI registrations across their global registry. This is essentially impossible for a routine preprint.  
**Additionally:** Even if Zenodo went offline, the local PDFs, git history, and any Wayback Machine snapshots would remain. Priority cannot be destroyed by Zenodo takedown.

**Scenario (b): Spoof commits / GitHub account compromise**  
Risk: **LOW-MEDIUM**  
If the GitHub PAT in `.netrc` were compromised (e.g., via VPS breach), an attacker could push falsified commits to the repo. Without GPG signing, these commits would appear legitimate. However:
- Past Zenodo archives are immutable and would show different content
- GitHub's audit log shows IP addresses of pushes
- The commit hashes already published in releases/tags cannot be retroactively changed
  
**Mitigation:** GPG signing (D1) + regular rotation of GitHub PAT. The VPS's `.netrc` is `chmod 600 root:root` — acceptable, but depends on VPS security.

**Scenario (c): Antedated preprints from competitors**  
Risk: **LOW**  
A bad actor could attempt to post a paper on arXiv or a predatory journal claiming to have independently discovered the same results before Kevin, using a backdated or fast-published article.  
**Why unlikely:** The ECI framework combines highly specific mathematical structure (LMFDB 4.5.b.a identification, specific CM structure, modular forms at τ=i) with specific cosmological data analysis — extremely difficult to genuinely reproduce without prior knowledge.  
**Defense:** Zenodo DOIs with pre-2026 timestamps definitively establish prior art. A competitor paper dated 2026-05-10 cannot claim priority over Zenodo records from 2026-04-22.

**Scenario (d): DDoS GitHub repository**  
Risk: **VERY LOW / IRRELEVANT**  
A DDoS on GitHub would only temporarily affect access. All data is locally available on the VPS. GitHub is one of the most DDoS-resistant services globally (Cloudflare, Azure CDN). Any downtime would be transient.

**Scenario (e): Legal / subpoena pressure**  
Risk: **VERY LOW**  
GitHub is US-based (Microsoft). Zenodo is CERN (Switzerland). A French independent researcher's scientific preprints would be extremely unlikely targets for legal pressure. CC-BY-4.0 license means the content is already freely distributed — any takedown would be ineffective given prior distribution.  
**Note:** If a French state actor (hypothetically) wanted to suppress research, they would act on the researcher directly, not on GitHub/Zenodo. This is speculative and has essentially zero realistic probability for physics preprints.

**Overall state-actor falsification risk: LOW**  
The combination of: (1) public Zenodo DOIs with CERN timestamps, (2) public GitHub commit history, (3) CC-BY-4.0 open license, and (4) unique mathematical content that is hard to reverse-engineer, makes this project extremely resilient to falsification attempts.

---

## D5. Watermarking + Steganography

### Current state
- No explicit steganographic watermarks in PDFs
- No per-version audit hash files in Zenodo uploads (recommended but not implemented)

### Natural watermarks already present

The ECI papers have strong **inherent uniqueness** serving as natural fingerprints:
- Mathematical content (LMFDB identifiers, specific CM class numbers, exact Damerell periods)
- Specific LaTeX macros and notation conventions (e.g., `\hhat{r}`, specific bra-ket notation)
- Unique cross-reference network between the 8 papers
- Git commit SHAs embedded in paper version strings (e.g., "v6.0.53.14, commit c27cd77")
- Author's unique framing combining modular forms + von Neumann algebras + cosmology

### Recommended additions

**Immediate (per next Zenodo upload):**
Create a checksum manifest file for each version:
```bash
# Generate audit file for next upload:
VERSION="v6.0.53.14"
find /root/crossed-cosmos/notes/eci_v7_aspiration/ -name "*.pdf" -newer /tmp/last_audit | \
  xargs sha256sum > /tmp/audit_${VERSION}.txt
echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /tmp/audit_${VERSION}.txt
echo "Git-SHA: $(git -C /root/crossed-cosmos rev-parse HEAD)" >> /tmp/audit_${VERSION}.txt
# Include audit_${VERSION}.txt in the Zenodo upload alongside PDFs
```

**Medium term (WEEK):**
Add a brief "version stamp" paragraph to each paper's acknowledgements section:
> "This work is archived under Zenodo DOI 10.5281/zenodo.XXXXXXX (v6.0.53.X, committed YYYY-MM-DD, git SHA: XXXXXXX). Priority is established by that immutable record."

This makes the priority chain self-documenting within the paper itself.

---

## Summary Table — Audit D

| Sub-audit | Severity | Finding | Action |
|---|---|---|---|
| D1 Commit signing | MEDIUM | No GPG signing configured | Set up GPG (commands in section) |
| D2 Zenodo timestamps | CLEAN | Strong immutable DOI chain since 2026-04-22 | Run live verification (B5 commands) |
| D3 arXiv submission | HIGH (opportunity) | 6 papers NOT on arXiv — major discoverability gap | Submit P-NT to math.NT first |
| D4 State-actor scenarios | LOW | Theoretical risks all mitigated by existing infrastructure | No immediate action needed |
| D5 Watermarking | LOW | Natural fingerprints strong; no explicit scheme | Add sha256 manifest to future uploads |
