# Actionable Recommendations — ECI IT Security Audit
**Date:** 2026-05-06  
**Prepared by:** M26 IT Security sub-agent  

---

## Priority Matrix

| # | Finding | Severity | Priority | Effort |
|---|---|---|---|---|
| 1 | zenodo_push_pdf.py concept ID bug (19686399 → 19686398) | HIGH | NOW | 1 min |
| 2 | arXiv submission — 6 papers not yet submitted | HIGH (opportunity) | NOW | Weeks |
| 3 | Leftover files in repo root (0, eciNotes.bib, note.pdf) | MEDIUM | WEEK | 5 min |
| 4 | GPG commit signing not configured | MEDIUM | WEEK | 30 min |
| 5 | Wayback Machine manual snapshots | LOW | WEEK | 5 min |
| 6 | SECURITY.md missing | LOW | MONTH | 10 min |
| 7 | Sha256 manifest in Zenodo uploads | LOW | MONTH | Scripted |
| 8 | Action version pinning to SHAs | LOW | OPTIONAL | 15 min |
| 9 | ResearchGate profile check | LOW | WEEK | 5 min |

---

## NOW — Fix immediately

### REC-1: Fix zenodo_push_pdf.py concept ID [1 line, 1 minute]

**Severity: HIGH — will break future automated PDF uploads if re-enabled**

```bash
# Run on VPS:
sed -i 's/CONCEPT_RECORD_ID = "19686399"/CONCEPT_RECORD_ID = "19686398"/' \
    /root/crossed-cosmos/scripts/zenodo_push_pdf.py

# Verify fix:
grep "CONCEPT_RECORD_ID" /root/crossed-cosmos/scripts/zenodo_push_pdf.py
# Expected output: CONCEPT_RECORD_ID = "19686398"

# Commit:
git -C /root/crossed-cosmos add scripts/zenodo_push_pdf.py
git -C /root/crossed-cosmos commit -m "fix: zenodo_push_pdf concept ID typo 19686399 → 19686398"
git -C /root/crossed-cosmos push
```

### REC-2: arXiv submission pipeline [critical priority gap]

**Severity: HIGH — every week without arXiv is a priority exposure window**

The 6 submission-ready papers exist only on Zenodo. arXiv provides:
- Timestamped priority recognized by the global physics community
- Google Scholar / INSPIRE-HEP indexing
- Discoverability (currently near-zero via web search)

**Recommended submission order (from PAPER-COHESION audit):**
1. **Week 1-2:** P-NT "Two LMFDB IDs for hatted weight-5 multiplets of S'_4" → `math.NT`
   - This is the most independently verifiable (LMFDB live verification)
   - math.NT endorsement easier to obtain than hep-th
   - Zenodo DOI: 10.5281/zenodo.20030684 (or latest) goes in the abstract

2. **Week 3-4:** V2 "No-go theorem at τ=i" → `hep-ph`
   - After P-NT submission history established

3. **Month 2:** Cardy + Modular Shadow → `math-ph`

4. **Month 2-3:** P-KS + ER=EPR → `hep-th`

**Endorsement strategy:**
- Email Prof. Booker (endorsement email drafted in `H7_TEMPLETON_DRAFT/OUTREACH_EMAILS/email_1_booker_june2026.md`) — but schedule NOW not June
- Alternatively: post math.NT preprint to HAL (French national archive, no endorsement needed) to establish French priority record while seeking arXiv endorsement

---

## WEEK — Address within 7 days

### REC-3: Clean repo root leftover files

**Severity: MEDIUM — clutter, not security risk**

```bash
# Add to .gitignore (run from /root/crossed-cosmos):
cat >> .gitignore << 'EOF'

# Leftover files (M26 audit 2026-05-06)
/0
/eciNotes.bib
/note.pdf
/note.aux
/note.log
/note.out
*.bak_*
*Notes.bib
EOF

# Remove the files:
rm -f /root/crossed-cosmos/0
rm -f /root/crossed-cosmos/eciNotes.bib
rm -f /root/crossed-cosmos/note.pdf

# Commit:
git -C /root/crossed-cosmos add .gitignore
git -C /root/crossed-cosmos commit -m "cleanup: ignore/remove stale root artifacts (M26 audit)"
git -C /root/crossed-cosmos push
```

**What `0` contains:** OCR dump of arXiv:1302.3174 (Them-Brum 2013, "States of Low Energy"). This is a public reference paper, not ECI content. Safe to delete.

### REC-4: Set up GPG commit signing

**Severity: MEDIUM — needed for anti-falsification guarantees before major journal submissions**

