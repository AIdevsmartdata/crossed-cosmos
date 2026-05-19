#!/usr/bin/env python3
"""Normalize author blocks across all papers/ to use canonical Kévin Rémondière + ORCID + Oloron-Sainte-Marie.

Patterns detected (variants):
  - \author{Kevin Remondi\`ere} (no accent é)
  - \author{K. Remondi\`ere} (abbreviated)
  - \author{K.~Remondi\`ere} (abbreviated tilde)
  - \author{K\'evin R\'emondi\`ere} (correct base)
  - \author{Kevin R\'emondi\`ere} (no accent K)
  - + various with/without affiliation, \email, \texttt

Canonical format chosen per paper-style:
  - Multi-line author block (most common):
    \author{K\'evin R\'emondi\`ere\\
    \small Independent Researcher, Oloron-Sainte-Marie, France\\
    \small ORCID: \href{https://orcid.org/0009-0008-2443-7166}{0009-0008-2443-7166}\\
    \small \texttt{kevin.remondiere@gmail.com}}
"""
import os
import re
import sys
import pathlib

CANONICAL_NAME = r"K\'evin R\'emondi\`ere"
CANONICAL_AFFIL = r"Independent Researcher, Oloron-Sainte-Marie, France"
CANONICAL_ORCID_URL = "https://orcid.org/0009-0008-2443-7166"
CANONICAL_ORCID_ID = "0009-0008-2443-7166"
CANONICAL_EMAIL = "kevin.remondiere@gmail.com"

PAPERS_ROOT = "/root/cc-private/papers"

# Variants of the bare name to normalize
NAME_PATTERNS = [
    r"Kevin Remondi\\`ere",       # no accent (literal backtick escaped for \`)
    r"K\. Remondi\\`ere",          # abbreviated period
    r"K\.~Remondi\\`ere",          # abbreviated tilde
    r"K\.~R\\'emondi\\`ere",       # abbrev with one accent
    r"Kevin R\\'emondi\\`ere",     # no accent K
    r"K\. R\\'emondi\\`ere",       # abbrev one accent
]


def detect_author_block(content):
    """Find \author{...} including potential affiliation."""
    # Match \author{ ... } even with nested \\ and newlines
    # Greedy on innermost balanced braces
    m = re.search(r"\\author\{((?:[^{}]|\{[^{}]*\})*)\}", content, re.DOTALL)
    if not m:
        return None, None, None
    return m.start(), m.end(), m.group(1)


def get_canonical_author_block(style="multiline"):
    if style == "multiline":
        return (
            f"\\author{{{CANONICAL_NAME}\\\\\n"
            f"\\small Independent Researcher, Oloron-Sainte-Marie, France\\\\\n"
            f"\\small ORCID: \\href{{{CANONICAL_ORCID_URL}}}{{{CANONICAL_ORCID_ID}}}\\\\\n"
            f"\\small \\texttt{{{CANONICAL_EMAIL}}}}}"
        )
    elif style == "compact":
        return (
            f"\\author{{{CANONICAL_NAME}\\\\\\small {CANONICAL_AFFIL}"
            f"\\\\\\small ORCID: \\href{{{CANONICAL_ORCID_URL}}}{{{CANONICAL_ORCID_ID}}}"
            f"\\\\\\small \\texttt{{{CANONICAL_EMAIL}}}}}"
        )
    return None


def fix_affiliation_tarbes(content):
    """Fix the Tarbes typo to Oloron-Sainte-Marie."""
    return re.sub(
        r"Tarbes,\s*France",
        "Oloron-Sainte-Marie, France",
        content,
    )


def normalize_file(path):
    """Normalize a single paper's main.tex author block."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # 1. Fix Tarbes typo wherever it appears
    if "Tarbes" in content:
        content = fix_affiliation_tarbes(content)
        changes.append("Tarbes → Oloron-Sainte-Marie")

    # 2. Locate author block
    start, end, block = detect_author_block(content)
    if start is None:
        return False, ["No \\author{} block found"]

    # 3. Check if already canonical (has ORCID + Kévin accents + Oloron)
    has_kevin_accents = "K\\'evin" in block or "K\\'evin R" in block
    has_orcid = CANONICAL_ORCID_ID in block or "orcid.org" in content
    has_oloron = "Oloron" in block or "Oloron" in content
    has_independent = "Independent" in content

    if has_kevin_accents and has_orcid and has_oloron and has_independent:
        # Already normalized
        if original != content:
            # only Tarbes fix
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, changes
        return False, ["already canonical"]

    # 4. Replace author block with canonical multiline
    new_block = get_canonical_author_block(style="multiline")

    # Also remove any standalone \email{...} on next lines that conflicts
    # And \affiliation{...} that conflicts
    new_content = content[:start] + new_block + content[end:]

    # Remove standalone \email{kevin.remondiere@gmail.com} that immediately follows
    new_content = re.sub(
        r"(}\s*\n)\\email\{" + re.escape(CANONICAL_EMAIL) + r"\}\s*\n",
        r"\1",
        new_content,
    )

    # Remove standalone \affiliation{...} block if it duplicates affiliation
    new_content = re.sub(
        r"(}\s*\n)\\affiliation\{[^}]*\}\s*\n",
        r"\1",
        new_content,
    )

    if new_content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        changes.append("author block normalized → Kévin + ORCID + Oloron")
        return True, changes

    return False, ["no changes"]


def main():
    root = pathlib.Path(PAPERS_ROOT)
    fixed = 0
    skipped = 0
    errors = 0

    for tex in sorted(root.rglob("main.tex")):
        if "archive" in tex.parts:
            continue
        rel = tex.relative_to(root)
        try:
            changed, msgs = normalize_file(tex)
            status = "✓ FIXED" if changed else "—"
            print(f"{status:12s}{str(rel):60s} {'; '.join(msgs)}")
            if changed:
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"✗ ERROR     {str(rel):60s} {e}")
            errors += 1

    print()
    print(f"Fixed   : {fixed}")
    print(f"Skipped : {skipped}")
    print(f"Errors  : {errors}")
    print(f"Total   : {fixed + skipped + errors}")


if __name__ == "__main__":
    main()
