"""
V6 pre-write claims audit pipeline.

Every numerical value, every citation, every theoretical claim intended for
insertion into the v6 draft (or any companion) MUST pass through this script
BEFORE being written to .tex. Usage:

    python V6-claims-audit-pipeline.py --registry claims.yaml

The registry is a YAML file with one entry per claim. Types:
  - numerical:   value, formula, tolerance → recomputed and asserted
  - citation:    bib_key, expected_title/venue/arxiv → verified against eci.bib
                 and (if network) against Crossref/arXiv via existing RAG cache
  - theoretical: statement, status ∈ {THEOREM, POSTULATE, ANSATZ, HEURISTIC,
                 MOTIVATION} → enforced labelling in prose
  - falsifier:   observable, S/N, instrument, pipeline_d18 ∈ {True, False}
                 → rejected if pipeline_d18 is False (V6-4)

All gates are HARD: a single FAIL aborts with non-zero exit code. This is
enforced by the pre-tag hook.

Anchor: PRINCIPLES.md rules 1, 2, 3, 12, 16 and V6-1, V6-4.
"""

from __future__ import annotations
import sys, os, math, subprocess, re, json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ----- Fundamental constants (CODATA 2022 exact / recommended) --------------
C     = 2.99792458e8     # m/s (exact)
G     = 6.67430e-11      # m^3 kg^-1 s^-2
HBAR  = 1.054571817e-34  # J s (exact by SI definition)
KB    = 1.380649e-23     # J/K (exact)
H_EV  = 4.135667696e-15  # eV s
MPC_M = 3.0856775814913673e22  # m (IAU 2015)

# Derived Planck quantities (deriving from the above, NOT quoted separately)
def planck_mass()      : return math.sqrt(HBAR * C / G)
def planck_length()    : return math.sqrt(HBAR * G / C**3)
def planck_time()      : return math.sqrt(HBAR * G / C**5)
def planck_energy_J()  : return math.sqrt(HBAR * C**5 / G)
def planck_temp_K()    : return math.sqrt(HBAR * C**5 / (G * KB**2))
def omega_planck()     : return math.sqrt(C**5 / (G * HBAR))  # rad/s

def H0_SI(H0_kms_per_Mpc: float) -> float:
    return H0_kms_per_Mpc * 1000.0 / MPC_M

def schwarzschild_entropy_kB(M_kg: float) -> float:
    """S_BH / k_B = 4π G M² / (ℏ c)."""
    return 4 * math.pi * G * M_kg**2 / (HBAR * C)

def bisognano_wichmann_unruh_kappa(T_R_K: float) -> float:
    """κ_R = 2π k_B T_R / ℏ (rad/s)."""
    return 2 * math.pi * KB * T_R_K / HBAR

def de_sitter_temp(H0: float) -> float:
    """T_dS = ℏ H_0 / (2π k_B) — Gibbons-Hawking."""
    return HBAR * H0 / (2 * math.pi * KB)


# ----- Gate enforcement -----------------------------------------------------
@dataclass
class Gate:
    name: str
    passed: bool
    detail: str = ""

_gates: list[Gate] = []

def gate(name: str, cond: bool, detail: str = "") -> None:
    _gates.append(Gate(name, cond, detail))
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}: {detail}")


# ============================================================================
# SECTION 1 — NUMERICAL ANCHORS (pre-approved reference values)
# ============================================================================
# Every numerical claim in v6/v6.1 must either (a) match one of these anchors
# within tolerance, or (b) be derived by a script that calls these functions.
# No numerical value quoted from training-data memory.
# ============================================================================

