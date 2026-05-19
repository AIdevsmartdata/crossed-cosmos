#!/usr/bin/env python3
"""Extract metadata from each paper main.tex and build PAPERS.md structured."""
import re
import pathlib
import json

PAPERS_ROOT = pathlib.Path("/root/cc-private/papers")
OUTPUT = pathlib.Path("/root/cc-private/PAPERS.md")

# Classification rules (path-based)
CORPUS_A_YM = {  # Yang-Mills + lattice + glueball
    "Paper_PRL_Theoreme_A_LMP",
    "Paper_K_ASP_Mini_JNT",
    "Paper_ECI_Survey_Clay_BullAMS",
    "Paper_P4W3_MathAnn",
    "Paper_LeeYang_SU2",
    "Paper_NewtonDickson_Note",
    "Paper_NewtonDickson_short",
    "Phase_E_motivic_glueball",
    "Paper_6prime_excited_glueball_AdS",
    "Paper_Holographic_SchuttHecke_JHEP",
    "Paper_G4_obstruction",
    "Paper_G3_G5_CMP",
    "Paper_NoGo_PRL",
    "Paper_Sp2N_mini",
    "Paper_NINE_INVARIANT_LATTICE",
    "Paper_TEK_X024_Note",
    "Paper_P4_KleinSigma_v1",
}

CORPUS_B_ECI_NT = {  # Number Theory, motives, Hodge, modular
    "Paper_HSH_v3_letter_JNT_v2",
    "Paper_SchuttHodge_MULTI_D_JNT",
    "Paper_Hodge_Note_ExpMath",
    "Paper_M187_period_identity",
    "M142_hierarchy_M183_M184",
    "Paper_unified_M142_hierarchy",
    "Paper_P7_qD_Q_Rationality",
    "Paper_RH_Lemma_JNT",
    "Paper_3_M183_3lemmas",
    "Paper_B_h1_selection_KW",
    "Paper_ClK_orbit",
    "Paper_Hurwitz_7disc_JNT",
    "Paper_NW_Voisin_index_NOTE",
    "Paper_Beilinson_qD_Note",
    "Paper_Beilinson_qD_short",
    "Paper_P5_SMatrix_Beilinson",
    "Paper_P5_skeleton",
}


def extract_title(path):
    """Extract title from \title{...} in tex file - handles nested braces."""
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except:
        return "[Unable to read]"
    # Find \title{ position
    i = content.find("\\title")
    if i < 0:
        return "[No \\title found]"
    # Skip optional [...]
    j = i + len("\\title")
    while j < len(content) and content[j] in " \t\n":
        j += 1
    if j < len(content) and content[j] == "[":
        depth = 1
        j += 1
        while j < len(content) and depth > 0:
            if content[j] == "[": depth += 1
            elif content[j] == "]": depth -= 1
            j += 1
        while j < len(content) and content[j] in " \t\n":
            j += 1
    if j >= len(content) or content[j] != "{":
        return "[Malformed \\title]"
    # Now match balanced braces
    depth = 1
    j += 1
    start = j
    while j < len(content) and depth > 0:
        if content[j] == "{": depth += 1
        elif content[j] == "}": depth -= 1
        if depth > 0:
            j += 1
    title = content[start:j]
    # Clean
    title = re.sub(r"\\\\(\[[^\]]*\])?", " ", title)
    title = re.sub(r"\\thanks\{[^}]*\}", "", title)
    title = re.sub(r"\\\\", " ", title)
    title = re.sub(r"\\,", " ", title)
    title = re.sub(r"\\(?:large|Large|small|footnotesize|normalsize|bf|it|tt|emph|textbf|textit)", "", title)
    # \texorpdfstring{TeX}{Unicode} → keep Unicode (second arg)
    title = re.sub(r"\\texorpdfstring\{[^{}]*\}\{([^{}]*)\}", r"\1", title)
    title = re.sub(r"%[^\n]*", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace("\\(", "$").replace("\\)", "$")
    title = title.replace("--", "—")
    return title or "[Empty title]"


def extract_journal(folder_name):
    """Infer target journal from folder name."""
    mapping = {
        "PRL": "Phys. Rev. Lett.",
        "LMP": "Lett. Math. Phys.",
        "JNT": "J. Number Theory",
        "Math.Ann": "Math. Ann.",
        "MathAnn": "Math. Ann.",
        "JHEP": "JHEP",
        "ExpMath": "Exp. Math.",
        "BullAMS": "Bull. AMS",
        "CMP": "Commun. Math. Phys.",
        "PRD": "Phys. Rev. D",
        "JFA": "J. Funct. Anal.",
    }
    for key, journal in mapping.items():
        if key in folder_name:
            return journal
    return "TBD"


def count_pages(pdf_path):
    """Estimate page count from PDF."""
    if not pdf_path.exists():
        return "?"
    try:
        import subprocess
        r = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, timeout=5)
        for line in r.stdout.split("\n"):
            if line.startswith("Pages:"):
                return line.split(":")[1].strip()
    except:
        pass
    return "?"


