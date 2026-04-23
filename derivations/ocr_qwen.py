"""
ocr_qwen.py — OCR / vision-QA CLI via qwen-tq3 on localhost:8083.

Complements ~/.openclaw/bin/ocr_glm.py (GLM-OCR via model-swap). This one
uses the always-on Qwen3.6-35B-A3B TQ3_4S + mmproj-BF16 endpoint (no
model swap, ~100 tok/s on RTX 5060 Ti) and accepts a PDF or an image.

Usage:
    # Single page of a PDF:
    python3 ocr_qwen.py paper.pdf --pages 1

    # Range of pages, JSON output:
    python3 ocr_qwen.py paper.pdf --pages 1-3 --json --out report.json

    # Direct image:
    python3 ocr_qwen.py figure.png

    # Custom prompt (replaces the default extraction template):
    python3 ocr_qwen.py paper.pdf --pages 1 \
        --prompt "Transcris tout le texte de cette page verbatim."

    # Higher DPI for tiny text (default 150):
    python3 ocr_qwen.py scan.pdf --pages 1 --dpi 220

Requires: pdftoppm (poppler-utils), requests, a running qwen-tq3.service
with --mmproj wired. Set QWEN_VISION_URL to override the endpoint
(default http://127.0.0.1:8083).

All calls use `enable_thinking=false` — vision prompts with long thinking
burn the budget and rarely improve accuracy on extraction tasks.
"""
from __future__ import annotations
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

DEFAULT_URL = os.environ.get("QWEN_VISION_URL", "http://127.0.0.1:8083")
DEFAULT_PROMPT = (
    "Extrait le contenu de cette page scientifique précisément :\n"
    "(a) titre ou section, (b) auteur/affiliation si visible, "
    "(c) texte principal (prose + équations significatives), "
    "(d) tables ou figures avec leur légende.\n"
    "N'invente rien. Écris 'illisible' pour ce que tu ne vois pas."
)


def _parse_pages(spec: str) -> list[int]:
    """Parse '1' / '1-3' / '1,3,5-7' into a sorted list of page indices."""
    out: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(chunk))
    return sorted(out)


def _pdf_to_pngs(pdf_path: Path, pages: list[int], dpi: int,
                 tmp_dir: Path) -> list[Path]:
    """Render each requested page to a PNG in tmp_dir. Returns PNG paths in
    the same order as `pages`."""
    out: list[Path] = []
    for p in pages:
        prefix = tmp_dir / f"page_{p:04d}"
        subprocess.run(
            ["pdftoppm", "-r", str(dpi), "-f", str(p), "-l", str(p),
             "-png", "-singlefile", str(pdf_path), str(prefix)],
            check=True,
        )
        png = tmp_dir / f"page_{p:04d}.png"
        if not png.exists():
            raise RuntimeError(f"pdftoppm did not produce {png}")
        out.append(png)
    return out


def _query_vision(png_path: Path, prompt: str, url: str, max_tokens: int,
                  temperature: float, timeout: int) -> dict:
    """Send a single-page vision request. Returns a dict with content,
    usage, timings, wall_s."""
    import requests
    b64 = base64.b64encode(png_path.read_bytes()).decode()
    payload = {
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url",
                 "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": prompt},
            ],
        }],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    t0 = time.time()
    r = requests.post(f"{url.rstrip('/')}/v1/chat/completions",
                      json=payload, timeout=timeout)
    r.raise_for_status()
    d = r.json()
    c = d["choices"][0]["message"]["content"]
    if isinstance(c, list):
        c = "".join(p.get("text", "") for p in c if p.get("type") == "text")
    return {
        "content": c,
        "usage": d.get("usage", {}),
        "timings": d.get("timings", {}),
        "wall_s": round(time.time() - t0, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="OCR/vision-QA via qwen-tq3:8083 (+mmproj).")
    ap.add_argument("source", type=Path,
                    help="Path to PDF or image (.png, .jpg, .jpeg).")
    ap.add_argument("--pages", default="1",
                    help="Pages for PDF: '1', '1-3', '1,3,5-7'. Default: 1.")
    ap.add_argument("--dpi", type=int, default=150,
                    help="PDF render DPI. Default 150. Bump to 220+ for tiny text.")
    ap.add_argument("--prompt", default=None,
                    help="Custom vision prompt. If omitted, uses the default extraction template.")
    ap.add_argument("--url", default=DEFAULT_URL,
                    help=f"Qwen vision endpoint. Default {DEFAULT_URL}.")
    ap.add_argument("--max-tokens", type=int, default=1500)
    ap.add_argument("--temperature", type=float, default=0.3)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--json", action="store_true",
                    help="Output structured JSON instead of human-readable text.")
    ap.add_argument("--out", type=Path, default=None,
                    help="Write output to file instead of stdout.")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"ERROR: {args.source} does not exist.", file=sys.stderr)
        return 2

    prompt = args.prompt or DEFAULT_PROMPT
    results: list[dict] = []

    # Determine input type
    ext = args.source.suffix.lower()
    with tempfile.TemporaryDirectory(prefix="ocr_qwen_") as tmp:
        tmp_dir = Path(tmp)
        if ext == ".pdf":
            pages = _parse_pages(args.pages)
            pngs = _pdf_to_pngs(args.source, pages, args.dpi, tmp_dir)
            for p, png in zip(pages, pngs):
                print(f"[ocr_qwen] page {p}: querying...", file=sys.stderr)
                res = _query_vision(png, prompt, args.url,
                                    args.max_tokens, args.temperature,
                                    args.timeout)
                res["page"] = p
                results.append(res)
        elif ext in (".png", ".jpg", ".jpeg"):
            print(f"[ocr_qwen] image: querying...", file=sys.stderr)
            res = _query_vision(args.source, prompt, args.url,
                                args.max_tokens, args.temperature,
                                args.timeout)
            res["page"] = 1
            results.append(res)
        else:
            print(f"ERROR: unsupported extension {ext}", file=sys.stderr)
            return 2

    # Output
    if args.json:
        out_text = json.dumps(
            {"source": str(args.source), "pages": results},
            ensure_ascii=False, indent=2)
    else:
        lines = []
        for r in results:
            tps = r.get("timings", {}).get("predicted_per_second", 0)
            u = r.get("usage", {})
            lines.append(f"\n===== page {r['page']} "
                         f"(wall={r['wall_s']}s prompt={u.get('prompt_tokens')} "
                         f"gen={u.get('completion_tokens')} tps={tps:.0f}) =====")
            lines.append(r["content"])
        out_text = "\n".join(lines).lstrip()

    if args.out:
        args.out.write_text(out_text)
        print(f"[ocr_qwen] wrote {args.out}", file=sys.stderr)
    else:
        print(out_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
