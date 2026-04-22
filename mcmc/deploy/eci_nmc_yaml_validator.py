#!/usr/bin/env python3
"""
ECI NMC YAML validator.

Loads mcmc/params/eci_nmc.yaml and checks:

  1. Every entry under `params:` is either
       (a) a dict with a `prior`, optionally a `ref` and `proposal`, OR
       (b) a derived parameter (dict with only `latex` / `derived: true`), OR
       (c) a fixed scalar value (int/float/str).
  2. Every `likelihood:` entry resolves to a known Cobaya cosmo package
     (Planck 2018, ACT DR6, DESI DR2, Pantheon+, etc.). Unknown entries are
     reported as "cobaya-install cosmo pending" rather than hard-failing so
     that offline validation stays useful.
  3. The `theory:` block points to `classy` (vanilla) or a custom NMC theory
     whose module is resolvable — the custom path is accepted as *pending*
     when the sibling agents (hi_class C patch or cobaya-nmc plugin) have
     not yet landed.

Exit code: 0 on clean pass, 1 on any hard failure (category 1 above).
Category-2/3 "pending" items are WARNINGS, not errors.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    sys.stderr.write("ERROR: PyYAML not installed. `pip install pyyaml`.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parents[2]
YAML_PATH = REPO_ROOT / "mcmc" / "params" / "eci_nmc.yaml"

# Cobaya `cosmo` bundle — packages installed by `cobaya-install cosmo`.
# Source: cobaya docs (v3.5) cosmo_input registry.
KNOWN_LIKELIHOODS = {
    # Planck 2018
    "planck_2018_lowl.TT",
    "planck_2018_lowl.EE",
    "planck_2018_lowl.TT_clik",
    "planck_2018_lowl.EE_clik",
    "planck_2018_highl_plik.TT",
    "planck_2018_highl_plik.TTTEEE",
    "planck_2018_highl_plik.TT_lite",
    "planck_2018_highl_plik.TTTEEE_lite",
    "planck_2018_highl_CamSpec.TT",
    "planck_2018_highl_CamSpec.TTTEEE",
    "planck_2018_lensing.clik",
    "planck_2018_lensing.native",
    "planck_NPIPE_highl_CamSpec.TTTEEE",
    # ACT
    "act_dr4.TE",
    "act_dr4.TT",
    "act_dr6_lenslike.ACTDR6LensLike",
    "act_dr6_cmbonly",
    # BAO
    "bao.desi_dr1",
    "bao.desi_dr2",
    "bao.sdss_dr16_baoplus_lrg",
    "bao.sdss_dr16_baoplus_elg",
    "bao.sixdf_2011_bao",
    "bao.sdss_dr7_mgs",
    # Supernovae
    "sn.pantheon_plus",
    "sn.pantheon",
    "sn.union3",
    "sn.des_y5",
    "sn.jla",
    # BBN
    "bbn.schoneberg",
    # H0 local
    "H0.riess2020",
    "H0.riess2020Mb",
    "H0.freedman2020",
}

KNOWN_THEORIES = {
    "classy",                     # vanilla CLASS
    "camb",                       # CAMB (not used here, but valid)
    "classy_nmc",                 # pending — hi_class C patch route
    "cobaya_nmc.NMCTheory",       # pending — Cobaya plugin route
}


def _is_param_with_prior(v: Any) -> bool:
    return isinstance(v, dict) and "prior" in v


def _is_derived(v: Any) -> bool:
    if not isinstance(v, dict):
        return False
    if v.get("derived") is True:
        return True
    # Common derived declaration: {latex: ...} with no prior.
    if "prior" not in v and set(v.keys()).issubset({"latex", "derived", "min", "max"}):
        return True
    return False


def _is_fixed(v: Any) -> bool:
    return isinstance(v, (int, float, str, bool))


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return [f"YAML not found: {path}"], []

    with path.open("r", encoding="utf-8") as fh:
        try:
            doc = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            return [f"YAML parse error: {exc}"], []

    if not isinstance(doc, dict):
        return [f"Top-level YAML is not a mapping (got {type(doc).__name__})"], []

    # ------------------------------------------------------------------ params
    params = doc.get("params", {}) or {}
    if not isinstance(params, dict):
        errors.append("`params:` must be a mapping")
    else:
        for name, spec in params.items():
            if _is_fixed(spec):
                continue
            if _is_param_with_prior(spec):
                if "ref" not in spec:
                    warnings.append(f"param '{name}': no `ref` (optional but recommended)")
                continue
            if _is_derived(spec):
                continue
            errors.append(
                f"param '{name}': neither a prior-bearing sampled param, a derived param, nor a fixed scalar"
            )

    # -------------------------------------------------------------- likelihood
    liks = doc.get("likelihood", {}) or {}
    if not isinstance(liks, dict):
        errors.append("`likelihood:` must be a mapping")
    else:
        for lk in liks.keys():
            if lk not in KNOWN_LIKELIHOODS:
                warnings.append(
                    f"likelihood '{lk}': not in the known cosmo registry — "
                    "will resolve after `cobaya-install cosmo` if upstream provides it"
                )

    # ------------------------------------------------------------------ theory
    theory = doc.get("theory", {}) or {}
    if not isinstance(theory, dict) or not theory:
        errors.append("`theory:` missing or empty")
    else:
        for th in theory.keys():
            if th in KNOWN_THEORIES:
                if th in {"classy_nmc", "cobaya_nmc.NMCTheory"}:
                    warnings.append(
                        f"theory '{th}': sibling-agent pending — ensure hi_class C patch "
                        "OR cobaya-nmc plugin is installed before the cloud run"
                    )
            else:
                warnings.append(f"theory '{th}': unknown — accepted as custom pending")

    # --------------------------------------------------------------- sampler
    sampler = doc.get("sampler", {}) or {}
    if not isinstance(sampler, dict) or not sampler:
        errors.append("`sampler:` missing or empty")

    return errors, warnings


def main() -> int:
    print(f"eci_nmc_yaml_validator: checking {YAML_PATH}")
    errors, warnings = validate(YAML_PATH)

    for w in warnings:
        print(f"  [WARN] {w}")
    for e in errors:
        print(f"  [ERR ] {e}")

    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    rc = main()
    # The task spec says: `assert` exit 0 if clean, exit 1 otherwise.
    assert rc in (0, 1)
    sys.exit(rc)
