"""
gemini_crosscheck.py — cross-check via Gemini CLI (OAuth free tier).

Matches the interface of derivations/mistral_crosscheck.py and
derivations/qwen_crosscheck.py so the three can be used interchangeably
for triangulation audits.

Uses the `gemini` CLI (Google's official, npm-installed at
/home/remondiere/.npm-global/bin/gemini v0.38.2) in non-interactive
headless mode (`-p "..."`). Defaults to `gemini-2.5-pro` (or whatever
the CLI default is if omitted). No API key needed — OAuth session is
managed by the CLI itself.

Env vars (all optional):
  GEMINI_MODEL        override the model. Default: CLI default.
  GEMINI_TIMEOUT      wall-clock seconds. Default 180.
  GEMINI_YOLO         if '1', pass -y (auto-approve tool use). Default 0.

Usage:
    from gemini_crosscheck import crosscheck
    r = crosscheck("Your prompt")
    print(r['backend'], r['content'])

    # Shell:
    python3 derivations/gemini_crosscheck.py "Prompt here"
"""
from __future__ import annotations
import os
import subprocess
import sys
import time
from typing import Optional

GEMINI_BIN = "/home/remondiere/.npm-global/bin/gemini"


def crosscheck(prompt: str, *, timeout: int = 180,
               model: Optional[str] = None,
               yolo: bool = False) -> dict:
    """Return {backend, model, content, wall_s}. Raises RuntimeError on
    failure."""
    model = model or os.environ.get("GEMINI_MODEL")
    timeout = int(os.environ.get("GEMINI_TIMEOUT", str(timeout)))
    yolo = yolo or (os.environ.get("GEMINI_YOLO", "0") == "1")

    cmd = [GEMINI_BIN, "-p", prompt]
    if model:
        cmd += ["-m", model]
    if yolo:
        cmd += ["-y"]
    # Gemini CLI may print ANSI colours / banners; keep them out.
    env = {**os.environ, "NO_COLOR": "1", "GEMINI_NO_COLOR": "1"}

    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"gemini_crosscheck: timeout after {timeout}s") from e
    if r.returncode != 0:
        raise RuntimeError(
            f"gemini_crosscheck: exit {r.returncode}, stderr={r.stderr[:400]}")

    content = r.stdout.strip()
    return {
        "backend": "gemini-cli",
        "model": model or "(cli-default)",
        "content": content,
        "wall_s": round(time.time() - t0, 2),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("usage: python3 gemini_crosscheck.py <prompt>\n")
        sys.exit(1)
    try:
        r = crosscheck(sys.argv[1])
        sys.stderr.write(
            f"[gemini-cli model={r['model']} wall={r['wall_s']}s]\n")
        print(r["content"])
    except RuntimeError as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)
