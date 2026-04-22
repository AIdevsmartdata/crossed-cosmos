"""
qwen_crosscheck.py — cross-check via Qwen, matching mistral_crosscheck.py interface.

Priority order (stops at first available):
  1. Local chimere-server (http://127.0.0.1:8081/v1/chat/completions) — zero cost
  2. DashScope Singapore international endpoint — requires DASHSCOPE_API_KEY
  3. DashScope US Virginia endpoint — alternate region
  4. HuggingFace Inference API — requires HF_TOKEN, rate-limited

Env vars (all optional):
  DASHSCOPE_API_KEY   — Alibaba Cloud / Model Studio key, created at
                        https://dashscope.aliyuncs.com/apiKey
  DASHSCOPE_MODEL     — model name, default 'qwen3-max' via DashScope
  CHIMERE_LOCAL_URL   — override local endpoint, default http://127.0.0.1:8081
  CHIMERE_LOCAL_MODEL — override local model tag, default 'qwen3.5-ramp'
  HF_TOKEN            — HuggingFace token as fallback
  HF_MODEL            — HF repo, default 'Qwen/Qwen2.5-72B-Instruct'

Usage:
    from qwen_crosscheck import crosscheck
    result = crosscheck(prompt, timeout=300, max_tokens=3000, temperature=0.6)
    print(result['backend'])   # which endpoint was used
    print(result['content'])   # response text

Or from shell:
    python3 derivations/qwen_crosscheck.py "Your prompt here"

No key loaded at import time — keys are read lazily when needed so the file
is safe to import without a .env.
"""
from __future__ import annotations
import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Optional

# Tolerant .env parser — supports ENV_FILE override, default ~/.env
def _load_env_file() -> dict:
    env_file = Path(os.environ.get("ENV_FILE", Path.home() / ".env"))
    out: dict = {}
    if not env_file.exists():
        return out
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _getenv(key: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(key)
    if v is not None:
        return v
    return _load_env_file().get(key, default)


def _try_local_chimere(prompt: str, timeout: int, max_tokens: int,
                       temperature: float) -> Optional[dict]:
    url = _getenv("CHIMERE_LOCAL_URL", "http://127.0.0.1:8081")
    model = _getenv("CHIMERE_LOCAL_MODEL", "qwen3.5-ramp")
    endpoint = f"{url.rstrip('/')}/v1/chat/completions"
    try:
        r = requests.post(
            endpoint,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=timeout,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        if isinstance(content, list):
            # some deploys return a list of parts
            parts = [p.get("text", "") for p in content if p.get("type") == "text"]
            content = "".join(parts)
        return {
            "backend": "chimere-local",
            "endpoint": endpoint,
            "model": model,
            "content": content,
            "usage": data.get("usage", {}),
        }
    except (requests.ConnectionError, requests.Timeout):
        return None
    except Exception as e:
        sys.stderr.write(f"[qwen_crosscheck] chimere-local error: {e}\n")
        return None


def _try_dashscope(prompt: str, timeout: int, max_tokens: int,
                   temperature: float, region: str = "intl") -> Optional[dict]:
    key = _getenv("DASHSCOPE_API_KEY")
    if not key:
        return None
    model = _getenv("DASHSCOPE_MODEL", "qwen3-max")
    hosts = {
        "intl": "https://dashscope-intl.aliyuncs.com",
        "us":   "https://dashscope-us.aliyuncs.com",
        "cn":   "https://dashscope.aliyuncs.com",
    }
    base = hosts.get(region, hosts["intl"])
    endpoint = f"{base}/compatible-mode/v1/chat/completions"
    try:
        r = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=timeout,
        )
        if r.status_code != 200:
            sys.stderr.write(f"[qwen_crosscheck] dashscope {region} "
                             f"HTTP {r.status_code}: {r.text[:200]}\n")
            return None
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        return {
            "backend": f"dashscope-{region}",
            "endpoint": endpoint,
            "model": model,
            "content": content,
            "usage": data.get("usage", {}),
        }
    except Exception as e:
        sys.stderr.write(f"[qwen_crosscheck] dashscope {region} error: {e}\n")
        return None


def _try_hf(prompt: str, timeout: int, max_tokens: int,
            temperature: float) -> Optional[dict]:
    token = _getenv("HF_TOKEN")
    if not token:
        return None
    model = _getenv("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")
    endpoint = f"https://api-inference.huggingface.co/models/{model}"
    try:
        r = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "return_full_text": False,
                },
            },
            timeout=timeout,
        )
        if r.status_code != 200:
            sys.stderr.write(f"[qwen_crosscheck] hf HTTP {r.status_code}: "
                             f"{r.text[:200]}\n")
            return None
        data = r.json()
        content = data[0].get("generated_text", "") if isinstance(data, list) else ""
        return {
            "backend": "huggingface",
            "endpoint": endpoint,
            "model": model,
            "content": content,
            "usage": {},
        }
    except Exception as e:
        sys.stderr.write(f"[qwen_crosscheck] hf error: {e}\n")
        return None


def crosscheck(prompt: str, *, timeout: int = 300, max_tokens: int = 3000,
               temperature: float = 0.6,
               backends: Optional[list[str]] = None) -> dict:
    """Return {backend, endpoint, model, content, usage} from first working
    backend. Raises RuntimeError if all fail.

    backends: list subset of {'local', 'dashscope-intl', 'dashscope-us',
              'dashscope-cn', 'hf'}. Default:
              ['local', 'dashscope-intl', 'dashscope-us', 'hf'].
    """
    if backends is None:
        backends = ["local", "dashscope-intl", "dashscope-us", "hf"]
    errors: list[str] = []
    for b in backends:
        t0 = time.time()
        if b == "local":
            result = _try_local_chimere(prompt, timeout, max_tokens, temperature)
        elif b == "dashscope-intl":
            result = _try_dashscope(prompt, timeout, max_tokens, temperature, "intl")
        elif b == "dashscope-us":
            result = _try_dashscope(prompt, timeout, max_tokens, temperature, "us")
        elif b == "dashscope-cn":
            result = _try_dashscope(prompt, timeout, max_tokens, temperature, "cn")
        elif b == "hf":
            result = _try_hf(prompt, timeout, max_tokens, temperature)
        else:
            errors.append(f"unknown backend {b}")
            continue
        if result is not None:
            result["wall_s"] = round(time.time() - t0, 2)
            return result
        errors.append(f"{b}: unavailable")
    raise RuntimeError("qwen_crosscheck: no backend worked. " +
                       "; ".join(errors))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("usage: python3 qwen_crosscheck.py <prompt>\n")
        sys.exit(1)
    prompt = sys.argv[1]
    try:
        result = crosscheck(prompt)
        print(json.dumps({k: v for k, v in result.items() if k != "content"},
                         indent=2))
        print("--- content ---")
        print(result["content"])
    except RuntimeError as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)