def collect_paper(tex_path):
    folder = tex_path.parent.name
    if "morn39_compiled" in str(tex_path):
        folder = f"morn39/{tex_path.parent.name}"
    rel = tex_path.relative_to(PAPERS_ROOT)
    title = extract_title(tex_path)
    pdf_path = tex_path.parent / "main.pdf"
    pages = count_pages(pdf_path)
    journal = extract_journal(folder)
    return {
        "folder": folder,
        "path": str(rel),
        "title": title,
        "pages": pages,
        "journal": journal,
    }


def render_section(papers, anchor):
    if not papers:
        return ""
    lines = []
    lines.append(f"### Index — {len(papers)} papers")
    lines.append("")
    lines.append("| # | Title | Folder | Pages | Target |")
    lines.append("|---|---|---|---:|---|")
    for i, p in enumerate(papers, 1):
        title = p["title"][:80] + ("…" if len(p["title"]) > 80 else "")
        lines.append(f"| {i} | {title} | [`{p['folder']}`](papers/{p['folder']}/) | {p['pages']} | {p['journal']} |")
    lines.append("")
    return "\n".join(lines)


def main():
    papers = []
    for tex in sorted(PAPERS_ROOT.rglob("main.tex")):
        if "archive" in tex.parts:
            continue
        papers.append(collect_paper(tex))

    # Classify
    corpus_a = [p for p in papers if any(p["folder"].endswith(k) or p["folder"] == k for k in CORPUS_A_YM)]
    corpus_b = [p for p in papers if any(p["folder"].endswith(k) or p["folder"] == k for k in CORPUS_B_ECI_NT)]
    morn39_a = [p for p in papers if p["folder"].startswith("morn39/") and "KleinSigma" in p["folder"]]
    morn39_b = [p for p in papers if p["folder"].startswith("morn39/") and "KleinSigma" not in p["folder"]]
    unclassified = [p for p in papers if p not in corpus_a and p not in corpus_b and p not in morn39_a and p not in morn39_b]

    out = []
    out.append("# Papers — crossed-cosmos / ECI research corpus")
    out.append("")
    out.append("**Author**: Kévin Rémondière — Independent Researcher, Oloron-Sainte-Marie, France")
    out.append("**ORCID**: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)")
    out.append("**Email**: kevin.remondiere@gmail.com")
    out.append("**License**: CC-BY-4.0")
    out.append("**Concept DOI**: [10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398)")
    out.append("")
    out.append(f"Total active papers: **{len(papers)}** organized in three corpora.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Corpus A — Yang-Mills Mass Gap & Lattice Bridge")
    out.append("")
    out.append("Empirical and conditional results on the SU(N) Yang-Mills mass gap, with the K_ASP arithmetic dictionary linking class-number-N imaginary quadratic fields to large-N glueball spectra.")
    out.append("")
    out.append("**Wiles strategy** (decomposition):")
    out.append("1. **Théorème A** (unconditional, on the arithmetic surrogate):  $m_{\\rm arith}(N) \\geq \\sqrt{2\\pi e\\,\\cdot\\,2/3}\\,\\cdot\\,F(N)\\,\\sqrt{21/25}$, modulo Sarnak 1983 + Vassilevich heat kernel + Cox-Gauss factorisation (3/3 EXACT at 50-digit).")
    out.append("2. **Transport conjecture** ($m_{\\rm YM} \\leftrightarrow m_{\\rm arith}$): four candidate routes (foncteur F, BSD Brunault-Chida, holographic, Smith asymptotic).")
    out.append("")
    out.append(render_section(corpus_a, "ym"))
    out.append("If `morn39/KleinSigma_LMP` exists, it belongs here.")
    out.append("")
    out.append(render_section(morn39_a, "ym2"))
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Corpus B — ECI Number Theory & Modular Forms")
    out.append("")
    out.append("CM newforms over imaginary quadratic fields, rational L-values (M142 hierarchy), HSH 2-rank, Beilinson regulators, Schütt-Hodge multi-weight.")
    out.append("")
    out.append(render_section(corpus_b, "nt"))
    out.append("")
    out.append("**morn39_compiled/** subprojects (auxiliary derivations):")
    out.append("")
    out.append(render_section(morn39_b, "nt2"))
    out.append("")
    if unclassified:
        out.append("---")
        out.append("")
        out.append("## Unclassified")
        out.append("")
        out.append(render_section(unclassified, "x"))
        out.append("")
    out.append("---")
    out.append("")
    out.append("## Corpus C — Cosmology (legacy track v5/v6/v7/Chimère)")
    out.append("")
    out.append("Preserved from earlier work, separate Zenodo records:")
    out.append("- **v5** — ECI phenomenological framework (`astro-ph.CO`) · [10.5281/zenodo.19696017](https://doi.org/10.5281/zenodo.19696017)")
    out.append("- **v6** — GSL on type-II crossed products (`hep-th`) · [10.5281/zenodo.19699006](https://doi.org/10.5281/zenodo.19699006)")
    out.append("- **v7-note** — Bogomolny–Keating + log-saturation no-go (`math.SP`)")
    out.append("- **Chimère Ω** — local-first LLM blueprint (`cs.LG`)")
    out.append("")
    out.append("See [`paper/`](paper/), [`paper/v6/`](paper/v6/), [`paper/v7_note/`](paper/v7_note/), [`paper/chimere_omega/`](paper/chimere_omega/) for full content and the historical PAPERS_v6.md (preserved as `PAPERS.md.v6-cosmology-2026-04`).")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## How to cite")
    out.append("")
    out.append("```bibtex")
    out.append("@misc{Remondiere2026CrossedCosmos,")
    out.append("  author       = {R\\'emondi\\`ere, K\\'evin},")
    out.append("  title        = {crossed-cosmos: ECI research corpus},")
    out.append("  year         = {2026},")
    out.append("  doi          = {10.5281/zenodo.19686398},")
    out.append("  url          = {https://github.com/AIdevsmartdata/crossed-cosmos}")
    out.append("}")
    out.append("```")
    out.append("")
    out.append("Per-paper BibTeX entries: see each folder's `cover_letter.tex` or accompanying metadata.")
    out.append("")
    out.append("## Build")
    out.append("")
    out.append("```bash")
    out.append("cd papers/<paper_folder> && latexmk -pdf main.tex")
    out.append("```")
    out.append("")
    out.append("## Contact")
    out.append("")
    out.append("**Kévin Rémondière** — Independent Researcher  ")
    out.append("Email: kevin.remondiere@gmail.com  ")
    out.append("ORCID: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)  ")
    out.append("GitHub: [AIdevsmartdata](https://github.com/AIdevsmartdata)")
    out.append("")

    OUTPUT.write_text("\n".join(out), encoding="utf-8")
    print(f"PAPERS.md written: {len(out)} lines")
    print(f"  Corpus A (YM): {len(corpus_a)}")
    print(f"  Corpus B (NT): {len(corpus_b)}")
    print(f"  morn39 (NT supplements): {len(morn39_b)}")
    print(f"  Unclassified: {len(unclassified)}")


if __name__ == "__main__":
    main()
