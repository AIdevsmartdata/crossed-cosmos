#!/usr/bin/env python3
"""V6b — Cross-model adversarial review with Mistral Magistral-medium.

Parallel to V6 (mistral-large-latest). Magistral is Mistral's reasoning-specialised
model with visible chain-of-thought, meant to catch errors a generalist pass misses.

Prompts are V6b-specific (explicit 'Think step by step' + 'Show all derivation steps').

API key must be in environment (MISTRAL_API_KEY). NEVER logged.
"""
from __future__ import annotations

import json
import os
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
    1: """Think step by step. Consider the action
  S = ∫ d^4 x √(-g) [ (M_P^2 / 2) R - (1/2)(∂χ)^2 - V(χ) - (1/2) ξ R χ^2 ]
in mostly-plus signature and reduced Planck mass convention.

Derive the PPN parameter γ − 1 in the weak-field, static limit, keeping only leading order in ξ and in χ_0 / M_P where χ_0 is the background scalar value.

Then, using the Cassini bound γ − 1 = (2.1 ± 2.3) × 10^{-5} (Bertotti, Iess, Tortora 2003), compute the maximum |ξ| allowed for χ_0 = M_P / 10.

Show all derivation steps. Do not consult the web; work from standard PPN formalism.""",
    2: """Think step by step. In standard minimal-coupling thawing quintessence (Scherrer & Sen 2008) with exponential potential V = V_0 exp(-α χ / M_P), the CPL (w_0, w_a) relation at matter-dark-energy crossover is
  w_a ≈ -1.58 (1 + w_0)  at Ω_Λ ≈ 0.7.

Now include a non-minimal coupling ξ R χ^2 / 2. At first order in ξ, what is w_a(w_0; ξ, χ_0 / M_P)? Derive the correction term symbolically, showing the ODE manipulations.

Do not consult the web.""",
    3: """Think step by step. In the Dark Dimension scenario (Montero, Vafa, Valenzuela 2022), the EFT species-scale cutoff is
  Λ_species(H) ≈ M_P (H / M_P)^{c'}, c' = 1/6.

If a non-minimally-coupled scalar χ with coupling (1/2) ξ R χ^2 is a bulk mode of the dark sector sharing this cutoff, derive the EFT constraint on ξ at H = H_0 (today) for χ_0 = M_P/10. Use the heuristic condition that the shift in the effective Planck mass must not exceed the cutoff squared, i.e. δM_P^2 ≤ Λ^2.

Compute Λ(H_0) and the resulting |ξ| bound numerically. H_0 ≈ 67 km/s/Mpc, M_P = 2.435 × 10^18 GeV.

Do not consult the web.""",
    4: """Think step by step. Two standard results from scalar-tensor cosmology to verify:

(A) For the Jordan-frame action
  S = ∫ √(-g) [ (1/2) M_P^2 R - (1/2) (∂χ)^2 - V(χ) - (1/2) ξ R χ^2 ]
what is the no-ghost (no negative-kinetic-energy) condition on (M_P, ξ, χ)? Derive from the kinetic matrix.

(B) For minimally-coupled exponential quintessence V(χ) = V_0 exp(-α χ / M_P), derive the condition on α for a late-time accelerating scalar-dominated attractor. Show w_φ at the fixed point as a function of α. For which α is the fixed point exactly de Sitter (w = -1)?

Do not consult the web.""",
}


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


def main() -> int:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not in env", file=sys.stderr)
        return 1

    total_usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for i in sorted(PROMPTS.keys()):
        print(f"[claim {i}] calling Magistral...")
        t0 = time.time()
        msg, usage = call_mistral(PROMPTS[i], api_key)
        dt = time.time() - t0
        # Magistral returns content; reasoning/CoT may be in 'content' (interleaved)
        # or a separate field depending on API. Persist the whole message object.
        content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
        # Some Magistral responses use a list of content blocks; flatten to text.
        def flatten(x):
            if isinstance(x, str):
                return x
            if isinstance(x, dict):
                # common keys: text, thinking, content
                for k in ("text", "thinking", "content"):
                    if k in x:
                        return flatten(x[k])
                return json.dumps(x)
            if isinstance(x, list):
                return "\n\n".join(flatten(b) for b in x)
            return str(x)
        content = flatten(content)
        if not content or not content.strip():
            print(f"  WARN: empty content claim {i}", file=sys.stderr)
        (OUT / f"magistral_claim_{i}.txt").write_text(content)
        # Save full message too for CoT inspection if present
        (OUT / f"magistral_claim_{i}_full.json").write_text(json.dumps(msg, indent=2, default=str))
        total_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
        total_usage["completion_tokens"] += usage.get("completion_tokens", 0)
        print(f"  {len(content)} chars, {dt:.1f}s, usage={usage}")
        time.sleep(3)

    # Magistral-medium pricing: ~$2/M in, $5/M out (per memory note)
    cost = (
        total_usage["prompt_tokens"] * 2e-6
        + total_usage["completion_tokens"] * 5e-6
    )
    print(f"Total usage: {total_usage}")
    print(f"Estimated cost: ${cost:.4f}")
    (OUT / "_magistral_usage.json").write_text(
        json.dumps({"model": MODEL, "usage": total_usage, "cost_usd": cost}, indent=2)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
