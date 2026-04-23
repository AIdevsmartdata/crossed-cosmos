#!/usr/bin/env python3
"""zenodo_push_pdf.py — push release PDFs onto the matching Zenodo record.

Used both by .github/workflows/zenodo-upload-pdf.yml (on release) and
manually for backfilling (ran once on 2026-04-23 to fix the 4 existing
records that only had the source zipball).

Env:
    ZENODO_TOKEN   personal token with deposit:write scope

Usage:
    python3 scripts/zenodo_push_pdf.py --tag v6.0.6 --pdf-dir pdfs/
    python3 scripts/zenodo_push_pdf.py --record 19701287 --pdf foo.pdf

Behavior:
- Resolves the Zenodo record matching a GitHub release tag via the
  concept DOI's /versions API.
- If the record is still in "unsubmitted" state (webhook just fired
  and Zenodo draft is open): add files then publish.
- If the record is already published: open a new draft version, add
  files, publish. Zenodo mints a new DOI for that new version; old
  DOIs stay valid and resolvable.

Concept DOI for crossed-cosmos: 10.5281/zenodo.19686399 (pinned here
so we do not depend on any env var in CI).
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

ZENODO_BASE = "https://zenodo.org/api"
CONCEPT_RECORD_ID = "19686399"  # crossed-cosmos concept (parent of all versions)


def _req(method: str, url: str, token: Optional[str] = None,
         data: Optional[bytes] = None,
         headers: Optional[dict] = None) -> dict:
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
        body = e.read().decode(errors="replace")
        print(f"[zenodo] HTTP {e.code} on {method} {url}\n  {body[:500]}",
              file=sys.stderr)
        raise


def find_record_for_tag(tag: str) -> Optional[dict]:
    """Scan /versions for the concept record, return the one whose
    `metadata.version` matches `tag`.
    """
    url = f"{ZENODO_BASE}/records/{CONCEPT_RECORD_ID}/versions?size=50"
    d = _req("GET", url)
    hits = d.get("hits", {}).get("hits", [])
    for h in hits:
        if h.get("metadata", {}).get("version") == tag:
            return h
    return None


def record_has_pdf(rec: dict, pdf_name: str) -> bool:
    for f in rec.get("files", []):
        if f.get("key") == pdf_name:
            return True
    return False


def new_version(concept_id: str, token: str) -> dict:
    """Create a new draft version of the concept record."""
    url = f"{ZENODO_BASE}/deposit/depositions/{concept_id}/actions/newversion"
    return _req("POST", url, token=token)


def get_draft(concept_id: str, token: str) -> dict:
    """Some flows return the draft id in 'links.latest_draft'."""
    url = f"{ZENODO_BASE}/deposit/depositions/{concept_id}"
    return _req("GET", url, token=token)


def upload_pdf(draft: dict, pdf_path: Path, token: str):
    """Upload a file to a draft deposition. Supports both old (files) and
    new bucket API. Prefer bucket."""
    bucket_url = draft.get("links", {}).get("bucket")
    if bucket_url:
        # Bucket API: PUT <bucket>/<filename>  body = raw bytes
        url = f"{bucket_url}/{urllib.parse.quote(pdf_path.name)}"
        with pdf_path.open("rb") as f:
            data = f.read()
        _req("PUT", url, token=token, data=data,
             headers={"Content-Type": "application/octet-stream"})
        print(f"[zenodo] uploaded (bucket) {pdf_path.name} "
              f"({len(data)/1024:.0f} KB)")
        return
    # Fallback old API
    raise RuntimeError("no bucket link on draft — API may have changed")


def publish(draft_id: str, token: str) -> dict:
    url = f"{ZENODO_BASE}/deposit/depositions/{draft_id}/actions/publish"
    return _req("POST", url, token=token)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", help="Release tag to update")
    ap.add_argument("--record", help="Direct Zenodo record ID")
    ap.add_argument("--pdf-dir", help="Dir containing PDF assets")
    ap.add_argument("--pdf", nargs="*", default=[],
                    help="Explicit PDF paths to upload")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.environ.get("ZENODO_TOKEN")
    if not token and not args.dry_run:
        print("error: ZENODO_TOKEN not set", file=sys.stderr)
        return 2

    # Collect PDFs
    pdfs: list[Path] = [Path(p) for p in args.pdf if Path(p).exists()]
    if args.pdf_dir:
        pdfs.extend(sorted(Path(args.pdf_dir).glob("*.pdf")))
    pdfs = [p for p in pdfs if p.exists()]
    if not pdfs:
        print("warn: no PDFs found — nothing to do")
        return 0
    print(f"PDFs to push: {[str(p) for p in pdfs]}")

    # Resolve record
    if args.tag:
        rec = find_record_for_tag(args.tag)
        if rec is None:
            print(f"error: no Zenodo record for tag {args.tag!r}", file=sys.stderr)
            return 3
    elif args.record:
        rec = _req("GET", f"{ZENODO_BASE}/records/{args.record}")
    else:
        print("error: need --tag or --record", file=sys.stderr)
        return 2

    rec_id = str(rec["id"])
    version = rec.get("metadata", {}).get("version", "?")
    print(f"Matched Zenodo record {rec_id} (version {version})")

    # Check if PDFs are already there
    missing = [p for p in pdfs if not record_has_pdf(rec, p.name)]
    if not missing:
        print("All PDFs already present on that record — nothing to do.")
        return 0
    print(f"Missing on record: {[p.name for p in missing]}")

    if args.dry_run:
        print("(dry-run) would upload and publish a new version")
        return 0

    # Published records are immutable: open a NEW VERSION, add PDFs,
    # publish. Zenodo promotes existing files to the new version
    # automatically, so the new record will have both zipball AND PDFs.
    print("Opening new draft version via newversion action...")
    nv = new_version(rec_id, token)
    draft_url = nv.get("links", {}).get("latest_draft")
    if not draft_url:
        print(f"error: no latest_draft link on newversion response: {nv}",
              file=sys.stderr)
        return 4
    draft_id = re.search(r"/(\d+)(?:/|$)", draft_url).group(1)
    draft = _req("GET", f"{ZENODO_BASE}/deposit/depositions/{draft_id}",
                 token=token)

    for p in missing:
        upload_pdf(draft, p, token)

    # Publish
    print(f"Publishing draft {draft_id}...")
    published = publish(draft_id, token)
    new_doi = published.get("doi")
    print(f"✓ Published new version. New DOI: {new_doi}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
