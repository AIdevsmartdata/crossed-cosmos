#!/usr/bin/env python3
"""V6 — Independent derivation attempt of ECI v6 composite equation via Magistral-medium.

Three questions probing (Q1) variational derivation from crossed-product first law,
(Q2) Krylov→k-design complexity shift, (Q3) dimensional analysis of κ_R.

Raw responses persisted to _mistral_responses/v6_q{1,2,3}.txt.
API key from ~/.env  # set ENV_FILE to override (MISTRAL_API_KEY). Never logged.
Rate-limit 3s, timeout 240s, 1 retry on 5xx.
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
    1: """Consider Faulkner-Speranza crossed-product Type II algebras in de Sitter, where an observer R sees a generalised entropy S_gen[R] = A/(4 G_N) + S_matter as a functor on QRFs. The modular Hamiltonian flows states in proper modular time τ_R.

Propose a physically motivated first-law-like identity of the form:
  dS_gen[R] / dτ_R = (some source term)

Starting from the crossed-product first law, show step by step how one could obtain:
  dS_gen[R] / dτ_R = κ_R · C(ρ_R) · Θ(δn)
where C is a complexity functional, Θ is a scalar modulation, and κ_R is observer-dep.

Does this derivation close rigorously under any reasonable assumption? Show your work. Be honest about handwaves.""",
    2: """In Fan 2022 (JHEP 08 (2022) 232) one has the Krylov inequality |∂_t S_K| ≤ 2 b_1 ΔS_K with S_K ∼ ln C_K in the linear-growth regime of Krylov complexity. That gives effectively Ṡ ≈ Ċ/C, a logarithmic form.

Can you obtain instead a linear form Ṡ ∝ C (not Ṡ ∝ Ċ/C) by:
(a) replacing C_K with the k-design complexity C_k?
(b) restricting to a post-scrambling but pre-saturation regime?
(c) modulating by an "activation function" Θ that suppresses the contribution away from the chaotic regime?

Identify precisely which step is rigorous and which is heuristic.""",
    3: """Given [S_gen] = nat, [τ] = seconds, [C_k] = dimensionless, [Θ] = dimensionless. Then [κ_R] must be nat/s.

Among the following candidates for κ_R, which is physically most defensible, and why:
(i) κ_R = 1/τ_scrambling (inverse scrambling time of the observer's patch)
(ii) κ_R = 2π T_R (modular temperature, de Sitter thermal)
(iii) κ_R = Haferkamp linear-growth rate c in C(t) ≥ c t

Also check: is the combination κ_R · C_k · Θ positive, reflecting the expected dS_gen ≥ 0?""",
}


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
        "max_tokens": 12000,
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
            with urllib.request.urlopen(req, timeout=240) as r:
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
        print(f"[q{i}] calling Magistral...")
        t0 = time.time()
        try:
            msg, usage = call_mistral(PROMPTS[i], api_key)
        except Exception as e:
            print(f"  FAIL q{i}: {type(e).__name__}: {e}", file=sys.stderr)
            status[i] = "UNAVAILABLE"
            (OUT / f"v6_q{i}.txt").write_text(f"UNAVAILABLE: {type(e).__name__}: {e}\n")
            time.sleep(3)
            continue
        dt = time.time() - t0
        content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
        content = flatten(content)
        (OUT / f"v6_q{i}.txt").write_text(content)
        (OUT / f"v6_q{i}_full.json").write_text(json.dumps(msg, indent=2, default=str))
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
    (OUT / "_v6_derivation_usage.json").write_text(
        json.dumps(
            {"model": MODEL, "usage": total_usage, "cost_usd": cost, "status": status},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
