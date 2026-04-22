#!/usr/bin/env python3
"""V10 — Adversarial review of v4.6 scientific content via Mistral Magistral-medium.

Four claim prompts sent sequentially (3 s rate-limit, 180 s timeout, 1 retry on 5xx).
Raw responses persisted to _mistral_responses/v10_claim_{1..4}.txt.

API key from ~/.env  # set ENV_FILE to override (MISTRAL_API_KEY). Never logged.
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
OUT = Path(__file__).parent / "_mistral_responses"
OUT.mkdir(exist_ok=True)

PROMPTS = {
    1: """Consider a scalar-tensor theory with action
  S = ∫ d^4x √(-g) [ (M_P²/2) R - (1/2)(∂χ)² - V(χ) - (1/2) ξ_χ R χ² ]
with F(χ) = M_P² - ξ_χ χ². In the sub-horizon quasi-static limit (k ≫ aH) on a flat FRW background, derive:
(a) the effective Newton constant G_eff(a) / G_N;
(b) the gravitational slip η(a) ≡ Φ/Ψ (Weyl potentials).
Expand both to leading order in ξ_χ. State which of G_eff deviation and η deviation is linear in ξ_χ, and which is quadratic. Justify briefly.""",
    2: """Given G_eff/G_N - 1 ≈ ξ_χ χ²/M_P², evaluate the fractional shift in the growth observable fσ₈(z) at z = 0.1, 0.5, 1.0 for ξ_χ = 2.4×10⁻² and χ = M_P/10. Compare to the Euclid/LSST Y10 precision σ(fσ₈) ~ 1% per bin. Conclude whether a Cassini-saturated NMC signature is detectable in near-future LSS.""",
    3: """You want a chameleon-like envelope Θ(ρ) = exp(-(ρ/ρ_c)^α) modulating an NMC coupling ξ_eff(ρ) = ξ_χ · Θ(ρ), with ξ_χ = 2.4×10⁻² at cosmological density ρ_cosm ≈ 10⁻²⁹ g/cm³, and a Cassini solar-system suppression requiring Θ(10 g/cm³) ≤ 10⁻³. What is the minimum (α, ρ_c) pair that saturates both bounds? Give numerical values.

Boundary conditions to saturate:
 (R1) Θ(ρ_☉ = 10 g/cm³) = 10⁻³  (Cassini ceiling)
 (R2) Θ(ρ_cosm = 10⁻²⁹ g/cm³) = 0.99  (cosmological visibility floor, preserves ~1% D7 thawing-DE signature)

Show all derivation steps including: (i) taking ratios of the two saturation equations to isolate α; (ii) numerically solving for α; (iii) back-substituting to get ρ_c. Give final values to 3 sig figs.""",
    4: """A framework paper in cosmology/quantum gravity introduces 6 axioms. Peer reviewers from three model families unanimously identify one axiom (Cryptographic Censorship transposed from AdS/CFT to de Sitter cosmology) and its supporting "toy dictionary" as the weakest content. The authors keep the dictionary but demote it from a main-body section to a clearly-labelled "Speculative" appendix. Is this the correct editorial response? Justify in 3-5 sentences.""",
}


def load_env_key() -> str | None:
    # Prefer env; else parse ~/.env  # set ENV_FILE to override
    k = os.getenv("MISTRAL_API_KEY")
    if k:
        return k
    env_path = Path(os.environ.get("ENV_FILE", Path.home() / ".env"))
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?MISTRAL_API_KEY\s*=\s*(.+?)\s*$", line)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                return v
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
        print("ERROR: MISTRAL_API_KEY not found in env or ~/.env  # set ENV_FILE to override", file=sys.stderr)
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
            (OUT / f"v10_claim_{i}.txt").write_text(f"UNAVAILABLE: {type(e).__name__}: {e}\n")
            time.sleep(3)
            continue
        dt = time.time() - t0
        content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
        content = flatten(content)
        if not content or not content.strip():
            print(f"  WARN: empty content claim {i}", file=sys.stderr)
        (OUT / f"v10_claim_{i}.txt").write_text(content)
        (OUT / f"v10_claim_{i}_full.json").write_text(json.dumps(msg, indent=2, default=str))
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
    (OUT / "_v10_usage.json").write_text(
        json.dumps(
            {"model": MODEL, "usage": total_usage, "cost_usd": cost, "status": status},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
