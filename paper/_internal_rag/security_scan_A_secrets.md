# Security Scan A — Secrets & Credentials Audit
**Repo:** /home/remondiere/crossed-cosmos  
**Date:** 2026-04-22  
**Scope:** All git-tracked files (1742 total, 728 excluding `.venv-trackB/`)  
**Tool:** ripgrep via Grep + git grep  

---

## Verdict: CLEAN — 0 actual credentials found

No real secrets, API keys, tokens, passwords, private keys, or embedded credentials were found in any tracked file.

---

## Patterns Searched

| Category | Patterns | Result |
|---|---|---|
| Anthropic API key | `sk-ant-api03-` | CLEAN |
| OpenAI API key | `sk-proj-` | CLEAN |
| HF token | `hf_[A-Za-z0-9]` (text files) | CLEAN (PDF binary noise only) |
| GitHub token | `ghp_`, `glpat-`, `gho_` | CLEAN |
| Known OPENCLAW_GATEWAY_TOKEN | `f29425d5` | CLEAN |
| Known MISTRAL_API_KEY fragment | `OWB8Ey` | CLEAN |
| Known ANTHROPIC_API_KEY fragment | `3e4XvqdwIoRO` | CLEAN |
| Known HF_TOKEN fragment | `hf_JxQe` | CLEAN |
| Known BRAVE_API_KEY fragment | `BSAfVcmh` | CLEAN |
| Known TELEGRAM_BOT_TOKEN fragment | `8386409837`, `AAEtWsU5` | CLEAN |
| Private keys | `BEGIN PRIVATE KEY`, `BEGIN RSA PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, `ssh-rsa`, `ssh-ed25519` | CLEAN |
| AWS keys | `AKIA`, `aws_secret` | CLEAN |
| Passwords | `password=`, `passwd=`, `secret=` (with value) | CLEAN |
| URL-embedded creds | `user:pass@` in https/ftp/postgres/mongodb URLs | CLEAN |
| Authorization headers | `Bearer <long-token>` | CLEAN |
| `os.environ.get` with hardcoded fallback | checked | CLEAN (only `GEMINI_MODEL` with safe model-name default) |
| curl/wget with `-u` / `--user` | checked | CLEAN |
| `.env` files tracked | none | CLEAN |

---

## Informational Findings (Not Secrets)

### 1. MISTRAL_API_KEY references in derivation scripts — SAFE
**Files:**
- `derivations/V6-magistral-derivation.py` (lines 8, 58, 64, 122)
- `derivations/V6-mistral-cross-check.py` (lines 7, 97, 99)
- `derivations/V10-magistral-adversarial.py` (lines 7, 46, 52, 111)
- `derivations/V11-magistral-adversarial.py` (lines 11, 57, 63, 121)
- `derivations/V12-magistral-adversarial.py` (lines 11, 52, 58, 116)
- `paper/_peer_review_v6/run_v6_panel.py` (lines 164, 166)

**Pattern:** `os.getenv("MISTRAL_API_KEY")` — reads from environment only. No hardcoded value. Falls back to parsing `~/.openclaw/.env` at runtime (path only, not value). Correct pattern.

**Severity:** None — informational only.

### 2. `os.environ.get` with non-secret default — SAFE
**File:** `paper/_peer_review_v6/run_v6_panel.py` line 139  
**Pattern:** `os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")` — default is a public model name, not a credential.

**Severity:** None.

### 3. PDF binary file tracked (`derivations/_cache/desi-dr2.pdf`) — NOT A SECRET
Contains binary sequences that trigger naive `hf_` pattern matches. Inspected: these are binary noise, not HF tokens.

**Severity:** None.

---

## .gitignore Coverage Gaps

| Gap | Risk | Recommendation |
|---|---|---|
| `.venv-trackB/` is NOT excluded — 1 014 files tracked | Low (pip venv, no credentials found) | Add `.venv-trackB/` to `.gitignore` unless intentionally vendored for reproducibility |
| No `.env` / `*.env` exclusion pattern | Medium (no .env files currently tracked, but future protection absent) | Add `*.env` / `.env*` to `.gitignore` |
| `derivations/_cache/*.pdf` not excluded | Low (DESI public data) | Add `derivations/_cache/*.pdf` if large binary not desired |

---

## Recommendations

1. **Add to `.gitignore`** (low urgency, defensive):
   ```
   .env
   .env.*
   *.env
   .venv-trackB/
   ```

2. **Mistral scripts** (V6–V12, run_v6_panel.py): current pattern `os.getenv("MISTRAL_API_KEY")` is correct. No action needed.

3. **Pre-commit hook** (optional): add `gitleaks` or `detect-secrets` as a pre-commit hook to catch future credential commits automatically. Config already exists in user's tooling (`gitleaks 8.24`).

---

## Summary

**CLEAN** — 0 credentials, 0 tokens, 0 private keys found in 1 742 tracked files.  
3 `.gitignore` coverage gaps (low-to-medium risk, no active exposure).
