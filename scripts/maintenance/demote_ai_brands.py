#!/usr/bin/env python3
"""Demote AI brand mentions (Claude/DeepSeek/Anthropic/OpenClaw) to generic 'LLM tooling'.

Kevin's discipline: peu de mention specific brand, garder reconnaissance LLM générique pour AI use disclosure (AI_USE.md handles compliance).
"""
import re
import pathlib

PAPERS_ROOT = "/root/cc-private/papers"

REPLACEMENTS = [
    # (regex pattern, replacement) — case-insensitive on the LHS for some
    (r"multi-LLM tooling \(Claude Opus, DeepSeek\)",
     "multi-LLM tooling"),
    (r"multi-LLM tooling \(Anthropic Claude Opus and DeepSeek V4 Pro\)",
     "multi-LLM tooling"),
    (r"LLM systems \(Claude, DeepSeek, Gemini\) used as research assistants",
     "LLM systems used as research assistants"),
    (r"one DeepSeek auxiliary computation",
     "one auxiliary LLM-based computation"),
    (r"LLM dispatch threads \(DeepSeek V4 Pro,\s*Opus 4\.7, Sonnet 4\.6, Gemini, Mistral\)",
     "LLM dispatch threads"),
    (r"arXiv IDs proposed by DeepSeek V4 Pro",
     "arXiv IDs proposed by LLM tooling"),
    # Paper_G4_obstruction — methodology
    (r"DeepSeek--V4--Pro adversarial review wave G4\.0",
     "LLM-based adversarial review wave G4.0"),
    (r"nine independent DeepSeek--V4--Pro workers",
     "nine independent LLM-based workers"),
    (r"an independent Opus--4\.7 adversarial audit",
     "an independent LLM-based adversarial audit"),
    # Anywhere else
    (r"DeepSeek V4 Pro", "LLM tooling"),
    (r"DeepSeek--V4--Pro", "LLM-based reviewer"),
    (r"Claude Opus", "LLM"),
    (r"Claude--4\.7", "LLM"),
    (r"Opus 4\.7", "LLM"),
    (r"Opus--4\.7", "LLM"),
    (r"Sonnet 4\.6", "LLM"),
    (r"Sonnet--4\.6", "LLM"),
    (r"Anthropic Claude", "LLM"),
    (r"\bAnthropic\b", "LLM provider"),
    (r"\bOpenClaw\b", "research pipeline"),
    (r"\bclaude\.ai\b", "LLM API"),
    # In comments too (LaTeX comments %% are fine, just demote)
]


def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    applied = []
    for pat, repl in REPLACEMENTS:
        new = re.sub(pat, repl, content)
        if new != content:
            applied.append(pat[:50])
            content = new
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True, applied
    return False, []


def main():
    root = pathlib.Path(PAPERS_ROOT)
    fixed = 0
    for tex in sorted(root.rglob("*.tex")):
        if "archive" in tex.parts:
            continue
        changed, applied = fix_file(tex)
        if changed:
            rel = tex.relative_to(root)
            print(f"✓ {str(rel):60s} {len(applied)} replacements")
            fixed += 1

    # also .md cover letters
    for md in sorted(root.rglob("*.md")):
        if "archive" in md.parts:
            continue
        changed, applied = fix_file(md)
        if changed:
            rel = md.relative_to(root)
            print(f"✓ {str(rel):60s} {len(applied)} replacements (md)")
            fixed += 1

    print(f"\nFixed: {fixed} files")


if __name__ == "__main__":
    main()
