#!/usr/bin/env python3
"""v6 JHEP cross-model peer pre-review panel.

Runs 3 frontier models (Qwen3-Max via 1min.ai, Gemini 2.5 Pro via CLI,
Magistral-medium via Mistral API) on the v6 formal-track skeleton and
extracts structured Q1-Q4 responses.

No keys are logged. Outputs: raw/<model>.json + <model>.md.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
TEX = REPO / "paper" / "v6" / "v6_jhep.tex"
RAW = ROOT / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# Load env from ~/.env  # set ENV_FILE to override without logging values
ENV_FILE = Path(os.environ.get("ENV_FILE", Path.home() / ".env"))
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TIMEOUT = 180
GEMINI_TIMEOUT = 420
RETRY_SLEEP = 5

PROMPT_HEAD = """You are a peer reviewer for Journal of High Energy Physics (JHEP). You have been given a 4-page formal-track paper presenting:
 - a differential-inequality upper bound on observer-dependent generalised entropy growth in type-II crossed-product algebras
 - a dequantisation map Tr_R[ρ_R n̂] as bridge between quantum states and classical density fields
 - 3 explicit postulates (M1 Brown-Susskind modular complexity ansatz, M2 CLT for coarse-graining, M3 chameleon profile exponent α = 0.095)
 - no cosmological prediction (companion paper handles phenomenology)

Answer ONLY these 4 questions in 3-5 sentences each:

Q1. Is this a genuinely new formal result, or a rewriting of existing GSL statements (Wall 2011, Faulkner-Speranza 2024, Kirklin 2025)?

Q2. Which of M1, M2, M3 is the weakest postulate? Should any be demoted to "conjecture" or strengthened?

Q3. Referee recommendation: PUBLISH / MINOR REVISIONS / MAJOR REVISIONS / REJECT? Justify in one paragraph.

Q4. One specific additional result the authors could derive (NOT "more rigour" handwaving) that would make the paper stronger. Max 2 sentences.

Be blunt. Assume the author is an independent researcher, no affiliation. Framework/formal paper genre acceptable at JHEP if it provides genuine formal novelty. Do NOT penalise for the absence of cosmological prediction — that is the companion paper's job.

--- Paper text follows ---

