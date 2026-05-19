#!/usr/bin/env python3
"""Second pass: fix Tarbes->Oloron in \thanks{} pattern + normalize pdfauthor.

Targets papers using \author{Kevin\thanks{...Tarbes...}} pattern instead of multiline.
"""
import re
import pathlib

PAPERS_ROOT = "/root/cc-private/papers"


def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    changes = []

    # 1. Tarbes -> Oloron-Sainte-Marie globally
    if "Tarbes" in content:
        new = re.sub(r"Tarbes,\s*France", "Oloron-Sainte-Marie, France", content)
        if new != content:
            content = new
            changes.append("Tarbes → Oloron-Sainte-Marie")

    # 2. pdfauthor without accents -> with accents
    # pdfauthor={Kevin Remondiere}  ->  pdfauthor={Kévin Remondière}
    content_new = re.sub(
        r"pdfauthor\s*=\s*\{Kevin Remondiere\}",
        "pdfauthor={Kévin Remondière}",
        content,
    )
    if content_new != content:
        content = content_new
        changes.append("pdfauthor accents")

    # 3. pdfauthor={Kevin Remondière} (mixed) -> Kévin
    content_new = re.sub(
        r"pdfauthor\s*=\s*\{Kevin Remondière\}",
        "pdfauthor={Kévin Remondière}",
        content,
    )
    if content_new != content:
        content = content_new
        changes.append("pdfauthor Kevin→Kévin")

    # 4. Comment '%% Author: Kevin Remondière' -> 'Kévin'
    content_new = re.sub(
        r"%%\s*Author:\s*Kevin Remondière",
        "%% Author: Kévin Remondière",
        content,
    )
    if content_new != content:
        content = content_new
        changes.append("comment Author K→Kévin")

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True, changes
    return False, ["no changes"]


def main():
    root = pathlib.Path(PAPERS_ROOT)
    fixed = 0
    skipped = 0

    for tex in sorted(root.rglob("main.tex")):
        if "archive" in tex.parts:
            continue
        rel = tex.relative_to(root)
        changed, msgs = fix_file(tex)
        status = "✓" if changed else "—"
        if changed:
            print(f"{status} {str(rel):60s} {'; '.join(msgs)}")
            fixed += 1
        else:
            skipped += 1

    print()
    print(f"Fixed: {fixed} / Skipped: {skipped}")


if __name__ == "__main__":
    main()
