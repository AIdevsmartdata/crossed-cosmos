#!/usr/bin/env python3
"""zenodo-apply.py — batch-update metadata on Zenodo records derived from the
ECI concept DOI (10.5281/zenodo.19686398).

Fixes the bug where the 23 auto-archived versions of `crossed-cosmos` all
inherited the generic v4 title. Applies 4 curated JSON specs to the matching
version records (v5, v6, v7-note, chimere-omega).

SAFETY
------
- Token never printed.
- Default mode is --dry-run: shows a diff per record and writes nothing.
- Never publishes without --publish AND --confirm flags together.

Usage
-----
    export ZENODO_TOKEN=...
    python3 zenodo-apply.py --dry-run            # preview diffs, no PUT
    python3 zenodo-apply.py --apply              # open drafts + PUT metadata, leave UNPUBLISHED
    python3 zenodo-apply.py --apply --publish --confirm   # fully publish

Mapping heuristic (title -> spec):
    "v5"         or "DESI"              -> zenodo-v5-2026-04-24.json
    "v6"         or "type-II" / "GSL"   -> zenodo-v6-2026-04-24.json
    "v7"         or "Riemann" / "BK"    -> zenodo-v7-2026-04-24.json
    "omega" / "Ω" / "Chimère"           -> zenodo-chimere-omega-2026-04-24.json
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

ZENODO_BASE = "https://zenodo.org/api"
CONCEPT_RECID = "19686398"   # concept DOI 10.5281/zenodo.19686398

# Spec dir resolution (CI-safe):
#   1. $ZENODO_SPEC_DIR if set (workflow passes this)
#   2. <this script's dir>/zenodo_metadata/ if it exists (repo layout)
#   3. ~/Bureau/ if the v5 file is there (Kevin's workstation)
_env_dir = os.environ.get("ZENODO_SPEC_DIR")
_repo_dir = Path(__file__).resolve().parent / "zenodo_metadata"
_bureau_dir = Path("~/Bureau").expanduser()
if _env_dir:
    SPEC_DIR = Path(_env_dir)
elif _repo_dir.exists():
    SPEC_DIR = _repo_dir
elif (_bureau_dir / "zenodo-v5-2026-04-24.json").exists():
    SPEC_DIR = _bureau_dir
else:
    SPEC_DIR = _repo_dir  # default, may fail with clear error below

SPECS = {
    "v5":    SPEC_DIR / "zenodo-v5-2026-04-24.json",
    "v6":    SPEC_DIR / "zenodo-v6-2026-04-24.json",
    "v7":    SPEC_DIR / "zenodo-v7-2026-04-24.json",
    "omega": SPEC_DIR / "zenodo-chimere-omega-2026-04-24.json",
}


# ----------------------------- HTTP helpers -----------------------------
def _req(method: str, url: str, token: Optional[str] = None,
         data: Optional[bytes] = None, headers: Optional[dict] = None) -> dict:
    headers = dict(headers or {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")
        print(f"[zenodo] HTTP {e.code} on {method} {url}\n  {msg[:600]}",
              file=sys.stderr)
        raise


# ----------------------------- Classification -----------------------------
def classify(title: str) -> Optional[str]:
    """Legacy title-based classifier (kept for reference / fallback)."""
    t = title.lower()
    if " v4" in t or t.startswith("eci v4"):
        return None
    if "omega" in t or "Ω" in title or "chimère" in t or "chimere ω" in t:
        return "omega"
    if " v7" in t or "v7-note" in t or "riemann" in t or "bogomolny" in t or "odlyzko" in t:
        return "v7"
    if " v6" in t or "type-ii" in t or "gsl" in t or "faulkner" in t or "crossed-product algebras" in t:
        return "v6"
    if " v5" in t or "desi dr2" in t or "quintessence" in t or "pantheon" in t or "non-minimally coupled" in t:
        return "v5"
    return None


def classify_by_version(version: str) -> Optional[str]:
    """Primary classifier — uses Zenodo's `version` field (git tag).

    v4.*                → None (framework paper, leave as-is)
    v5.* / v5.0-preview → v5
    v6.*                → v6
    v7-note-* / v7.*    → v7
    chimere-omega-*     → omega
    """
    if not version:
        return None
    v = version.lower().strip()
    if v.startswith("chimere-omega") or v == "omega" or v.startswith("omega-"):
        return "omega"
    if v.startswith("v7-note") or v.startswith("v7.") or v == "v7":
        return "v7"
    if v.startswith("v6"):
        return "v6"
    if v.startswith("v5"):
        return "v5"
    if v.startswith("v4"):
        return None  # framework paper — leave alone
    return None


def classify_by_title(title: str) -> Optional[str]:
    """Fallback classifier by title keywords — used when `version` field was
    already rewritten to a bare "5.0.2" / "0.1" form by a previous apply.
    The post-apply titles are distinctive enough to disambiguate.
    """
    if not title:
        return None
    t = title.lower()
    if "chimère ω" in t or "chimere ω" in t or "chimere-omega" in t or "chimère omega" in t:
        return "omega"
    if "eci v7" in t or "v7-note" in t or "empirical bogomolny" in t or "odlyzko" in t:
        return "v7"
    if "eci v6" in t or "faulkner" in t or "generalised second law" in t:
        return "v6"
    if "eci v5" in t or "desi dr2" in t or "pantheon+" in t or "phenomenological framework with desi" in t:
        return "v5"
    # Don't match generic "ECI v4 — ..." — that's the framework paper.
    return None


# ----------------------------- Versions list -----------------------------
def list_concept_versions(token: str) -> list[dict]:
    """List every version of the concept record via deposit API.

    GET /api/deposit/depositions?q=conceptrecid:<id>&size=100&all_versions=true
    """
    url = (f"{ZENODO_BASE}/deposit/depositions"
           f"?q=conceptrecid:{CONCEPT_RECID}"
           f"&size=100&all_versions=true&sort=-mostrecent")
    data = _req("GET", url, token=token)
    if isinstance(data, list):
        return data
    return data.get("hits", {}).get("hits", [])


# ----------------------------- Diff & apply -----------------------------
def diff_metadata(current: dict, target: dict) -> list[str]:
    changes = []
    tracked = ["title", "description", "keywords", "version",
               "publication_date", "related_identifiers"]
    for k in tracked:
        cur = current.get(k)
        new = target.get(k)
        if cur != new:
            def _fmt(v):
                s = json.dumps(v, ensure_ascii=False) if v is not None else "∅"
                return s[:180] + ("…" if len(s) > 180 else "")
            changes.append(f"  {k}:\n     cur: {_fmt(cur)}\n     new: {_fmt(new)}")
    return changes


def update_record(dep_id: str, metadata: dict, token: str,
                  publish: bool = False) -> dict:
    """Open edit mode on a published record, PUT new metadata, optionally publish."""
    # If record is published, we must call /actions/edit first to unlock it
    try:
        _req("POST",
             f"{ZENODO_BASE}/deposit/depositions/{dep_id}/actions/edit",
             token=token)
    except urllib.error.HTTPError as e:
        if e.code not in (400, 403):  # 400 ≈ already in edit; 403 ≈ maybe unsubmitted
            raise

    body = json.dumps({"metadata": metadata}).encode()
    updated = _req("PUT",
                   f"{ZENODO_BASE}/deposit/depositions/{dep_id}",
                   token=token, data=body)
    if publish:
        published = _req(
            "POST",
            f"{ZENODO_BASE}/deposit/depositions/{dep_id}/actions/publish",
            token=token)
        return published
    return updated


# ----------------------------- Main -----------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Print diffs only. Default if no other mode given.")
    ap.add_argument("--apply", action="store_true",
                    help="Open drafts + PUT metadata. Drafts stay UNPUBLISHED.")
    ap.add_argument("--publish", action="store_true",
                    help="Publish each updated draft. Requires --apply and --confirm.")
    ap.add_argument("--confirm", action="store_true",
                    help="Required with --publish to prevent accidental publication.")
    ap.add_argument("--only", choices=list(SPECS.keys()) + ["all"],
                    default="all", help="Target a single spec or all.")
    ap.add_argument("--ids", default="",
                    help="Explicit record-id → spec map, comma-separated: "
                         "e.g. 'v5=19701245,v6=19708665,v7=19700036,omega=19700868'. "
                         "Bypasses classify_by_version — useful when drafts are "
                         "already PUT and classify no longer matches.")
    ap.add_argument("--list", action="store_true",
                    help="List every record under the concept with all "
                         "disambiguating fields (id, title, version, filename, "
                         "pub_date, related_identifiers). No classification, "
                         "no changes. Use this first when the 4 records all "
                         "inherit the same generic title.")
    args = ap.parse_args()

    if not args.apply and not args.publish and not args.list:
        args.dry_run = True

    if args.publish and not (args.apply and args.confirm):
        print("error: --publish requires both --apply and --confirm", file=sys.stderr)
        return 2

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("error: ZENODO_TOKEN not set in env", file=sys.stderr)
        return 2

    # Load specs
    targets: dict[str, dict] = {}
    for k, p in SPECS.items():
        if args.only != "all" and args.only != k:
            continue
        if not p.exists():
            print(f"error: spec file missing: {p}", file=sys.stderr)
            return 3
        with p.open() as f:
            targets[k] = json.load(f)["metadata"]

    # Enumerate records
    print(f"[zenodo] listing all versions of concept {CONCEPT_RECID}...")
    try:
        versions = list_concept_versions(token)
    except urllib.error.HTTPError as e:
        print(f"error: could not list versions (HTTP {e.code}). "
              f"Token scope must include `deposit:write`.", file=sys.stderr)
        return 4
    print(f"[zenodo] {len(versions)} records under concept")

    # --list mode: print everything disambiguating, then exit.
    if args.list:
        print("\n=== RECORD LISTING (no changes) ===")
        # Sort by publication_date descending so newest is first
        sorted_recs = sorted(
            versions,
            key=lambda r: r.get("metadata", {}).get("publication_date", ""),
            reverse=True,
        )
        for rec in sorted_recs:
            rid = rec.get("id")
            doi = rec.get("doi") or rec.get("conceptdoi") or "—"
            md = rec.get("metadata", {})
            title = md.get("title", "")
            version = md.get("version", "")
            pub = md.get("publication_date", "")
            files = rec.get("files", [])
            filenames = [f.get("filename", "?") for f in files]
            rel = md.get("related_identifiers", [])
            rel_brief = [f"{r.get('relation','?')}={r.get('identifier','?')}" for r in rel[:3]]
            print(f"\n  id={rid}  doi={doi}  pub={pub}")
            print(f"    title   : {title[:120]}")
            if version:
                print(f"    version : {version}")
            if filenames:
                print(f"    files   : {filenames[:3]}")
            if rel_brief:
                print(f"    rels    : {rel_brief}")
        print(f"\n[zenodo] list done ({len(versions)} records).")
        return 0

    # Match each record by `version` field. Option A semantics (2026-04-24):
    # every version of the v5 / v6 / v7-note / chimere-omega papers receives
    # the corresponding metadata. Only v4.* (framework paper) is left alone.
    matched: dict[str, list[dict]] = {k: [] for k in targets}
    unmatched: list[dict] = []
    skipped_no_files: list[dict] = []

    # Pre-compute explicit id→key overrides from --ids flag, if any.
    explicit_ids: dict[str, str] = {}   # rec_id (str) → spec_key
    if args.ids:
        for entry in args.ids.split(","):
            entry = entry.strip()
            if not entry:
                continue
            if "=" not in entry:
                print(f"warn: --ids entry '{entry}' ignored (missing '=')", file=sys.stderr)
                continue
            k, rid = entry.split("=", 1)
            k = k.strip()
            rid = rid.strip()
            if k not in SPECS:
                print(f"warn: --ids key '{k}' unknown (expected one of {list(SPECS.keys())})", file=sys.stderr)
                continue
            explicit_ids[rid] = k
        if explicit_ids:
            print(f"[zenodo] --ids override: {explicit_ids}")

    # DEBUG — show first 4 records so we can see why matching fails
    print("\n=== DEBUG: first 4 records seen by apply path ===")
    for rec in versions[:4]:
        rid = str(rec.get("id", ""))
        md = rec.get("metadata", {})
        version = md.get("version", "")
        files = rec.get("files", [])
        title = md.get("title", "")
        key_pv = classify_by_version(version)
        key_ex = explicit_ids.get(rid)
        print(f"  id={rid} version={version!r} files_n={len(files)} "
              f"title[0:40]={title[:40]!r} key_pv={key_pv} key_ex={key_ex}")
    print()

    for rec in versions:
        rid = str(rec.get("id", ""))
        md = rec.get("metadata", {})
        version = md.get("version", "")
        title = md.get("title", "")
        state = rec.get("state", "")
        # Explicit id overrides > version classify > title classify.
        if rid in explicit_ids:
            key = explicit_ids[rid]
        else:
            key = classify_by_version(version) or classify_by_title(title)
        if key and key in targets:
            # No-files guard: only skip records that are UNSUBMITTED (brand
            # new drafts with no content). `state == "inprogress"` is an
            # edit-draft of a published record — files live on the parent
            # record and the publish action handles inheritance. `state ==
            # "done"` is a published record (we want to edit it). Explicit
            # --ids override bypasses the guard entirely.
            files_ok = bool(rec.get("files")) or state in ("inprogress", "done") or rid in explicit_ids
            if not files_ok:
                skipped_no_files.append(rec)
                continue
            matched[key].append(rec)
        else:
            unmatched.append(rec)

    # Sort each bucket by version so the diff is readable
    for k in matched:
        matched[k].sort(key=lambda r: r.get("metadata", {}).get("version", ""))

    # Report
    print("\n=== MATCHING (by version prefix) ===")
    total_matched = 0
    for k in targets:
        recs = matched.get(k, [])
        total_matched += len(recs)
        if not recs:
            print(f"  [{k:>5}] no records match")
        else:
            print(f"  [{k:>5}] {len(recs)} record(s):")
            for rec in recs:
                ver = rec.get("metadata", {}).get("version", "?")
                print(f"            id={rec.get('id')}  version={ver}")

    print(f"\n  ({len(unmatched)} records un-targeted = framework v4.* + any "
          f"uncaught; will be left alone)")
    if skipped_no_files:
        print(f"  ({len(skipped_no_files)} records skipped — no files, "
              f"likely edit-drafts):")
        for rec in skipped_no_files:
            ver = rec.get("metadata", {}).get("version", "?")
            print(f"      id={rec.get('id')} version={ver}")

    print(f"\n  TOTAL to update: {total_matched} record(s)")

    # Per-record action
    for k, target_md in targets.items():
        recs = matched.get(k, [])
        for rec in recs:
            dep_id = str(rec["id"])
            ver = rec.get("metadata", {}).get("version", "?")
            print(f"\n=== [{k}] id={dep_id} version={ver} ===")
            changes = diff_metadata(rec.get("metadata", {}), target_md)
            if not changes:
                print("  (no metadata change)")
                continue
            for c in changes:
                print(c)

            if args.dry_run:
                print("  (dry-run — skipping PUT)")
                continue

            print("  → PUT /deposit/depositions/{id}  ...")
            try:
                update_record(dep_id, target_md, token,
                              publish=(args.publish and args.confirm))
                print("  ✓ updated" + (" & published" if args.publish else " (draft)"))
            except urllib.error.HTTPError as e:
                print(f"  ✗ failed HTTP {e.code}", file=sys.stderr)

    print("\n[zenodo] done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