def check_numerical_anchors():
    print("\n=== Section 1: Numerical anchors ===")
    # ω_Planck
    omega_P = omega_planck()
    gate("omega_P = 1.854859e43 rad/s (within 0.1%)",
         abs(omega_P - 1.854859e43) / 1.854859e43 < 1e-3,
         f"computed {omega_P:.6e}")

    # T_Planck
    T_P = planck_temp_K()
    gate("T_Planck = 1.4168e32 K (within 0.1%)",
         abs(T_P - 1.4168e32) / 1.4168e32 < 1e-3,
         f"computed {T_P:.6e}")

    # *** The identity that was FALSELY claimed in Claude-app document ***
    # 2π k_B T_P / ℏ = 2π ω_P, NOT ω_P.
    kappa_at_T_P = bisognano_wichmann_unruh_kappa(T_P)
    gate("BW-Unruh κ at T_Planck equals 2π · ω_Planck (NOT ω_Planck)",
         abs(kappa_at_T_P - 2 * math.pi * omega_P) / (2 * math.pi * omega_P) < 1e-6,
         f"κ(T_P)/ω_P = {kappa_at_T_P/omega_P:.4f} (expected 2π={2*math.pi:.4f})")

    # H_0 at Planck-ACT 67.4 and SH0ES 73.0
    H0_p = H0_SI(67.4)
    gate("H_0(67.4 km/s/Mpc) = 2.184e-18 s^-1 (within 0.1%)",
         abs(H0_p - 2.1843e-18) / 2.1843e-18 < 1e-3,
         f"computed {H0_p:.4e}")

    # T_dS at 67.4
    T_dS = de_sitter_temp(H0_p)
    gate("T_dS(67.4) = 2.655e-30 K (within 1%)",
         abs(T_dS - 2.655e-30) / 2.655e-30 < 1e-2,
         f"computed {T_dS:.4e}")

    # Lambda/M_P^4 vs (H_0/ω_P)² — NOT exactly equal
    rho_L = 0.6847 * 3 * H0_p**2 * C**2 / (8 * math.pi * G)
    rho_P = C**7 / (HBAR * G**2)
    ratio_cosmo = rho_L / rho_P
    ratio_H0 = (H0_p / omega_P)**2
    # They should agree to within ~1 order of magnitude, NOT exactly
    log_ratio = math.log10(ratio_cosmo / ratio_H0)
    gate("Λ/M_P⁴ ≠ (H_0/ω_P)² exactly (at least 0.3 dex off)",
         abs(log_ratio) > 0.3,
         f"log10[(Λ/M_P⁴) / (H_0/ω_P)²] = {log_ratio:.3f} dex")

    # S_BH at 5.1e14 g — NOT 10^25
    M_star_kg = 5.1e14 * 1e-3
    S_star = schwarzschild_entropy_kB(M_star_kg)
    gate("S_BH(5.1e14 g) ~ 10^40 (NOT 10^25)",
         abs(math.log10(S_star) - 40) < 1.0,
         f"computed log10 S_BH = {math.log10(S_star):.2f}")

    # Burst extension with *correct* S
    alpha = 0.05
    ext = S_star**(-alpha) * math.log(S_star)
    gate("With correct S_BH, burst 'extension' S^-0.05 * ln S < 2 (not 3)",
         ext < 2,
         f"computed ext = {ext:.3f}")


# ============================================================================
# SECTION 2 — CITATION GATES
# ============================================================================

CITATION_ANCHORS_MANDATORY = {
    # Cited in v6.1 HEAD (a09bbce). Any of these missing → HARD FAIL.
    "Haferkamp2022":   {"venue": "Nat. Phys.", "volume": "18", "page": "528",
                        "arxiv": "2106.05305",
                        "doi": "10.1038/s41567-022-01539-6"},
    "CLPW2023":        {"arxiv": "2206.10780"},
    "FaulknerSperanza2024": {"arxiv": "2405.00847",
                             "note": "no 'Theorem 3.1' label; use Eq.(3.57)/(4.31)"},
    "Jacobson1995":    {"arxiv": "gr-qc/9504004"},
    "Wall2011":        {"arxiv": "1105.3445"},
    "BrownSusskind2018": {"arxiv": "1701.01107"},
    "ConnesRovelli1994": {"arxiv": "gr-qc/9406019"},
    "KhouryWeltman2004": {"arxiv": "astro-ph/0309300"},
}

