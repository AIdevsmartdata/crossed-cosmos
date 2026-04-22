#!/usr/bin/env python3
"""3-model frontier peer pre-review v2 via 1min.ai aggregator."""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)

API_URL = "https://api.1min.ai/api/chat-with-ai"
API_KEY = os.environ.get("ONEMIN_AI_API_KEY")
if not API_KEY:
    print("ERROR: ONEMIN_AI_API_KEY not set (source ~/.env  # set ENV_FILE to override first)", file=sys.stderr)
    sys.exit(1)

MODELS = [
    ("gpt-5.4", "OpenAI GPT-5.4"),
    ("gemini-3.1-pro-preview", "Google Gemini 3.1 Pro"),
    ("grok-4-0709", "xAI Grok 4"),
]

# --- Concatenate LaTeX, resolving \input ---
def resolve_inputs(tex_path: Path) -> str:
    text = tex_path.read_text()
    def repl(m):
        name = m.group(1)
        if not name.endswith(".tex"):
            name += ".tex"
        target = tex_path.parent / name
        if target.exists():
            return f"% === BEGIN \\input{{{name}}} ===\n" + target.read_text() + f"\n% === END \\input{{{name}}} ==="
        return m.group(0)
    return re.sub(r"\\input\{([^}]+)\}", repl, text)

concat = resolve_inputs(PAPER / "eci.tex")
print(f"[info] concatenated LaTeX: {len(concat)} bytes")

PROMPT_HEADER = """You are a peer reviewer for European Physical Journal C (EPJ C). You have been given a short framework paper synthesizing six established results in cosmology and quantum gravity.

Answer ONLY these 4 questions, 3-5 sentences each:

Q1. What is the single WEAKEST claim in this paper, and why?
Q2. What is the single STRONGEST claim in this paper, and why?
Q3. Referee recommendation: PUBLISH as-is / MINOR REVISIONS / MAJOR REVISIONS / REJECT? Justify in one paragraph.
Q4. One specific additional calculation or derivation (not broad "more MCMC") that would most strengthen falsifiability. Max 2 sentences.

Be blunt. Indie-author paper, no affiliation. Framework-paper genre acceptable at EPJ C.

--- Paper follows ---

"""

FULL_PROMPT = PROMPT_HEADER + concat

def call_model(model_id: str, timeout: int = 120):
    body = json.dumps({
        "type": "UNIFY_CHAT_WITH_AI",
        "model": model_id,
        "promptObject": {"prompt": FULL_PROMPT},
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "API-KEY": API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "curl/8.5.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8")), resp.status

def extract_text(payload) -> str:
    try:
        rec = payload.get("aiRecord", {}).get("aiRecordDetail", {})
        obj = rec.get("resultObject", [])
        if isinstance(obj, list):
            return "\n".join(str(x) for x in obj)
        return str(obj)
    except Exception as e:
        return f"[extract failed: {e}]\n{json.dumps(payload)[:2000]}"

results = {}
for i, (mid, label) in enumerate(MODELS):
    if i > 0:
        time.sleep(3)
    print(f"[{i+1}/3] {mid} ({label}) ...", flush=True)
    attempt = 0
    last_err = None
    while attempt < 2:
        attempt += 1
        try:
            t0 = time.time()
            payload, status = call_model(mid)
            dt = time.time() - t0
            print(f"    -> HTTP {status} in {dt:.1f}s", flush=True)
            (RAW / f"{mid}.json").write_text(json.dumps(payload, indent=2))
            text = extract_text(payload)
            (HERE / f"{mid}.md").write_text(f"# {label} ({mid})\n\n{text}\n")
            results[mid] = {"status": "ok", "label": label, "text": text, "raw": payload}
            break
        except urllib.error.HTTPError as e:
            last_err = f"HTTPError {e.code}: {e.reason}"
            print(f"    ! {last_err}", flush=True)
            if 500 <= e.code < 600 and attempt < 2:
                time.sleep(5)
                continue
            break
        except (urllib.error.URLError, TimeoutError, Exception) as e:
            last_err = f"{type(e).__name__}: {e}"
            print(f"    ! {last_err}", flush=True)
            if attempt < 2:
                time.sleep(5)
                continue
            break
    else:
        pass
    if mid not in results:
        results[mid] = {"status": "unavailable", "label": label, "error": last_err}
        (HERE / f"{mid}.md").write_text(f"# {label} ({mid})\n\n[UNAVAILABLE] {last_err}\n")

# Summary (no secrets)
summary = {
    mid: {"status": r["status"], "label": r["label"],
          "chars": len(r.get("text", "")) if r["status"] == "ok" else 0,
          "error": r.get("error")}
    for mid, r in results.items()
}
(HERE / "run_summary.json").write_text(json.dumps(summary, indent=2))
print("[done]", json.dumps(summary, indent=2))
