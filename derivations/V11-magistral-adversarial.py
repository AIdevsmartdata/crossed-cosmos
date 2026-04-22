#!/usr/bin/env python3
"""V11 — Adversarial review of v4.7.0 via Mistral Magistral-medium.

Three claim prompts:
  1. Abstract clause (v) tone check — Cryptographic Censorship status.
  2. §1.5 Team B thesis defensibility — late-time quasi-dS specialisation.
  3. Observer-frame qualifier propagation integrity — §3.5/§3.6/§A6/App A.

Rate-limit 3 s, timeout 180 s, retry once on 5xx. Raw responses to
_mistral_responses/v11_claim_{1,2,3}.txt. API key from ~/.env  # set ENV_FILE to override
(MISTRAL_API_KEY). Never logged.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
MODEL = "magistral-medium-latest"
HERE = Path(__file__).parent
OUT = HERE / "_mistral_responses"
OUT.mkdir(exist_ok=True)

SECTION_15 = (HERE.parent / "paper" / "section_1_5_thesis_B.tex").read_text()

CLAIM_1 = """Read the following abstract passage from a cosmology framework paper and answer: does the passage overstate the evidential status of "Cryptographic Censorship"? Specifically, does it read as if A3 (a working conjecture) is now supported by a proven dictionary, or does it correctly convey that A3 remains a working conjecture whose cosmological transposition is speculative?

Passage:
"(v) Cryptographic Censorship as a working-conjecture bulk-geometry criterion, linked through the observer-dependent reading of A1 (§1.5) and made operational through an explicit toy dS/FLRW dictionary (Appendix A), [MaHuang2025]"

Respond in 4-6 sentences. Be blunt."""

CLAIM_2 = f"""Read the attached one-page §1.5 draft of a cosmology framework paper. It argues that the type-II crossed-product construction of Chandrasekaran-Longo-Penington-Witten 2023 (CFT observables for de Sitter) and De Vuyst-Eccles-Höhn-Kirklin 2024-2025 (crossed product + QRF) can be specialised to a "late-time quasi-de Sitter regime" and used as a unifying observer-dependent framework for the paper's six axioms.

Is this specialisation scientifically honest and publishable in EPJ C as a framework paper? In particular: (a) is the matter-era concession unavoidable? (b) does it buy anything predictive?

{SECTION_15}

Respond in 6-10 sentences. Be blunt."""

CLAIM_3 = """The paper's §3.5 adds "(solar-system observer frame)" to its Cassini PPN bound; §3.6 adds "(causal-diamond regime of a single geodesic observer)" to its Swampland EFT bound; §A6 adds "(observer ensemble average)" to the Matsubara Euler-characteristic shift; Appendix A adds a sentence linking Cryptographic Censorship's working-conjecture status to the QRF subregion of the observer's crossed product. These are all prose-level additions; no numerical value moves.

Do these qualifiers change the paper's predictive content? Does any of them open a consistency gap between the §1.5 thesis and the numerical §3 predictions? Or are they scope-conservative?

Respond in 4-6 sentences. Be blunt."""

PROMPTS = {1: CLAIM_1, 2: CLAIM_2, 3: CLAIM_3}


def load_env_key() -> str | None:
    k = os.getenv("MISTRAL_API_KEY")
    if k:
        return k
    env_path = Path(os.environ.get("ENV_FILE", Path.home() / ".env"))
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?MISTRAL_API_KEY\s*=\s*(.+?)\s*$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return None


def call_mistral(prompt: str, api_key: str, retries: int = 1):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 10000,
        "temperature": 0.2,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode("utf-8"))
                return data["choices"][0]["message"], data.get("usage", {})
        except urllib.error.HTTPError as e:
            last_err = e
            if 500 <= e.code < 600 and attempt < retries:
                time.sleep(3)
                continue
            raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(3)
                continue
            raise
    raise RuntimeError(f"unreachable: {last_err}")


def flatten(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        for k in ("text", "thinking", "content"):
            if k in x:
                return flatten(x[k])
        return json.dumps(x)
    if isinstance(x, list):
        return "\n\n".join(flatten(b) for b in x)
    return str(x)


def main() -> int:
    api_key = load_env_key()
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not found", file=sys.stderr)
        return 1

    total_usage = {"prompt_tokens": 0, "completion_tokens": 0}
    status = {}
    for i in sorted(PROMPTS.keys()):
        print(f"[claim {i}] calling Magistral...")
        t0 = time.time()
        try:
            msg, usage = call_mistral(PROMPTS[i], api_key)
        except Exception as e:
            print(f"  FAIL claim {i}: {type(e).__name__}: {e}", file=sys.stderr)
            status[i] = "UNAVAILABLE"
            (OUT / f"v11_claim_{i}.txt").write_text(f"UNAVAILABLE: {type(e).__name__}: {e}\n")
            time.sleep(3)
            continue
        dt = time.time() - t0
        content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
        content = flatten(content)
        if not content or not content.strip():
            print(f"  WARN: empty content claim {i}", file=sys.stderr)
        (OUT / f"v11_claim_{i}.txt").write_text(content)
        (OUT / f"v11_claim_{i}_full.json").write_text(json.dumps(msg, indent=2, default=str))
        total_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
        total_usage["completion_tokens"] += usage.get("completion_tokens", 0)
        status[i] = "OK"
        print(f"  {len(content)} chars, {dt:.1f}s, usage={usage}")
        time.sleep(3)

    cost = (
        total_usage["prompt_tokens"] * 2e-6
        + total_usage["completion_tokens"] * 5e-6
    )
    print(f"Total usage: {total_usage}")
    print(f"Estimated cost: ${cost:.4f}")
    (OUT / "_v11_usage.json").write_text(
        json.dumps(
            {"model": MODEL, "usage": total_usage, "cost_usd": cost, "status": status},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