"""


def build_prompt() -> str:
    return PROMPT_HEAD + TEX.read_text(encoding="utf-8")


# ---------------- 1min.ai (Qwen3-Max) ----------------

def call_qwen(prompt: str) -> dict:
    key = os.environ.get("ONEMIN_AI_API_KEY")
    if not key:
        return {"error": "no ONEMIN_AI_API_KEY"}
    url = "https://api.1min.ai/api/chat-with-ai"
    body = {
        "type": "UNIFY_CHAT_WITH_AI",
        "model": "deepseek-chat",
        "promptObject": {"prompt": prompt},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "API-KEY": key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "curl/8.5.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read().decode("utf-8", errors="replace")
    try:
        parsed = json.loads(raw)
    except Exception:
        return {"raw": raw}
    return parsed


def extract_qwen(resp: dict) -> str:
    # 1min.ai envelopes vary; try common paths
    if not isinstance(resp, dict):
        return str(resp)
    for path in (
        ("aiRecord", "aiRecordDetail", "resultObject"),
        ("aiRecord", "aiRecordDetail", "result"),
        ("resultObject",),
        ("result",),
        ("choices", 0, "message", "content"),
        ("raw",),
    ):
        cur = resp
        ok = True
        for p in path:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            elif isinstance(cur, list) and isinstance(p, int) and p < len(cur):
                cur = cur[p]
            else:
                ok = False
                break
        if ok:
            if isinstance(cur, list) and cur and isinstance(cur[0], str):
                return "\n".join(cur)
            if isinstance(cur, str):
                return cur
    return json.dumps(resp)[:4000]


# ---------------- Gemini CLI ----------------

def call_gemini(prompt: str) -> dict:
    # gemini CLI reads prompt from stdin with -p ? Actually `gemini` takes
    # prompt as arg or via --prompt. Safer: pipe via stdin to `gemini -p -`.
    try:
        proc = subprocess.run(
            ["gemini", "-m", os.environ.get("GEMINI_MODEL", "gemini-2.5-pro"), "-p", prompt],
            capture_output=True,
            text=True,
            timeout=GEMINI_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except FileNotFoundError:
        return {"error": "gemini CLI not found"}
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr[-2000:],
    }


def extract_gemini(resp: dict) -> str:
    if resp.get("error"):
        return f"[ERROR] {resp['error']}"
    return resp.get("stdout", "").strip() or f"[stderr] {resp.get('stderr','')[:500]}"


# ---------------- Mistral (Magistral-medium) ----------------

def call_magistral(prompt: str) -> dict:
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        return {"error": "no MISTRAL_API_KEY"}
    url = "https://api.mistral.ai/v1/chat/completions"
    body = {
        "model": "magistral-medium-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.3,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def extract_magistral(resp: dict) -> str:
    try:
        msg = resp["choices"][0]["message"]
        # Magistral returns reasoning + content; prefer content, fallback to reasoning
        content = msg.get("content")
        if isinstance(content, list):
            parts = []
            for c in content:
                if isinstance(c, dict):
                    parts.append(c.get("text", ""))
                else:
                    parts.append(str(c))
            content = "\n".join(p for p in parts if p)
        if content:
            return content
        return msg.get("reasoning_content", "") or json.dumps(msg)[:2000]
    except Exception:
        return json.dumps(resp)[:4000]


# ---------------- Driver ----------------

ALL_MODELS = [
    ("deepseek_chat",   call_qwen,      extract_qwen),
    ("gemini_2_5_pro",  call_gemini,    extract_gemini),
    ("magistral_medium", call_magistral, extract_magistral),
]
# Allow filtering via CLI: python run_v6_panel.py qwen3_max gemini_2_5_pro
if len(sys.argv) > 1:
    keep = set(sys.argv[1:])
    MODELS = [m for m in ALL_MODELS if m[0] in keep]
else:
    MODELS = ALL_MODELS


def run_one(name, caller, extractor, prompt):
    last_err = None
    for attempt in (1, 2):
        try:
            print(f"[{name}] attempt {attempt}...", flush=True)
            t0 = time.time()
            resp = caller(prompt)
            dt = time.time() - t0
            print(f"[{name}] got response in {dt:.1f}s", flush=True)
            if isinstance(resp, dict) and resp.get("error") and attempt == 1:
                last_err = resp["error"]
                time.sleep(RETRY_SLEEP)
                continue
            (RAW / f"{name}.json").write_text(json.dumps(resp, indent=2, ensure_ascii=False))
            text = extractor(resp)
            (ROOT / f"{name}.md").write_text(
                f"# {name} review of v6\n\n{text}\n"
            )
            return True, text
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:500]
            last_err = f"HTTP {e.code}: {body}"
            print(f"[{name}] {last_err}", flush=True)
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            print(f"[{name}] {last_err}", flush=True)
        if attempt == 1:
            time.sleep(RETRY_SLEEP)
    (ROOT / f"{name}.md").write_text(
        f"# {name} review of v6\n\n**UNAVAILABLE** — {last_err}\n"
    )
    return False, f"UNAVAILABLE: {last_err}"


def main():
    prompt = build_prompt()
    print(f"Prompt: {len(prompt)} chars", flush=True)
    results = {}
    for i, (name, caller, extractor) in enumerate(MODELS):
        if i > 0:
            time.sleep(RETRY_SLEEP)
        ok, text = run_one(name, caller, extractor, prompt)
        results[name] = {"ok": ok, "preview": text[:300]}
    (ROOT / "run_summary.json").write_text(json.dumps(results, indent=2))
    print("\nDone.", flush=True)


if __name__ == "__main__":
    main()