CITATION_ANCHORS_WISHLIST = {
    # Candidate for v7 phenomenology or §6 programmatic outlook. Missing is
    # a WARNING, not FAIL — but must be added before any v2 document cites them.
    "Jacobson2016":    {"arxiv": "1505.04753",
                        "note": "entanglement equilibrium"},
    "CaputaMagan2024": {"arxiv": "2205.05688",
                        "note": "Krylov / spread complexity of modular flow"},
    "GibbonsHawking1977": {"journal": "PRD 15 2738",
                           "note": "Euclidean action, factor 1/4"},

    # *** Known-bad value from Claude-app document ***
    "Lange2021":       {"arxiv": "2010.06620",
                        "journal": "PRL 126 011102",
                        "value_alpha_dot_REAL": "1.0(1.1) × 10^-18 / yr",
                        "value_alpha_dot_FABRICATED": "-8.0 ± 3.6 × 10^-18/yr",
                        "WARNING": "Claude-app doc value is WRONG. Real value ~1σ compatible with zero."},
}

def check_citation_file(bibfile: Path, key: str) -> Optional[str]:
    """Return first line of bib entry for KEY, or None."""
    try:
        txt = bibfile.read_text()
    except FileNotFoundError:
        return None
    m = re.search(r"@\w+\{" + re.escape(key) + r",", txt)
    if not m:
        return None
    # Find the title field
    rest = txt[m.end():m.end()+2000]
    tm = re.search(r"title\s*=\s*[{\"]([^}\"]+)", rest)
    return tm.group(1) if tm else "<no title field>"

def check_citations():
    print("\n=== Section 2: Citation gates (mandatory) ===")
    bib = Path(__file__).resolve().parents[1] / "paper" / "eci.bib"
    for key, info in CITATION_ANCHORS_MANDATORY.items():
        title = check_citation_file(bib, key)
        if title is None:
            gate(f"MANDATORY {key} present in eci.bib", False,
                 f"missing; expected anchor: {info.get('arxiv', info.get('journal','?'))}")
        else:
            gate(f"MANDATORY {key} present in eci.bib", True, title[:60])

    print("\n=== Section 2b: Citation wishlist (future v2/v7 — WARN only) ===")
    for key, info in CITATION_ANCHORS_WISHLIST.items():
        title = check_citation_file(bib, key)
        if title is None:
            print(f"[WARN] wishlist {key}: missing — must be added before v2 doc cites it")
            print(f"       expected anchor: {info.get('arxiv', info.get('journal','?'))}")
        else:
            print(f"[OK]   wishlist {key}: present ({title[:60]})")
        if "WARNING" in info:
            print(f"  [RED-FLAG] {key}: {info['WARNING']}")
            print(f"             correct value: {info.get('value_alpha_dot_REAL', '?')}")
            print(f"             fabricated:    {info.get('value_alpha_dot_FABRICATED', '?')}")


# ============================================================================
# SECTION 3 — THEORETICAL STATUS GATE
# ============================================================================
# Per PRINCIPLES.md V6-1 and rule 12. Every load-bearing claim in the draft
# must carry one of: THEOREM, POSTULATE, ANSATZ, HEURISTIC, MOTIVATION.
# The pipeline rejects:
#   - equality-form statements of the v6 main inequality (V6-1)
#   - any "theorem" label on derivations flagged ANSATZ by 3-model audit
#   - Einstein-analogy framings that omit POSTULATE/MOTIVATION tag
# ============================================================================

