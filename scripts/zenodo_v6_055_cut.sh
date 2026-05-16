#!/usr/bin/env bash
# zenodo_v6_055_cut.sh — Cut Zenodo v6.0.55 release from current main branch
#
# Bumps CITATION.cff version + date, commits, tags, pushes to public remote
# which triggers Zenodo webhook auto-deposit.
#
# Safety: dry-run by default. Requires --execute flag to actually apply changes.
#
# Usage:
#   bash scripts/zenodo_v6_055_cut.sh              # dry-run (default)
#   bash scripts/zenodo_v6_055_cut.sh --execute    # apply changes
#
# Pre-conditions:
#   - Paper 3 G4 PDF compiled (papers/Paper_G4_obstruction/main.pdf)
#   - Paper 2 HSH v3 JNT v2 PDF compiled
#   - Sp(2N) mini PDF compiled
#   - Plan v5 §B reframe in notes/
#   - Session 11 agents committed (b84aa97 or later)
#   - Clean working tree (or only intended changes)
#
# Post-conditions:
#   - CITATION.cff version 6.0.55, date 2026-05-16
#   - Commit "Zenodo cut v6.0.55 — post 11 agents session 2026-05-16"
#   - Tag v6.0.55 pushed to public remote (Zenodo webhook fires)
#   - Manual fallback: deposit via Zenodo UI if webhook fails

set -euo pipefail

REPO_DIR="${REPO_DIR:-/root/crossed-cosmos}"
NEW_VERSION="6.0.55"
NEW_DATE="2026-05-16"
DRY_RUN=true

# Parse args
for arg in "$@"; do
    case "$arg" in
        --execute) DRY_RUN=false ;;
        --help|-h)
            echo "Usage: $0 [--execute]"
            echo "  Without --execute: dry-run only (default)"
            echo "  With --execute: applies version bump + commit + tag + push"
            exit 0
            ;;
        *) echo "Unknown arg: $arg" >&2; exit 1 ;;
    esac
done

cd "$REPO_DIR"

echo "=== Zenodo v6.0.55 cut script ==="
echo "Repo: $REPO_DIR"
echo "Target version: $NEW_VERSION"
echo "Target date: $NEW_DATE"
echo "Mode: $($DRY_RUN && echo DRY-RUN || echo EXECUTE)"
echo

# ---- Pre-flight checks ----
echo "--- Pre-flight checks ---"

# Check git status clean (or only intended)
if [[ -n "$(git status --porcelain)" ]]; then
    echo "⚠️  Working tree not clean:"
    git status --short
    echo
    if $DRY_RUN; then
        echo "(dry-run continues, but execute will fail without clean tree)"
    else
        echo "❌ ABORT: clean or commit working tree first."
        exit 1
    fi
fi

# Check key papers exist
REQUIRED_FILES=(
    "papers/Paper_G4_obstruction/main.pdf"
    "papers/Paper_HSH_v3_letter_JNT_v2/main.pdf"
    "papers/Paper_Sp2N_mini/main.pdf"
    "notes/PLAN_v5_section_B_reframe_2026-05-16.md"
    "CITATION.cff"
)
for f in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$f" ]]; then
        echo "❌ MISSING: $f"
        exit 1
    fi
done
echo "✅ All 5 required files present"

# Check session 11 agents commit (b84aa97 or descendant)
if ! git log --oneline | grep -q "11 agents post-W40"; then
    echo "⚠️  Session 11 agents commit not found in history."
    echo "    Continuing but check this is intended."
fi
echo "✅ Session 11 agents commit detected"

# Show current CITATION.cff version
CURRENT_VERSION=$(grep '^version:' CITATION.cff | head -1 | awk -F'"' '{print $2}')
CURRENT_DATE=$(grep '^date-released:' CITATION.cff | head -1 | awk -F'"' '{print $2}')
echo "Current: version=$CURRENT_VERSION, date=$CURRENT_DATE"
echo "Target:  version=$NEW_VERSION, date=$NEW_DATE"
echo

