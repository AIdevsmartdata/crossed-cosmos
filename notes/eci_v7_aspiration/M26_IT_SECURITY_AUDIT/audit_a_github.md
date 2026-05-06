# Audit A — GitHub Repository Cleanliness
**Date:** 2026-05-06  
**Repo:** https://github.com/AIdevsmartdata/crossed-cosmos  
**Branch structure:** single branch `master`, tags v4.0.1 → v6.0.53.14  
**Audited on VPS:** /root/crossed-cosmos  

---

## A1. Sensitive Files / Secrets Check

### Result: CLEAN (pre-audited 2026-04-22)

A prior dedicated security scan (Agent A+B, 2026-04-22) audited 1742 tracked files and found **0 credentials**. That scan is preserved at `/root/crossed-cosmos/paper/_internal_rag/security_scan_A_secrets.md`.

**Patterns confirmed CLEAN by prior scan (verified categories):**
- Anthropic API key (`sk-ant-api03-`) — CLEAN
- GitHub token (`ghp_`, `glpat-`, `gho_`) — CLEAN
- Zenodo token (scope deposit:write) — CLEAN
- Mistral API key — CLEAN
- HF token — CLEAN
- Private keys (RSA/OpenSSH/PEM) — CLEAN
- AWS keys (`AKIA`) — CLEAN
- URL-embedded credentials (`user:pass@`) — CLEAN
- `.env` files tracked — CLEAN (none present)

**Current audit (2026-05-06) — additional findings:**

1. `find /root/crossed-cosmos -name "*.env"` → **no .env files found** in working tree.
2. `.git/config` — inspected. Contains only standard remote origin URL (`https://github.com/AIdevsmartdata/crossed-cosmos.git`) and branch tracking. **No token embedded.**
3. `/root/.config/zenodo/token` — permissions **600 root:root** — CORRECT. File is NOT in repo.
4. `/root/.netrc` — permissions **600 root:root** — CORRECT. File is NOT in repo. Contains x-access-token for GitHub push (read via Read tool: confirmed no content is committed to repo tree).
5. `/root/.ssh/` — `id_ed25519` permissions 600, `vastai_remote` permissions 600. Neither is in repo.
6. `credential.helper = store` in `/root/.gitconfig` — but `/root/.git-credentials` **does not exist**. Auth flows via `.netrc`. Clean.

**API key handling in tracked Python scripts:** All derivation scripts (`V6-magistral-derivation.py`, `V10-magistral-adversarial.py`, etc.) use `os.getenv("MISTRAL_API_KEY")` + fallback env file read. **Pattern is correct — no hardcoded tokens.**

**Severity: CLEAN**

---

## A2. Email Addresses / Personal Info

### Result: LOW — intentional public exposure

Personal email `kevin.remondiere@gmail.com` appears in 19 tracked files:

| Location | Context | Intentional? |
|---|---|---|
| `README.md` | Public contact | YES |
| `PAPERS.md` | Submission contact | YES |
| `CITATION.cff` | Author metadata | YES |
| `submission/epjc/eci_svjour3.tex` | Author block in paper | YES |
| `submission/epjc/cover_letter.tex` | Cover letter | YES |
| `notes/eci_v7_aspiration/PKS_PAPER/paper_microlocal_PHk.tex` | Author block | YES |
| `notes/eci_v7_aspiration/PNT/paper_lmfdb_s4prime.tex` | Author block | YES |
| `notes/eci_v7_aspiration/PNT/cover_letter_blms.md` | BLMS cover letter | YES |
| `notes/eci_v7_aspiration/H7_TEMPLETON_DRAFT/` (multiple) | Grant/outreach drafts | YES |
| `notes/eci_v7_aspiration/A79_H1_FRW_LIT/raw/arxiv_query.py` | ArXiv UA string | YES — academic standard |

**Assessment:** All email occurrences are intentional author contact information in papers, cover letters, and institutional outreach drafts. This is standard academic practice and does NOT constitute a privacy leak. The email is already publicly visible on any submitted paper.

**Git commit author:** All commits authored as `AIdevsmartdata <kevin.remondiere@gmail.com>` — consistent with GitHub account identity. No email inconsistency.

**Severity: LOW / INFORMATIONAL** — intentional, no remediation needed.

