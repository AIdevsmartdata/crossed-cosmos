#!/usr/bin/env python3
"""V12 — Final adversarial review of v5.0 delta via Mistral Magistral-medium.

Three claim prompts (verbatim from v5.0 gate):
  1. MCMC integration honesty (D17 → §3.5 / §4 / abstract).
  2. §3.6 Swampland × NMC cross-constraint rigor (16 orders claim).
  3. A3 appendix quarantine sufficiency.

Rate-limit 3 s, timeout 180 s, retry once on 5xx. Raw responses to
_mistral_responses/v12_claim_{1,2,3}.txt. API key from ~/.env  # set ENV_FILE to override
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

CLAIM_1 = """A cosmology framework paper has just completed a 4-chain MPI MCMC on DESI DR2 BAO + Pantheon+ SN (no CMB likelihood), converged at R-1 = 0.036. The posterior on the non-minimal coupling parameter xi_chi is:

xi_chi = 0.003 +0.065/-0.070 (68% CL), |xi_chi| < 0.095 (95% CL)

This is essentially the prior [-0.1, 0.1]. The Bayes factor vs LCDM is BF_{01} ~ 1.00. The Delta chi^2 = -0.04.

The paper's section 3.5 now quotes these numbers, stating that the DR2+SN posterior is consistent with zero, that Cassini (|xi_chi| <= 2.4e-2) remains 600x tighter, and that the joint CMB+NMC analysis is deferred to v5.1 via the hi_class patch.

Is this presentation scientifically honest, or does it overstate/understate the result? Be blunt."""

CLAIM_2 = """The paper's section 3.6 adopts a Swampland x NMC cross-constraint giving |xi_chi| <= 8.4e-19 at c' = 1/6 (species scale) with chi_0 = M_P/10, i.e. 16 orders of magnitude tighter than Cassini. This relies on a heuristic delta M_P^2 <= Lambda^2 step, stated as such in the prose (the word "heuristic" appears three times). A parallel approach (arXiv:2512.07929) derives SDC from frame covariance and is cited as complementary.

Is the 16-orders-of-magnitude claim defensible as "a working conjecture under the bulk-mode hypothesis" as the paper states, or is it oversold? Should it be demoted further?"""

CLAIM_3 = """The paper's A3 axiom (Cryptographic Censorship transposed from AdS/CFT to FLRW) is flagged as a "working conjecture" in the main body, with a toy dictionary in an Appendix A explicitly labeled "Speculative". Three peer-pre-review rounds (including Claude + Gemini + Magistral + GPT-5.4 + Grok 4 + Qwen3 Max + DeepSeek) all identified A3 as the weakest axiom. The quarantine to appendix is the paper's response.

Is this editorial move sufficient, or should A3 be removed entirely for v5.0 submission?"""

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
            (OUT / f"v12_claim_{i}.txt").write_text(f"UNAVAILABLE: {type(e).__name__}: {e}\n")
            time.sleep(3)
            continue
        dt = time.time() - t0
        content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
        content = flatten(content)
        if not content or not content.strip():
            print(f"  WARN: empty content claim {i}", file=sys.stderr)
        (OUT / f"v12_claim_{i}.txt").write_text(content)
        (OUT / f"v12_claim_{i}_full.json").write_text(json.dumps(msg, indent=2, default=str))
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
    (OUT / "_v12_usage.json").write_text(
        json.dumps(
            {"model": MODEL, "usage": total_usage, "cost_usd": cost, "status": status},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
