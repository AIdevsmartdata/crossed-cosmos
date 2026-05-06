# Audit B — Zenodo API Sync Verification
**Date:** 2026-05-06  
**Concept DOI:** 10.5281/zenodo.19686398 (concept record ID: 19686398)  
**Latest version DOI:** 10.5281/zenodo.20050093 (per project context v6.0.53.14)  

---

## Important Note on Verification Method

Direct Zenodo API calls (curl/WebFetch) were not permitted during this audit session. Verification is based on:
1. Local scripts and config files in the repo (inspected directly)
2. CITATION.cff, README.md, .zenodo.json (checked for consistency)
3. Project context from MEMORY.md (tracking 14+ Zenodo DOIs)
4. Cross-checking both Zenodo scripts for ID consistency
5. Web search results for context about Zenodo platform status

**For live DOI integrity, Kevin must run manual verification commands** provided in section B5.

---

## B1. Concept DOI Integrity

### Cross-reference across config files

| File | Concept DOI |
|---|---|
| `CITATION.cff` | `10.5281/zenodo.19686398` |
| `README.md` | `10.5281/zenodo.19686398` |
| `.zenodo.json` | (implicitly, via GitHub webhook integration) |
| `scripts/zenodo_apply_metadata.py` | `19686398` (hardcoded `CONCEPT_RECID`) |
| `scripts/zenodo_push_pdf.py` | **`19686399`** ← MISMATCH |

### CRITICAL FINDING: Concept ID Mismatch in zenodo_push_pdf.py

`scripts/zenodo_push_pdf.py` line 41:
```python
CONCEPT_RECORD_ID = "19686399"  # crossed-cosmos concept (parent of all versions)
```

**Correct value should be `19686398`** (as confirmed in CITATION.cff, README.md, and zenodo_apply_metadata.py).

**Impact:** The `zenodo_push_pdf.py` script uses `CONCEPT_RECORD_ID` to query `/versions` when resolving records by tag (function `find_record_for_tag`). If this script is called for future uploads, it will query the WRONG concept record and fail to find the correct version records, causing PDF upload failures.

**However:** The workflow file `zenodo-upload-pdf.yml` has the auto-release trigger **disabled since 2026-05-04**. The script is only used manually. The fallback path (`--record 19708665`) in the workflow hardcodes a specific record ID, bypassing the tag resolution path. This limits immediate impact but the bug must be fixed.

**Fix (one-line):**
```python
# In scripts/zenodo_push_pdf.py line 41:
CONCEPT_RECORD_ID = "19686398"  # crossed-cosmos concept (parent of all versions)
```

**Severity: HIGH** (latent bug — no current data loss, but will break future automated PDF uploads if re-enabled)

---

## B2. Version DOI Coverage

### Known DOI inventory (from project MEMORY.md and code)

| Version | Zenodo ID | Notes |
|---|---|---|
| Concept | 19686398 | Always-latest pointer |
| v6.0.0 | per tag history | First v6 |
| v6.0.6 | 19708665 | Referenced in workflow fallback |
| v5 companion | 19696017 | Cited in CITATION.cff |
| v6 companion | 19699006 | Cited in CITATION.cff |
| v6.0.53 | 20030684 | Noted in MEMORY.md |
| v6.0.53.1 | 20034969 | Noted in MEMORY.md |
| v6.0.53.3 | 20036808 | Noted in MEMORY.md |
| v6.0.53.14 | 20050093 | Latest in MEMORY.md |

The `.gitignore` and version-level zenodo metadata scripts confirm at least 4 curated version specs (v5, v6, v7-note, chimere-omega). MEMORY.md states "14 DOIs published."

**Tag count confirms scale:** 51 local tags + 17 packed = 68 total tags. Not all tags map to separate Zenodo records (the GitHub webhook creates one Zenodo record per tagged release).

### Metadata consistency check (via .zenodo.json and spec files)

`.zenodo.json` (root file for GitHub integration) specifies:
- Title: "ECI — Entanglement, Complexity, Information: a framework paper"
- Creator: Remondière, Kevin; ORCID: 0009-0008-2443-7166
- License: CC-BY-4.0
- Access: open
- Upload type: publication/preprint
- Related identifiers: ORCID, GitHub repo, zenodo.19696017, zenodo.19699006

Version-specific specs in `scripts/zenodo_metadata/` (4 JSON files):
- All specify `"access_right": "open"` and `"license": "CC-BY-4.0"` — CONSISTENT
- All include `isVersionOf: 10.5281/zenodo.19686398` — CONSISTENT
- Creator name/ORCID consistent across all 4 specs