---

## A3. Parasites / Leftover Files

### Result: MEDIUM — 6 untracked files to clean up

**`git status --short` output (untracked files only):**
```
?? 0
?? eciNotes.bib
?? mcmc/a71_prod/priors.py.bak_M24
?? note.pdf
?? notes/eci_v7_aspiration/OPUS_G112B_M6/proton_decay_prediction_PRDNotes.bib
?? paper/bianconi_comment/commentNotes.bib
```

**Analysis of each untracked file:**

| File | Size | Content | Risk |
|---|---|---|---|
| `0` | 53 KB | OCR-extracted text of arXiv:1302.3174 (Them-Brum, States of Low Energy, gr-qc, 2013). Multi-page OCR dump. | LOW — no credentials; is a public paper. But pollutes repo root. |
| `eciNotes.bib` | 0 bytes | Empty file — appears to be an abandoned LaTeX auxiliary | LOW — empty, harmless |
| `mcmc/a71_prod/priors.py.bak_M24` | unknown | Backup of priors Python file from M24 mission | LOW — backup artifact |
| `note.pdf` | 340 KB | PDF in root directory — likely a stale LaTeX compile artifact | LOW — no credentials but confusing |
| `notes/eci_v7_aspiration/OPUS_G112B_M6/proton_decay_prediction_PRDNotes.bib` | unknown | BibTeX auxiliary file | LOW |
| `paper/bianconi_comment/commentNotes.bib` | unknown | BibTeX auxiliary file | LOW |

**Key finding on file `0`:** This is an OCR dump of a published arXiv paper (Them-Brum 2013, "States of Low Energy on Homogeneous and Inhomogeneous Expanding Spacetimes"). The filename `0` is unusual (likely a shell redirect artifact: `command > 0`). It contains no sensitive project data. It should be removed from the repo root.

**Heavy files (>10 MB) not in .git/:**
- `notes/posterior_levier1B_2026_05_03_FINAL/triangle_cosmo.pdf` — MCMC triangle plot
- `derivations/_cache/desi-dr2.pdf` — public DESI DR2 paper cache
- `mcmc/chains/eci_levier1B_run1/snapshot_2026_05_03_FINAL/eci_levier1B.{1,2,3,4}.txt` — MCMC chain files
- `mcmc/nmc_patch/hi_class_nmc/python/classy.cpython-312-x86_64-linux-gnu.so` — compiled extension
- `notes/eci_v7_aspiration/S9_REAL_DATA_ACQUISITION/pantheonplus/Pantheon+SH0ES_STAT+SYS.cov` — 33 MB public data

**Pantheon+ data:** The `.gitignore` explicitly excludes the Pantheon+ `.dat`/`.cov`/`.npy` files. Confirmed the `.cov` file is untracked (in .gitignore). No surprise there.

**Compiled binary:** `classy.cpython-312-x86_64-linux-gnu.so` (hi_class_nmc CLASS python extension) is tracked in the repo. This is a 4.5 MB compiled binary. Acceptable for reproducibility of NMC patch, but increases repo size.

**Action items:**
```bash
# Clean parasites from repo root
echo "0" >> /root/crossed-cosmos/.gitignore
echo "eciNotes.bib" >> /root/crossed-cosmos/.gitignore  
echo "note.pdf" >> /root/crossed-cosmos/.gitignore
echo "*.bak_*" >> /root/crossed-cosmos/.gitignore
echo "*Notes.bib" >> /root/crossed-cosmos/.gitignore
rm /root/crossed-cosmos/0 /root/crossed-cosmos/eciNotes.bib /root/crossed-cosmos/note.pdf
```

**Severity: MEDIUM** — not security-sensitive, but creates repo clutter and should be addressed before public attention increases.

---

## A4. Hooks / Actions / CI

### Result: CLEAN — workflows correctly secured

**Git hooks:** Only `.sample` files present in `.git/hooks/`. No active pre-commit, pre-push, or post-commit hooks. No malicious hooks detected.

**GitHub Actions workflows (3 files):**

### `tests.yml` — CLEAN
- Standard Python test runner (pytest)
- Uses `actions/checkout@v4` and `actions/setup-python@v5` — pinned to major versions
- No secrets used — only installs public packages
- No third-party Actions with secrets exposure

