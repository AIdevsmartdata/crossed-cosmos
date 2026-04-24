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

BUREAU = Path("~/Bureau").expanduser()
SPECS = {
    "v5":    BUREAU / "zenodo-v5-2026-04-24.json",
    "v6":    BUREAU / "zenodo-v6-2026-04-24.json",
    "v7":    BUREAU / "zenodo-v7-2026-04-24.json",
    "omega": BUREAU / "zenodo-chimere-omega-2026-04-24.json",
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
    """Return spec key ('v5','v6','v7','omega') or None from a record title."""
    t = title.lower()
    # Skip v4 framework paper itself
    if " v4" in t or t.startswith("eci v4"):
        # could be the original v4 – leave alone unless caller asks
        return None
    # Chimere Omega
    if "omega" in t or "Ω" in title or "chimère" in t or "chimere ω" in t:
        return "omega"
    # v7-note (Riemann / BK / Odlyzko)
    if " v7" in t or "v7-note" in t or "riemann" in t or "bogomolny" in t or "odlyzko" in t:
        return "v7"
    # v6 (GSL / type-II / Faulkner-Speranza)
    if " v6" in t or "type-ii" in t or "gsl" in t or "faulkner" in t or "crossed-product algebras" in t:
        return "v6"
    # v5 (DESI / quintessence / Pantheon)
    if " v5" in t or "desi dr2" in t or "quintessence" in t or "pantheon" in t or "non-minimally coupled" in t:
        return "v5"
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
    args = ap.parse_args()

    if not args.apply and not args.publish:
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

    # Match each record to a spec
    matched: dict[str, dict] = {}   # spec_key -> chosen record
    unmatched: list[dict] = []
    for rec in versions:
        md = rec.get("metadata", {})
        title = md.get("title", "")
        key = classify(title)
        if key and key in targets:
            # Most-recent heuristic: keep the *latest* pub_date per spec
            prev = matched.get(key)
            if prev is None or md.get("publication_date", "") > \
                    prev.get("metadata", {}).get("publication_date", ""):
                matched[key] = rec
        else:
            unmatched.append(rec)

    # Report
    print("\n=== MATCHING ===")
    for k in targets:
        rec = matched.get(k)
        if rec is None:
            print(f"  [{k:>5}] NO MATCH found in {len(versions)} versions")
        else:
            print(f"  [{k:>5}] → dep_id={rec.get('id')} "
                  f"cur_ver={rec.get('metadata',{}).get('version','?'):>10} "
                  f"title={rec.get('metadata',{}).get('title','')[:70]}")

    if unmatched:
        print(f"\n  ({len(unmatched)} records un-targeted, will be left alone)")

    # Per-record action
    for k, target_md in targets.items():
        rec = matched.get(k)
        if rec is None:
            continue
        dep_id = str(rec["id"])
        print(f"\n=== [{k}] record {dep_id} ===")
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
