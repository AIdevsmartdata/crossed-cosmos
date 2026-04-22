# Security Scan B — PII & Internal-Reference Audit
Date: 2026-04-22 | Scope: all git-tracked files outside `.venv-trackB/`

---

## Summary

**FINDINGS** — 4 categories, 14 distinct file-level findings.  
No phone numbers, postal addresses, SSN, IBAN, Telegram tokens/chat-IDs, or private-repo paths found.  
No third-party personal names beyond academic-paper authors (intentional).

---

## Category 1 — Third-party email addresses in RAG / source code

| Severity | File | Line | Pattern | Recommendation |
|---|---|---|---|---|
| LOW | `paper/_rag/Bedroya2025.txt` | 391-393 | `jiamingp@umich.edu`, `ye@lorentz.leidenuniv.nl` | Leave — academic paper author contact, scraped from arXiv |
| LOW | `paper/_rag/Wolf2025.txt` | 500 | `william.wolf@stx.ox.ac.uk` | Leave — academic author |
| LOW | `paper/_rag/PanYe2026.txt` | 391-393 | same as Bedroya2025 (shared authors) | Leave |
| LOW | `paper/_rag/PoulinSmith2026.txt` | 66-70 | 4 academic emails | Leave — published paper |
| LOW | `paper/_rag/DEHK2025a.txt` | 21-27 | 4 OIST/PITP emails | Leave — published paper |
| LOW | `paper/_rag/CryptoCensorship.txt` | 19-20 | 5 MIT emails | Leave — published paper |
| LOW | `paper/_rag/FaulknerSperanza2024.txt` | 46-48 | `tomf@illinois.edu`, `asperanz@gmail.com` | Leave — published paper |
| LOW | `paper/_rag/Yip2024.txt` | 33-34 | 4 academic emails | Leave — published paper |
| LOW | `paper/_rag/DEHK2025b.txt` | 119-121 | 2 academic emails (Calabrese, Hill) | Leave — published paper |
| LOW | `paper/_rag/Faraoni2004.txt` | 12 | `vfaraoni@unbc.ca` | Leave — published paper |
| LOW | `paper/_rag/Faraoni2000.txt` | 45-47 | 2 academic emails | Leave — published paper |
| LOW | `paper/_rag/Montero2022.txt` | 15-16 | `mmontero@g.harvard.edu`, `vafa@g.harvard.edu`, `irene.valenzuela@cern.ch` | Leave — published paper |
| LOW | `paper/_rag/Ye2025.txt` | 340 | `ye@lorentz.leidenuniv.nl` | Leave — published paper |
| LOW | `mcmc/nmc_patch/hi_class_nmc/CPU.py` | 5 | `benjamin.audren@gmail.com` | Leave — hi_class open-source attribution |
| LOW | `mcmc/nmc_patch/hi_class_nmc/python/classy.pyx` | 4-6 | 3 hi_class maintainer emails | Leave — open-source attribution |
| LOW | `mcmc/nmc_patch/hi_class_nmc/cpp/ClassEngine.hh` | 9 | `plaszczy@lal.in2p3.fr` | Leave — open-source attribution |
| LOW | `derivations/_cache/desi-dr2.txt` | 288 | `spokespersons@desi.lbl.gov` | Leave — from official DESI paper |
| LOW | `submission/hal/response.xml` | 9 | `hal@ccsd.cnrs.fr` | Leave — HAL API system address |

**Assessment:** All third-party emails are academic paper author contacts or open-source maintainer attributions extracted from published sources. None are private.

---

## Category 2 — Internal system references (`.openclaw/`, hardcoded paths)

| Severity | File | Line | Pattern | Recommendation |
|---|---|---|---|---|
| MEDIUM | `_run_all.py` | 6 | `PY = "/home/remondiere/.openclaw/venvs/pipeline/bin/python"` | Replace with `sys.executable` or env var; hardcoded internal tool path reveals private toolchain name |
| MEDIUM | `RESULTS.md` | 15, 74 | `~/.openclaw/venvs/pipeline/` (2 occurrences) | Redact to generic `(project venv)` — references private tooling namespace |
| MEDIUM | `derivations/V10-magistral-adversarial.py` | 7, 45, 49, 111 | `~/.openclaw/.env` path in comments and code | Low risk (no key value present, just path), but redact comment path to `~/.env` or env var only |
| MEDIUM | `derivations/V11-magistral-adversarial.py` | 10, 60 | same pattern | Same — redact `~/.openclaw/.env` references |
| MEDIUM | `derivations/V6-magistral-derivation.py` | 8, 61 | same pattern | Same |
| MEDIUM | `derivations/V12-magistral-adversarial.py` | 10, 55 | same pattern | Same |
| MEDIUM | `paper/_peer_review_v2/run_3model.py` | 20 | `source ~/.openclaw/.env` in error message | Redact to generic `source <env file>` |
| MEDIUM | `paper/_peer_review_v6/run_v6_panel.py` | 28-29 | `Path.home() / ".openclaw" / ".env"` hardcoded | Replace with env-var fallback only |

**Assessment:** The `.openclaw` directory name is a private internal branding. These references reveal the author's private AI toolchain. Recommend either removing the hardcoded path or replacing with a generic env-var pattern.

---

## Category 3 — Platform session metadata (userId / teamId UUIDs)