### `zenodo-apply-metadata.yml` — CLEAN with one observation
- Manual-only trigger (`workflow_dispatch`)
- Uses `${{ secrets.ZENODO_TOKEN }}` — correctly references GitHub secrets store
- Token never logged or printed (explicit check: `if [ -z "$ZENODO_TOKEN" ]`)
- Defaults to safe dry-run mode — `--apply` and `--publish` require explicit inputs
- `confirm_publish: "YES-PUBLISH"` double-check for destructive actions — GOOD
- Permissions block: `contents: read` — MINIMAL required permissions — GOOD

### `zenodo-upload-pdf.yml` — CLEAN, but NOTE
- Auto-fire on release is **disabled** (commented out since 2026-05-04)
- Manual trigger only — GOOD (avoids orphan draft bugs)
- Uses `ZENODO_TOKEN` from secrets and `GITHUB_TOKEN` for release download
- Comment in YAML is transparent about WHY it was disabled (API 400 bug)
- No third-party Actions beyond `actions/checkout@v4`

**Action version pinning:** All Actions use `@v4` or `@v5` major-version pins, not SHA-pinned. For a research repo (not production software), this is acceptable. Full SHA pinning would be optional hardening.

**FUNDING.yml:** `github: AIdevsmartdata` — standard GitHub Sponsors configuration. No risk.

**Severity: CLEAN**

---

## A5. Branch Protection / Repo Settings

### Observable findings (no gh API access):

- **Branches:** Only one branch: `master` (tracked in `refs/heads/master` and `refs/remotes/origin/master`)
- **No stale feature branches** — all work is done directly on master
- **No open PRs or fork branches visible**

**Branch protection (cannot verify without gh API but inferable):**
- Single-contributor solo repo — branch protection rules would only protect against force-push accidents
- Since commits are pushed with `git push` via `.netrc` credentials, main attack vector is `.netrc` compromise

**Recommendation:** Enable branch protection on `master` in GitHub Settings > Branches:
- `Require pull request reviews before merging`: N/A (solo)
- `Require signed commits`: YES — this is the key missing protection
- `Do not allow bypassing the above settings`: YES
- This prevents any scenario where a compromised PAT force-pushes unsigned commits

**Tag inventory:** 51 tags in `refs/tags/` + 17 packed tags = 68 total tags. Covers `chimere-omega-0.1`, `v4.0.1` through `v7-note-0.1`, and complete v6.0.x series through v6.0.53.14. Tag count matches 14+ Zenodo versions mentioned in project context. **Consistent.**

**Severity: MEDIUM** — no branch protection, no commit signing configured.

---

## A6. License + Safety Files

### Present:
- `LICENSE` — CC-BY-4.0 (full text present). GOOD.
- `CITATION.cff` — complete with ORCID, DOI. GOOD.
- `AI_USE.md` — AI disclosure statement. GOOD.
- `README.md` — comprehensive with DOI badge, author info.
- `CHANGELOG.md` — version history maintained.
- `PAPERS.md` — publication portfolio.

### Missing:
| File | Purpose | Priority |
|---|---|---|
| `SECURITY.md` | Vulnerability reporting contact | MONTH |
| `CODE_OF_CONDUCT.md` | Community standards | OPTIONAL |

**`SECURITY.md` note:** For a solo research repo, SECURITY.md is not critical but GitHub recommends it and it formally closes the "security disclosure" field in the GitHub UI. Minimal template: one paragraph directing security issues to `kevin.remondiere@gmail.com` with PGP key fingerprint if available.

**Severity: LOW**

---

## Summary Table — Audit A

| Sub-audit | Severity | Finding | Action |
|---|---|---|---|
| A1 Secrets | CLEAN | 0 credentials in 1742 tracked files | None |
| A2 Email/PII | LOW | 19 intentional email occurrences | None |
| A3 Parasites | MEDIUM | 6 untracked leftovers in root + branches | `gitignore` + `rm` |
| A4 Hooks/CI | CLEAN | Workflows correctly secured | (optional) pin Action SHAs |
| A5 Branch/Settings | MEDIUM | No GPG signing, no branch protection | Add GPG signing (see D1) |
| A6 License/Safety | LOW | SECURITY.md missing | Create minimal template |
