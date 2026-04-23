"""
multi_backend_crosscheck.py — unified triangulation across Mistral + Gemini + local Qwen.

Runs the three `*_crosscheck.py` siblings in parallel against the same
prompt and returns a dict:
{
  "prompt": ...,
  "responses": {
     "mistral":   {"content": ..., "wall_s": ..., "backend": ...},
     "gemini":    {"content": ..., "wall_s": ..., "backend": ...},
     "qwen":      {"content": ..., "wall_s": ..., "backend": ...},
  },
  "consensus":   {"agree_pairs": [...], "median_length_chars": ...},
}

Used for adversarial audits (as we did in this session for F-6 PH↔HP,
Form A vs B, Chandrasekaran-Flanagan authorship, etc.).

Usage:
    from multi_backend_crosscheck import triangulate
    result = triangulate("Is Pinsker's inequality used in Ceyhan-Faulkner 2020?")
    for k, v in result['responses'].items():
        print(f"{k}: {v['content'][:400]}")

    # Shell (prints JSON to stdout):
    python3 derivations/multi_backend_crosscheck.py "Your question"
"""
from __future__ import annotations
import concurrent.futures as cf
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).resolve().parent


def _load(name: str):
    """Dynamically import a sibling *_crosscheck.py without needing package
    wiring."""
    path = _HERE / f"{name}_crosscheck.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"{name}_cc", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _call_mistral(prompt: str, timeout: int, max_tokens: int,
                  temperature: float) -> dict:
    m = _load("mistral")
    if m is None:
        return {"error": "mistral_crosscheck.py not found"}
    try:
        # mistral_crosscheck.py is a script, not an importable function —
        # it runs at import time. Fall back to subprocess.
        return _subprocess_call("mistral_crosscheck.py", prompt, timeout)
    except Exception as e:
        return {"error": f"mistral: {e}"}


def _call_gemini(prompt: str, timeout: int, **_) -> dict:
    m = _load("gemini")
    if m is None:
        return {"error": "gemini_crosscheck.py not found"}
    try:
        return m.crosscheck(prompt, timeout=timeout)
    except Exception as e:
        return {"error": f"gemini: {e}"}


def _call_qwen(prompt: str, timeout: int, max_tokens: int,
               temperature: float) -> dict:
    m = _load("qwen")
    if m is None:
        return {"error": "qwen_crosscheck.py not found"}
    try:
        return m.crosscheck(prompt, timeout=timeout, max_tokens=max_tokens,
                            temperature=temperature)
    except Exception as e:
        return {"error": f"qwen: {e}"}


def _subprocess_call(script: str, prompt: str, timeout: int) -> dict:
    """Fallback for scripts that run side-effects at import time."""
    import subprocess
    import time
    t0 = time.time()
    r = subprocess.run(
        ["python3", str(_HERE / script), prompt],
        capture_output=True, text=True, timeout=timeout,
    )
    if r.returncode != 0:
        return {"error": f"{script} exit {r.returncode}: {r.stderr[:200]}",
                "wall_s": round(time.time() - t0, 2)}
    return {"backend": script.replace("_crosscheck.py", ""),
            "content": r.stdout.strip(),
            "wall_s": round(time.time() - t0, 2)}


def triangulate(prompt: str, *, timeout: int = 240, max_tokens: int = 2000,
                temperature: float = 0.3,
                backends: Optional[list[str]] = None) -> dict:
    """Run the three backends in parallel. If a backend is unavailable it
    returns {'error': ...}; the others still complete. The consensus
    section is a cheap heuristic (length similarity); a real consensus
    check should use a dedicated 4th call to an LLM-as-judge."""
    if backends is None:
        backends = ["mistral", "gemini", "qwen"]
    dispatch = {
        "mistral": _call_mistral,
        "gemini": _call_gemini,
        "qwen": _call_qwen,
    }
    responses: dict = {}
    with cf.ThreadPoolExecutor(max_workers=len(backends)) as pool:
        futures = {pool.submit(dispatch[b], prompt, timeout,
                               max_tokens=max_tokens,
                               temperature=temperature): b
                   for b in backends if b in dispatch}
        for f in cf.as_completed(futures):
            responses[futures[f]] = f.result()

    # Cheap consensus heuristic: pairwise length-ratio ≥ 0.5
    lengths = {k: len(v.get("content", ""))
               for k, v in responses.items() if "content" in v}
    agree_pairs: list[tuple[str, str]] = []
    names = list(lengths.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            la, lb = lengths[a], lengths[b]
            if la == 0 or lb == 0:
                continue
            ratio = min(la, lb) / max(la, lb)
            if ratio >= 0.5:
                agree_pairs.append((a, b))
    median_len = (sorted(lengths.values())[len(lengths) // 2]
                  if lengths else 0)

    return {
        "prompt": prompt,
        "responses": responses,
        "consensus": {
            "agree_pairs": agree_pairs,
            "median_length_chars": median_len,
            "n_succeeded": len(lengths),
            "n_attempted": len(responses),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write(
            "usage: python3 multi_backend_crosscheck.py <prompt> [--json]\n")
        sys.exit(1)
    prompt = sys.argv[1]
    as_json = "--json" in sys.argv[2:]
    result = triangulate(prompt)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Prompt: {prompt}\n")
        for name, r in result["responses"].items():
            print("=" * 72)
            print(f"{name} (wall={r.get('wall_s', '?')}s)")
            print("=" * 72)
            if "error" in r:
                print(f"ERROR: {r['error']}")
            else:
                print(r.get("content", "")[:2000])
            print()
        print("=" * 72)
        print(f"Consensus: {result['consensus']}")