```bash
# Step 1: Generate key on VPS (run as root since repo is /root/)
gpg --batch --gen-key <<EOF
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: Kevin Remondière
Name-Email: kevin.remondiere@gmail.com
Expire-Date: 2y
%commit
EOF

# Step 2: Get the key fingerprint
gpg --list-secret-keys --keyid-format LONG kevin.remondiere@gmail.com

# Step 3: Configure git globally
git config --global user.signingkey <FINGERPRINT>
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Step 4: Export public key for GitHub
gpg --armor --export kevin.remondiere@gmail.com > /tmp/gpg_public_key.txt
# Upload content of gpg_public_key.txt at:
# https://github.com/settings/gpg/new

# Step 5: Sign a tag for the latest version
git -C /root/crossed-cosmos tag -s v6.0.53.14-signed -m "GPG-signed re-tag of v6.0.53.14"

# Step 6: Keep a backup of the GPG key
gpg --armor --export-secret-keys kevin.remondiere@gmail.com > /root/.config/gpg_backup_$(date +%Y%m%d).asc
chmod 600 /root/.config/gpg_backup_*.asc
```

**Note:** After setup, all future commits will be automatically signed. GitHub will show a "Verified" badge on each commit.

### REC-5: Wayback Machine manual snapshots

**Severity: LOW — adds third-party timestamp redundancy**

Trigger Wayback Machine to archive key Zenodo pages:
```bash
# Save concept DOI page:
curl "https://web.archive.org/save/https://zenodo.org/records/19686398"

# Save latest version:
curl "https://web.archive.org/save/https://zenodo.org/records/20050093"

# Save GitHub repo:
curl "https://web.archive.org/save/https://github.com/AIdevsmartdata/crossed-cosmos"
```

This is free, takes <1 minute, and adds a publicly verifiable third-party timestamp.

### REC-9: ResearchGate profile check

**Severity: LOW**

Search `https://www.researchgate.net/search?q=Kevin+Remondiere` to verify no auto-created profile exists with incorrect metadata. If found, claim the profile to ensure accuracy. Takes 5 minutes.

---

## MONTH — Within 30 days

### REC-6: Add SECURITY.md

**Severity: LOW — best practice, closes GitHub UI recommendation**

Create `/root/crossed-cosmos/SECURITY.md`:

```markdown
# Security Policy

## Scope

This is an academic research repository. Security issues in the technical sense
(vulnerable dependencies, etc.) are low risk as this project has no production deployment.

## Reporting

For concerns about integrity, falsification, or unauthorized use of research content:

**Email:** kevin.remondiere@gmail.com  
**ORCID:** https://orcid.org/0009-0008-2443-7166

For citation priority concerns, please reference:
**Zenodo concept DOI:** https://doi.org/10.5281/zenodo.19686398
```

### REC-7: Add sha256 manifest to Zenodo uploads

**Severity: LOW — adds watermarking and integrity verification layer**

```bash
# Template script: generate per-version manifest before Zenodo upload
VERSION="v6.0.53.14"
GIT_SHA=$(git -C /root/crossed-cosmos rev-parse HEAD)
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat > /tmp/audit_${VERSION}.txt << EOF
ECI audit manifest — ${VERSION}
Generated: ${DATE}
Git-SHA: ${GIT_SHA}
Concept DOI: 10.5281/zenodo.19686398

SHA-256 checksums of submitted PDFs:
EOF

# Add checksums for all paper PDFs in this release:
find /root/crossed-cosmos/notes/eci_v7_aspiration -name "*.pdf" -newer /tmp/last_upload | \
    xargs sha256sum >> /tmp/audit_${VERSION}.txt

# Include this file in the Zenodo deposit alongside PDFs
```

---

## OPTIONAL — Enhanced hardening (not urgent)

### REC-8: Pin GitHub Actions to SHA hashes

**Severity: LOW — defense in depth for CI/CD pipeline**

Current `actions/checkout@v4` is pinned to major version. For maximum security, pin to exact SHA:

```yaml
# In .github/workflows/*.yml, replace:
uses: actions/checkout@v4
# With:
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

uses: actions/setup-python@v5
# With:
uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2f  # v5.3.0
```

This prevents supply-chain attacks where an Action maintainer publishes a malicious update to a major version tag.

---

## Overall Risk Summary

| Category | Overall Status |
|---|---|
| Credentials / secrets | CLEAN — 0 found in 1742 tracked files |
| Personal info exposure | INTENTIONAL LOW — academic author contact |
| Repo parasites | MEDIUM — 3 files to remove, 3 .bib artifacts |
| CI/CD security | CLEAN — token handling correct, manual-only triggers |
| Zenodo sync | HIGH FINDING — concept ID bug in push script (fix now) |
| Bot scraping | SYSTEMIC — CC-BY-4.0 permits; not targeted |
| Priority protection | STRONG — Zenodo DOI chain solid; arXiv gap is key weakness |
| Falsification risk | LOW — multiple immutable timestamp layers |
| State-actor risk | VERY LOW — CERN infrastructure, public CC content |

**Bottom line:** The repo is well-maintained and already passed a rigorous 2026-04-22 credentials audit. The two most impactful actions are: (1) fix the 1-line Zenodo concept ID bug, and (2) begin arXiv submission to lock scientific priority in the community-recognized record system.
