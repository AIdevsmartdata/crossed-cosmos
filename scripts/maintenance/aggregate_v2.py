#!/usr/bin/env python3
"""Tolerant aggregator v2 — handle truncated/markdown-wrapped JSON."""
import json
import pathlib
import re

REPORTS_DIR = pathlib.Path("/tmp/fact_check_reports_2026-05-19")
OUT = pathlib.Path("/tmp/MASTER_FACT_CHECK_v2.md")


def parse_smart(content):
    content = content.strip()
    # Strip markdown code fences
    m = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', content, re.DOTALL)
    if m:
        content = m.group(1).strip()
    # Try direct
    try:
        return json.loads(content)
    except:
        pass
    # Extract first {...} substring
    s = content.find('{')
    e = content.rfind('}')
    if s >= 0 and e > s:
        try:
            return json.loads(content[s:e+1])
        except:
            pass
    # Truncated: try to complete at last comma
    if content.startswith('{'):
        # Find last valid stopping point
        for cut in range(len(content), 100, -200):
            attempt = content[:cut].rstrip().rstrip(',') + '\n}'
            try:
                return json.loads(attempt)
            except:
                continue
    return None


def parse_report(path):
    try:
        d = json.load(open(path))
    except:
        return None
    content = (d.get('content', '') or '').strip()
    if not content:
        return None
    return parse_smart(content)


def main():
    by_verdict = {}
    all_data = {}
    for r in sorted(REPORTS_DIR.glob('*.json')):
        data = parse_report(r)
        if data is None:
            by_verdict.setdefault('ERROR_PARSE', []).append(r.stem)
            all_data[r.stem] = None
            continue
        v = data.get('verdict', '?')
        by_verdict.setdefault(v, []).append(r.stem)
        all_data[r.stem] = data

    # Counts
    print("=== Verdict counts ===")
    for v in ['READY_TO_SUBMIT', 'NEEDS_PATCHES', 'REJECT', 'ERROR_PARSE']:
        items = by_verdict.get(v, [])
        if items:
            print(f'  {v}: {len(items)}')
    print()

    # Master summary write
    lines = ["# Master Fact-Check Summary v2 — 2026-05-19", ""]
    lines.append(f"DS Pro V4 medium reasoning, 12k tokens — {len(all_data)} papers")
    lines.append("")
    for v in ['REJECT', 'NEEDS_PATCHES', 'READY_TO_SUBMIT', 'ERROR_PARSE']:
        items = by_verdict.get(v, [])
        if items:
            lines.append(f"## {v} ({len(items)})")
            for it in sorted(items):
                lines.append(f"- `{it}`")
            lines.append("")

    lines.append("")
    lines.append("## Per-paper details (REJECT only)")
    for it in sorted(by_verdict.get('REJECT', [])):
        d = all_data.get(it)
        if not d: continue
        lines.append(f"### `{it}` ({d.get('confidence', '?')})")
        sa = d.get('suspect_attributions', [])
        sc = d.get('scope_overclaims', [])
        if sa:
            lines.append("**Suspect attributions:**")
            for s in sa[:3]:
                lines.append(f"  - *{s.get('line_hint', '?')}*: {s.get('issue', '?')[:200]}")
        if sc:
            lines.append("**Scope overclaims:**")
            for s in sc[:3]:
                lines.append(f"  - {s.get('actual_scope', '?')[:200]}")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary: {OUT}")


if __name__ == "__main__":
    main()