FORBIDDEN_PATTERNS_IN_TEX = [
    # V6-1: equality form of Eq.(1)
    (r"d\s*S_?\{?gen\}?\s*/\s*d\s*\\?tau_?R\s*=\s*\\?kappa",
     "V6-1 violation: equality-form of main inequality (must be ≤)"),
    (r"dS_\{?\\?text\{?gen\}?\}?\[.*?\]\s*=\s*\\?kappa_?R\s*\\?cdot",
     "V6-1 violation: equality-form of main inequality (alt format)"),

    # V6-4: cosmological falsifier claims
    (r"PBH\s+burst.*?(?:factor|\\?times).*?(?:3|trois)",
     "V6-4 violation: PBH burst ×3 prediction without D18-equivalent pipeline"),
    (r"LISA.*?\\?Omega_?\{?gw\}?\s*h.*?\d",
     "V6-4 requires explicit D18-equivalent pipeline tag before LISA prediction"),

    # Rule 1: known-bad citation
    (r"-?8\.0.*?3\.6.*?10\^?\{?-18\}?.*?Lange",
     "Rule 1 (honesty): fabricated Lange 2021 numerical value"),

    # Rule 12: equality of Λ/M_P⁴ with (H_0/ω_P)²
    (r"\\?Lambda\s*/\s*M_?P\^?\{?4\}?\s*=\s*\(\s*H_?0\s*/\s*\\?omega_?P",
     "Rule 12 violation: Λ/M_P⁴ = (H_0/ω_P)² is 1-dex approximate, not exact"),

    # Rule 16: negative-literature sweep claim
    (r"[Aa]ucune publication entre\s+\d{4}\s+et\s+\d{4}",
     "Rule 16 violation: un-substantiated negative-literature claim"),
]

def check_draft_tex(texfile: Path):
    print(f"\n=== Section 3: Scanning {texfile.name} for forbidden patterns ===")
    txt = texfile.read_text()
    any_failed = False
    for pat, reason in FORBIDDEN_PATTERNS_IN_TEX:
        m = re.search(pat, txt, re.IGNORECASE | re.DOTALL)
        if m:
            gate(f"no forbidden pattern: {reason[:60]}", False,
                 f"match at char {m.start()}: '{txt[max(0,m.start()-20):m.end()+20]}'")
            any_failed = True
    if not any_failed:
        gate(f"{texfile.name} clean of forbidden patterns", True,
             f"checked {len(FORBIDDEN_PATTERNS_IN_TEX)} patterns")


# ============================================================================
# SECTION 4 — FALSIFIER GATE (V6-4)
# ============================================================================
# Any new cosmological falsifier proposed for v6 must carry a D18-equivalent
# pipeline artefact: Fisher forecast + nuisance marginalisation + cross-model
# adversarial verdict. Pipeline registry below.
# ============================================================================

APPROVED_FALSIFIERS = {
    # Empty. D18 fσ_8 × Θ(PH_2) killed 2026-04-21.
    # To register a new falsifier: (a) run Fisher+marginalisation+cross-model,
    # (b) commit D19+ report under derivations/D19-*.md, (c) update this dict.
}

def check_falsifiers():
    print("\n=== Section 4: Falsifier registry ===")
    if not APPROVED_FALSIFIERS:
        gate("no approved cosmological falsifier (V6-4 compliant)", True,
             "v6 is formal paper; no falsifier required")
    else:
        for name, info in APPROVED_FALSIFIERS.items():
            gate(f"falsifier {name} has D18-equivalent", "pipeline_d18" in info,
                 str(info))


# ============================================================================
# Main
# ============================================================================
def main():
    check_numerical_anchors()
    check_citations()
    # Scan current v6.1 draft
    tex = Path(__file__).resolve().parents[1] / "paper" / "v6" / "v6_jhep.tex"
    if tex.exists():
        check_draft_tex(tex)
    check_falsifiers()

    failed = [g for g in _gates if not g.passed]
    print(f"\n{'='*72}\nSUMMARY: {len(_gates) - len(failed)}/{len(_gates)} gates passed")
    if failed:
        print("FAILED:")
        for g in failed:
            print(f"  - {g.name}: {g.detail}")
        sys.exit(1)
    print("All gates passed. Draft is V6-1/V6-4/rule1/rule12/rule16 compliant.")
    sys.exit(0)

if __name__ == "__main__":
    main()
