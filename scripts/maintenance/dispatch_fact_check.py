#!/usr/bin/env python3
"""Dispatch DS Pro V4 fact-check wave on all papers in parallel.

For each paper main.tex:
  - Send to DS Pro V4 high-reasoning
  - Prompt: verify arXiv IDs, equations, attributions, flag fabrications
  - Output JSON report → /tmp/fact_check_reports/<paper>.json

Max parallel: 20 (conservative for API rate limits)
"""
import subprocess
import json
import pathlib
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

PAPERS_ROOT = pathlib.Path("/root/cc-private/papers")
REPORTS_DIR = pathlib.Path("/tmp/fact_check_reports_2026-05-19")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

MAX_PARALLEL = 20
MAX_INPUT_CHARS = 30000   # truncate paper if too long

SYSTEM_PROMPT = """You are an Inventiones/Annals reviewer with PhD-level rigor.
Your task: fact-check a research paper draft. Output STRICT JSON only.

Default stance: SKEPTICAL. Flag anything dubious.

JSON schema:
{
  "paper_id": "<from prompt>",
  "verdict": "READY_TO_SUBMIT | NEEDS_PATCHES | REJECT",
  "arxiv_ids_to_verify": ["1234.5678", ...],
  "suspect_attributions": [
    {"claim": "<verbatim quote>", "issue": "<what's wrong>", "line_hint": "<approximate>"},
    ...
  ],
  "equation_issues": [
    {"equation": "<latex>", "issue": "<what's wrong>"},
    ...
  ],
  "scope_overclaims": [
    {"claim": "<verbatim>", "actual_scope": "<correction>"},
    ...
  ],
  "missing_citations": [
    {"claim": "<context>", "needs_cite": "<what to cite>"},
    ...
  ],
  "minor_polish": [
    "<bullet point>",
    ...
  ],
  "confidence": "HIGH | MEDIUM | LOW"
}

Be CONCISE in messages but COMPLETE in findings. Quote verbatim when flagging."""


def check_paper(paper_path):
    paper_id = paper_path.parent.name
    out_path = REPORTS_DIR / f"{paper_id}.json"
    if out_path.exists():
        return paper_id, "SKIP (already done)"

    try:
        content = paper_path.read_text(encoding="utf-8", errors="ignore")
        if len(content) > MAX_INPUT_CHARS:
            content = content[:MAX_INPUT_CHARS] + "\n\n[TRUNCATED]"
    except Exception as e:
        return paper_id, f"ERROR reading: {e}"

    user_prompt = f"""Paper ID: {paper_id}

Fact-check this paper. Identify all issues. Output strict JSON per schema.

PAPER CONTENT:
---
{content}
---
"""

    try:
        proc = subprocess.run(
            [
                "python3", "/root/bin/deepseek.py",
                "--model", "deepseek-v4-pro",
                "--reasoning-effort", "medium",
                "--system", SYSTEM_PROMPT,
                "--json",
                "--max-tokens", "12000",
                user_prompt,
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if proc.returncode != 0:
            err = (proc.stderr or "")[:500]
            return paper_id, f"FAIL rc={proc.returncode}: {err}"

        # Save raw output
        out_path.write_text(proc.stdout)
        return paper_id, "OK"
    except subprocess.TimeoutExpired:
        return paper_id, "TIMEOUT"
    except Exception as e:
        return paper_id, f"EXC: {e}"


def main():
    papers = sorted(
        p for p in PAPERS_ROOT.rglob("main.tex")
        if "archive" not in p.parts
    )
    print(f"Found {len(papers)} papers to fact-check.")
    print(f"Dispatching with {MAX_PARALLEL} parallel DS Pro V4 workers...")
    print(f"Output: {REPORTS_DIR}")
    print()

    success = 0
    fail = 0
    skip = 0
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as ex:
        futures = {ex.submit(check_paper, p): p for p in papers}
        for i, fut in enumerate(as_completed(futures), 1):
            paper_id, status = fut.result()
            print(f"[{i:3d}/{len(papers)}] {paper_id:50s} {status}")
            if status == "OK":
                success += 1
            elif status.startswith("SKIP"):
                skip += 1
            else:
                fail += 1

    print()
    print(f"OK: {success} | SKIP: {skip} | FAIL: {fail}")
    print(f"Reports: {REPORTS_DIR}/")


if __name__ == "__main__":
    main()