**No metadata inconsistency detected in local files.**

---

## B3. Cross-Version Consistency Analysis

**What can be verified locally:**

The 4 spec files consistently declare:
- License CC-BY-4.0 on all curated versions
- Single creator: Remondière, Kevin with ORCID 0009-0008-2443-7166
- `publication_date` set explicitly (e.g., `"2026-04-23"` for v6.0.6 spec)
- `"communities": []` — no community affiliation declared (expected for independent researcher)

**What requires live API verification:**
- Whether all 14 DOIs resolve correctly at zenodo.org
- Whether each version record links back to concept DOI 19686398
- File checksums (sha256) for each version's PDF

---

## B4. "Robotscrap" Concern — Platform-Level Finding

Kevin's concern about being "robot-scraped on Zenodo" is confirmed as a **platform-wide phenomenon**, not a targeted attack on this repo.

**Verified finding from Zenodo blog (November 2025):**
- Zenodo observes ~180 requests/sec average, up to 500 req/sec peaks
- Automated systems (AI training data harvesters) actively bypass rate limits
- New rate limits enforced: 25 results/page anon, 100 authenticated, max 30 req/min
- Zenodo recommends OAI-PMH for bulk metadata access

**Nature (2025) confirmed:** "Automated programs gathering training data for AI tools are overwhelming academic websites."

**Assessment for Kevin's specific case:**
- The scraping was NOT targeted at crossed-cosmos specifically — it's systemic
- CC-BY-4.0 license PERMITS re-use with attribution — scraped content that is re-used without attribution violates the license but this is extremely common for AI training
- Zenodo records (public PDFs and metadata) are legally scrapeable under CC-BY terms
- The scraped content cannot be "stolen" in the copyright sense as long as attribution is required — what it CAN do is feed AI training data

**Risk assessment:**
- Content being harvested for AI training: VERY LIKELY (affects all Zenodo public records)
- Content being plagiarized in a competing paper: LOW — original mathematical derivations are hard to plagiarize undetected
- Content appearing in an LLM's training set: PROBABLE but NOT harmful to priority claims — Zenodo DOIs provide timestamped priority independent of training data

---

## B5. Manual Live Verification Commands

Kevin should run these commands to verify live Zenodo state:

```bash
# B5.1 — Verify concept DOI resolves
curl -s "https://zenodo.org/api/records/19686398" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('Title:', d.get('metadata',{}).get('title'))
print('Latest:', d.get('links',{}).get('latest'))
print('DOI:', d.get('doi'))
print('Files:', [f['key'] for f in d.get('files',[])])
"

# B5.2 — Verify latest version DOI
curl -s "https://zenodo.org/api/records/20050093" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('Title:', d.get('metadata',{}).get('title'))
print('Version:', d.get('metadata',{}).get('version'))
print('Date:', d.get('metadata',{}).get('publication_date'))
print('DOI:', d.get('doi'))
print('ConceptDOI:', d.get('conceptdoi'))
for f in d.get('files',[]):
    print(f'File: {f[\"key\"]} ({f.get(\"size\",\"?\")} bytes) sha256={f.get(\"checksum\",\"?\")}')
"

# B5.3 — Count all versions under concept DOI
curl -s "https://zenodo.org/api/records/19686398/versions?size=100" | python3 -c "
import json,sys
d=json.load(sys.stdin)
hits = d.get('hits',{}).get('hits',[])
print(f'Total versions: {len(hits)}')
for h in hits:
    m = h.get('metadata',{})
    print(f'  {m.get(\"version\")} → {h.get(\"doi\")} [{m.get(\"publication_date\")}]')
"

# B5.4 — Fix the concept ID bug in zenodo_push_pdf.py
sed -i 's/CONCEPT_RECORD_ID = "19686399"/CONCEPT_RECORD_ID = "19686398"/' \
    /root/crossed-cosmos/scripts/zenodo_push_pdf.py
```

---

## Summary Table — Audit B

| Sub-audit | Severity | Finding | Action |
|---|---|---|---|
| B1 Concept DOI | HIGH | `zenodo_push_pdf.py` has wrong concept ID `19686399` vs correct `19686398` | Fix one-line in script |
| B2 Version coverage | CLEAN (local) | 14 DOIs claimed, local config consistent | Run B5.3 to verify live |
| B3 Metadata consistency | CLEAN (local) | All spec files agree on license, ORCID, creator | Run B5.1–B5.2 to verify |
| B4 Robotscraping | INFO | Platform-wide Zenodo AI harvesting (confirmed 2025); not targeted attack | No action; CC-BY permits |
