#!/usr/bin/env python3
"""Peer pre-review v3 — 3 credit-light models via 1min.ai aggregator."""
import json, os, re, sys, time, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path("/home/remondiere/crossed-cosmos/paper")
OUT = ROOT / "_peer_review_v3"
RAW = OUT / "raw"
RAW.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("ONEMIN_AI_API_KEY")
if not API_KEY:
    print("ERROR: ONEMIN_AI_API_KEY not set", file=sys.stderr); sys.exit(1)

URL = "https://api.1min.ai/api/chat-with-ai"
MODELS = ["qwen3-max", "gemini-3.1-pro-preview", "deepseek-chat"]

def load_tex(p):
    return p.read_text(encoding="utf-8")

# Resolve \input in eci.tex manually by replacing with concatenation of section files explicitly listed.
eci = load_tex(ROOT / "eci.tex")
s35 = load_tex(ROOT / "section_3_5_constraints.tex")
s36 = load_tex(ROOT / "section_3_6_swampland_cross.tex")
s37 = load_tex(ROOT / "section_3_7_perturbations.tex")
s5A = load_tex(ROOT / "section_5_A3_dictionary.tex")

# Substitute \input directives
eci_resolved = eci
for name, content in [
    ("section_3_5_constraints", s35),
    ("section_3_6_swampland_cross", s36),
    ("section_3_7_perturbations", s37),
    ("section_5_A3_dictionary", s5A),
]:
    eci_resolved = eci_resolved.replace(f"\\input{{{name}}}", content)

PROMPT_HEADER = """You are a peer reviewer for European Physical Journal C (EPJ C). You have been given a short framework paper synthesizing six established results in cosmology and quantum gravity.

Answer ONLY these 4 questions, 3–5 sentences each:

Q1. What is the single WEAKEST claim in this paper, and why?
Q2. What is the single STRONGEST claim in this paper, and why?
Q3. Referee recommendation: PUBLISH as-is / MINOR REVISIONS / MAJOR REVISIONS / REJECT? Justify.
Q4. One specific additional calculation or derivation (not broad "more MCMC") that would most strengthen falsifiability. Max 2 sentences.

Be blunt. Indie-author paper, no affiliation. Framework-paper genre acceptable at EPJ C.

--- Paper follows ---

"""

full_prompt = PROMPT_HEADER + eci_resolved
print(f"Prompt length: {len(full_prompt):,} chars ({len(full_prompt)//4:,} approx tokens)")

def call(model, prompt, timeout=120):
    body = json.dumps({
        "type": "UNIFY_CHAT_WITH_AI",
        "model": model,
        "promptObject": {"prompt": prompt},
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "API-KEY": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "curl/8.5.0",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def extract(resp):
    try:
        ro = resp["aiRecord"]["aiRecordDetail"]["resultObject"]
        if isinstance(ro, list):
            return "\n".join(str(x) for x in ro)
        return str(ro)
    except Exception as e:
        return f"[EXTRACTION ERROR: {e}]\n{json.dumps(resp)[:2000]}"

results = {}
for i, m in enumerate(MODELS):
    if i > 0:
        time.sleep(3)
    print(f"[{i+1}/3] {m} ...", flush=True)
    t0 = time.time()
    last_err = None
    for attempt in range(2):
        try:
            resp = call(m, full_prompt)
            dt = time.time() - t0
            print(f"  OK in {dt:.1f}s", flush=True)
            (RAW / f"{m}.json").write_text(json.dumps(resp, indent=2), encoding="utf-8")
            text = extract(resp)
            (RAW / f"{m}.md").write_text(text, encoding="utf-8")
            results[m] = {"ok": True, "text": text, "dt": dt, "raw": resp}
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, Exception) as e:
            last_err = e
            code = getattr(e, "code", None)
            print(f"  attempt {attempt+1} error: {type(e).__name__} {code} {str(e)[:200]}", flush=True)
            if attempt == 0:
                time.sleep(5)
            else:
                results[m] = {"ok": False, "text": f"[FAIL: {type(e).__name__}: {str(e)[:500]}]", "dt": time.time()-t0}

summary = OUT / "run_log.txt"
with summary.open("w") as f:
    for m, r in results.items():
        f.write(f"=== {m} ok={r['ok']} dt={r.get('dt',0):.1f}s ===\n")
        f.write(r["text"][:4000] + "\n\n")

print("DONE. raw files in", RAW)