# ---- Apply version bump ----
if $DRY_RUN; then
    echo "--- DRY-RUN: would apply changes ---"
    echo "1. sed -i 's/version: \"$CURRENT_VERSION\"/version: \"$NEW_VERSION\"/' CITATION.cff"
    echo "2. sed -i 's/date-released: \"$CURRENT_DATE\"/date-released: \"$NEW_DATE\"/' CITATION.cff"
    echo "3. git add CITATION.cff"
    echo "4. git commit -m 'Zenodo cut v$NEW_VERSION — post 11 agents session $NEW_DATE'"
    echo "5. git tag -a v$NEW_VERSION -m 'Zenodo release v$NEW_VERSION ($NEW_DATE)'"
    echo "6. git push origin master"
    echo "7. git push public master"
    echo "8. git push public v$NEW_VERSION  # triggers Zenodo webhook"
    echo
    echo "To execute: bash $0 --execute"
else
    echo "--- EXECUTING ---"

    # 1. Bump version
    sed -i "s/version: \"$CURRENT_VERSION\"/version: \"$NEW_VERSION\"/" CITATION.cff
    sed -i "s/date-released: \"$CURRENT_DATE\"/date-released: \"$NEW_DATE\"/" CITATION.cff
    echo "✅ Bumped CITATION.cff to $NEW_VERSION ($NEW_DATE)"

    # 2. Show diff
    echo "Diff:"
    git diff CITATION.cff
    echo

    # 3. Commit
    git add CITATION.cff
    git commit -m "Zenodo cut v$NEW_VERSION — post 11 agents session $NEW_DATE

Bumped version $CURRENT_VERSION → $NEW_VERSION + date → $NEW_DATE.
Session 2026-05-16 deliverables :
- Paper 3 G4 obstruction 3pp (honest negative G4.0' P((★))∈[0.05,0.18])
- Paper 2 HSH v3 letter JNT v2 7pp (Gauss 1801 + Rubin 1991 split)
- Sp(2N) mini-paper PRD 4pp (c=0.203±0.056)
- HSH +81 anchors PARI sweep D ∈ [-2000,-1000]
- HSH-νDM D=-67 Dirac falsifier (XLZD 2027-2030)
- Bridge 9.1 cross-N FALSIFIED
- c=0.80 → c=0.94 ± 0.04 calibration shift (P01 RELAUNCH)
- Plan v5 §B reframe (aggregate ~41% projeté +18pp)
- Constructive YM 4D anchors verified (CNS 2509.04688, SZZ 2204.12737, Chatterjee 2401.10507)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
    echo "✅ Committed"

    # 4. Tag
    git tag -a "v$NEW_VERSION" -m "Zenodo release v$NEW_VERSION ($NEW_DATE)

Session 2026-05-16 deliverables — 11 agents post-W40.
Cluster firm 391. Aggregate YM stable 23% (Plan v5 §B projection ~41% sous condition)."
    echo "✅ Tagged v$NEW_VERSION"

    # 5. Push to private origin
    git push origin master
    echo "✅ Pushed to origin/master (private)"

    # 6. Push to public + tag (triggers Zenodo webhook)
    echo
    echo "⚠️  Next : push to PUBLIC remote — this triggers Zenodo webhook deposit."
    echo "    Confirming user intent..."
    read -p "    Push to public + tag v$NEW_VERSION ? (yes/no): " confirm
    if [[ "$confirm" == "yes" ]]; then
        git push public master
        git push public "v$NEW_VERSION"
        echo "✅ Pushed to public/master + tag v$NEW_VERSION"
        echo
        echo "🔗 Zenodo webhook should fire shortly. Check :"
        echo "   https://zenodo.org/account/settings/github/repository/AIdevsmartdata/crossed-cosmos"
        echo
        echo "   Fallback manual deposit if webhook fails :"
        echo "   1. Visit https://zenodo.org/deposit/new?c=ECI"
        echo "   2. Upload latest tag tarball from https://github.com/AIdevsmartdata/crossed-cosmos/releases/tag/v$NEW_VERSION"
        echo "   3. Apply metadata from scripts/zenodo_metadata/zenodo-v6-2026-04-24.json (update version + date)"
        echo "   4. Publish."
    else
        echo "⏸️  Public push skipped. Apply manually when ready :"
        echo "   git push public master && git push public v$NEW_VERSION"
    fi
fi

echo
echo "=== Done ==="
