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


def find_record_for_tag(tag: str, token: Optional[str] = None) -> Optional[dict]:
    """Scan /versions for the concept record, return the one whose
    `metadata.version` matches `tag`. Paginate (anon cap 25/page, auth 100).
    """
    page_size = 100 if token else 25
    page = 1
    while True:
        url = (f"{ZENODO_BASE}/records/{CONCEPT_RECORD_ID}/versions"
               f"?size={page_size}&page={page}")
        d = _req("GET", url, token=token)
        hits = d.get("hits", {}).get("hits", [])
        if not hits:
            return None
        for h in hits:
            if h.get("metadata", {}).get("version") == tag:
                return h
        total = d.get("hits", {}).get("total", 0)
        if page * page_size >= total:
            return None
        page += 1


def record_has_pdf(rec: dict, pdf_name: str) -> bool:
    for f in rec.get("files", []):
        if f.get("key") == pdf_name:
            return True
    return False


def new_version(published_id: str, token: str) -> dict:
    """Create a new draft version using the InvenioRDM API.

    POST /api/records/{id}/versions — new-style endpoint. Inherits
    metadata from parent but starts with files disabled; we must
    re-import files (or upload fresh ones) then publish.
    """
    url = f"{ZENODO_BASE}/records/{published_id}/versions"
    return _req("POST", url, token=token)


def import_parent_files(draft_id: str, token: str) -> dict:
    """Tell the draft to copy files from its parent version."""
    url = f"{ZENODO_BASE}/records/{draft_id}/draft/actions/files-import"
    return _req("POST", url, token=token)


def draft_unlock_files(draft_id: str, token: str) -> dict:
    """Allow new files to be added to the draft (sets files.enabled=true)."""
    url = f"{ZENODO_BASE}/records/{draft_id}/draft"
    body = json.dumps({"files": {"enabled": True}}).encode()
    return _req("PUT", url, token=token, data=body)


def upload_pdf(draft_id: str, pdf_path: Path, token: str):
    """Upload a file to a draft using the InvenioRDM two-phase protocol:
    1) POST /records/{id}/draft/files with [{"key": filename}] to declare
    2) PUT  /records/{id}/draft/files/{filename}/content with the bytes
    3) POST /records/{id}/draft/files/{filename}/commit
    """
    name = pdf_path.name
    # 1) declare
    declare_url = f"{ZENODO_BASE}/records/{draft_id}/draft/files"
    declare_body = json.dumps([{"key": name}]).encode()
    try:
        _req("POST", declare_url, token=token, data=declare_body)
    except urllib.error.HTTPError as e:
        if e.code != 400:  # 400 may mean already declared, try to proceed
            raise
    # 2) upload content
    content_url = f"{ZENODO_BASE}/records/{draft_id}/draft/files/{urllib.parse.quote(name)}/content"
    with pdf_path.open("rb") as f:
        data = f.read()
    _req("PUT", content_url, token=token, data=data,
         headers={"Content-Type": "application/octet-stream"})
    # 3) commit
    commit_url = f"{ZENODO_BASE}/records/{draft_id}/draft/files/{urllib.parse.quote(name)}/commit"
    _req("POST", commit_url, token=token)
    print(f"[zenodo] uploaded {name} ({len(data)/1024:.0f} KB)")


def publish(draft_id: str, token: str) -> dict:
    url = f"{ZENODO_BASE}/records/{draft_id}/draft/actions/publish"
    return _req("POST", url, token=token)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", help="Release tag to update")
    ap.add_argument("--record", help="Direct Zenodo record ID")
    ap.add_argument("--pdf-dir", help="Dir containing PDF assets")
    ap.add_argument("--pdf", nargs="*", default=[],
                    help="Explicit PDF paths to upload")
    ap.add_argument("--publish-draft", metavar="ID",
                    help="Publish an existing unsubmitted draft by ID "
                         "(skip newversion+upload). For resuming partial runs.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # Resume mode: draft already created, just publish it.
    if args.publish_draft:
        token = os.environ.get("ZENODO_TOKEN")
        if not token:
            print("error: ZENODO_TOKEN not set", file=sys.stderr); return 2
        draft_id = args.publish_draft
        # Drafts created via the legacy `deposit/depositions/.../actions/
        # newversion` endpoint carry legacy-shaped metadata. The new
        # `/records/.../draft/actions/publish` endpoint validates against
        # the InvenioRDM schema and fails on metadata.resource_type etc.
        # Use the LEGACY publish endpoint instead — it accepts legacy
        # drafts. For drafts created via the new API, call publish() as
        # written in the full-flow path (not here).
        legacy_url = f"{ZENODO_BASE}/deposit/depositions/{draft_id}/actions/publish"
        print(f"Publishing existing draft {draft_id} via legacy endpoint...")
        published = _req("POST", legacy_url, token=token)
        new_doi = (published.get("doi")
                   or published.get("pids", {}).get("doi", {}).get("identifier"))
        print(f"✓ Published. New DOI: {new_doi}")
        return 0

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
        rec = find_record_for_tag(args.tag, token=token)
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

    # Published records are immutable: open a NEW VERSION via
    # /records/{id}/versions (InvenioRDM API), import parent files,
    # add PDFs, publish.
    print("Opening new draft version...")
    draft = new_version(rec_id, token)
    draft_id = str(draft.get("id"))
    if not draft_id or draft_id == "None":
        print(f"error: no draft id in response: {draft}", file=sys.stderr)
        return 4
    print(f"Draft {draft_id} created")

    # Import parent's files (zipball) so the new version isn't empty.
    try:
        import_parent_files(draft_id, token)
        print(f"Imported parent files into draft {draft_id}")
    except urllib.error.HTTPError as e:
        # Some drafts start with files unlocked or already imported
        print(f"  (files-import returned {e.code}, continuing)")

    for p in missing:
        upload_pdf(draft_id, p, token)

    print(f"Publishing draft {draft_id}...")
    published = publish(draft_id, token)
    new_doi = published.get("pids", {}).get("doi", {}).get("identifier") \
        or published.get("doi")
    print(f"✓ Published new version. New DOI: {new_doi}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