| Severity | File | Line | Pattern | Recommendation |
|---|---|---|---|---|
| MEDIUM | `paper/_peer_review_v2/raw/grok-4-0709.json` | 3-8 | `userId: 70df666d-...`, `teamId: 0c5a019d-...` | Remove or strip from raw JSON — platform account IDs |
| MEDIUM | `paper/_peer_review_v2/raw/gpt-5.4.json` | 3-8 | same userId / teamId | Same |
| MEDIUM | `paper/_peer_review_v2/raw/gemini-3.1-pro-preview.json` | 3-8 | same userId / teamId | Same |
| MEDIUM | `paper/_peer_review_v3/raw/deepseek-chat.json` | 3-8 | same userId / teamId | Same |
| MEDIUM | `paper/_peer_review_v3/raw/qwen3-max.json` | 3-8 | same userId / teamId | Same |
| MEDIUM | `paper/_peer_review_v3/raw/gemini-3.1-pro-preview.json` | 3-8 | same userId / teamId | Same |
| MEDIUM | `paper/_peer_review_v6/run_summary.json` | 4 | userId + teamId in preview field | Same |
| LOW | `paper/_peer_review_v3/run_log.txt` | 15, 18 | `traceId: d1c81d4c...` and `9e45268c...` in error messages | Low risk (trace IDs, not auth tokens), but leave or strip |
| LOW | `paper/peer_pre_review_v3.md` | 31, 33 | same traceIds quoted | Same |

**Assessment:** The userId `70df666d-96f4-4b70-a68d-d15c45bcf218` and teamId `0c5a019d-56f1-4533-b416-1bba79f1f763` appear consistently across 6 raw JSON files. These are internal API account identifiers from a 1min.ai or similar platform. Not credentials, but unintended account fingerprints. Recommend stripping from raw JSON files before public release.

---

## Category 4 — Vast.ai / hardware references

| Severity | File | Line | Pattern | Recommendation |
|---|---|---|---|---|
| LOW | `mcmc/deploy/vast_ai_deploy.md` | 75 | `ssh -p 12345 root@ssh4.vast.ai` | Intentional example command (generic port 12345, standard Vast endpoint) — Leave as-is |
| LOW | `mcmc/deploy/vast_ai_deploy.md` | 107 | `user@storagebox.your-server.de` | Template placeholder, not a real address — Leave |
| LOW | `mcmc/deploy/checkpoint_rsync.sh` | 7-8 | same template placeholders | Leave |
| LOW | `numerics/README.md` | 3 | `~$50` cloud cost estimate | Intentional budget note in public doc — Leave |
| LOW | `paper/chimere_omega/chimere_omega.tex` | 456-457 | hardware spec disclosure (i5-14600KF, RTX 5060 Ti, 16 GB VRAM) | Intentional methodological disclosure — Leave |
| LOW | `mcmc/deploy/preflight_report.md` | 5 | `i5-14600KF, 32 GB RAM, Ubuntu 6.17` | Intentional benchmark context — Leave |

**Assessment:** All hardware/Vast.ai references are either generic templates or intentional methodological disclosures. The hardware specs in `chimere_omega.tex` and MCMC deploy docs are part of reproducibility metadata. No actual rental IDs, real SSH endpoints (only the generic `ssh4.vast.ai` example), or financial account info found.

---

## Category 5 — chimere-server / private repo references

| Severity | File | Line | Pattern | Recommendation |
|---|---|---|---|---|
| LOW | `paper/chimere_omega/chimere_omega.tex` | 54, 312, 457, 472 | `chimere-server` named as inference runtime | Intentional methodological reference in a paper about chimere-server — Leave |
| LOW | `paper/chimere_omega/CITATION.cff` | 25 | `chimere-server` named | Same — Leave |
| LOW | `mcmc/benchmark/compile_flags.md` | 32 | `chimere-server regressions on our side` | Internal dev note in a public benchmark doc — consider rephrasing to neutral language |

---

## Not Found (CLEAN)

- Phone numbers or postal addresses: **none**
- SSN / IBAN patterns: **none**
- Telegram tokens, chat IDs, bot usernames (@Keke_open_claw_bot, @MelanieAgroBot): **none**
- Private IP addresses (10.x, 192.168.x): **none**
- MEMORY.md content committed: **none**
- ~/.claude/ references: **none**
- /tmp/ paths committed: **none**
- KineBot / OpenClaw / agent workflow names in published content: **none** (only in `_run_all.py` and script comments)
- Other users' home directory paths: **none**
- Actual API key values: **none** (only variable names / env-file path references)

---

## Action Priority

| Priority | Action |
|---|---|
| 1 — MEDIUM | Strip `userId` / `teamId` from 6 raw JSON files in `paper/_peer_review_v2/raw/` and `paper/_peer_review_v3/raw/` and `paper/_peer_review_v6/run_summary.json` before any public release of those files |
| 2 — MEDIUM | Replace `~/.openclaw/venvs/pipeline/bin/python` in `_run_all.py` with `sys.executable` or a `PIPELINE_PYTHON` env var |
| 3 — MEDIUM | Redact `~/.openclaw/.env` references in 4 derivation scripts to generic `~/.env` or `os.getenv("MISTRAL_API_KEY")` only |
| 4 — MEDIUM | Update `RESULTS.md` lines 15, 74 to remove `~/.openclaw/` path |
| 5 — LOW | Rephrase `chimere-server regressions on our side` in `mcmc/benchmark/compile_flags.md` |
