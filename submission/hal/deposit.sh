#!/usr/bin/env bash
# HAL SWORD v1 deposit for ECI v4 framework paper.
#
# Prerequisites:
#   1. You have an account on https://hal.science (created at /user/create)
#   2. The compiled PDF is at ../../paper/eci.pdf
#   3. curl, zip installed
#
# Usage:
#     cd submission/hal
#     ./deposit.sh                 # prompts for HAL login + password interactively
#     ./deposit.sh LOGIN            # prompts only for password
#
# Security:
#   - Password is read with `read -s` (not echoed, not in shell history).
#   - The curl invocation uses --user which can show in `ps` briefly;
#     we mitigate by using --netrc-file <(printf ...) to keep creds off argv.
#   - The TEST endpoint (preprod) is used by default. Flip SWORD_URL to prod
#     only when you're confident in the TEI + PDF.
#
# Endpoints:
#   - Preprod:  https://api-preprod.archives-ouvertes.fr/sword/hal
#   - Prod:     https://api.archives-ouvertes.fr/sword/hal
#
set -euo pipefail

SWORD_URL="${SWORD_URL:-https://api-preprod.archives-ouvertes.fr/sword/hal}"
TEI="eci.xml"
PDF="../../paper/eci.pdf"
BUNDLE="eci-hal-bundle.zip"

if [[ ! -f "$TEI" ]]; then
    echo "ERROR: missing $TEI" >&2; exit 1
fi
if [[ ! -f "$PDF" ]]; then
    echo "ERROR: missing $PDF (compile paper/eci.tex first)" >&2; exit 1
fi

LOGIN="${1:-}"
if [[ -z "$LOGIN" ]]; then
    read -rp "HAL login: " LOGIN
fi
read -rsp "HAL password: " PASS; echo

# Build SWORD bundle: a zip containing the TEI (mets.xml-style) + PDF payload.
rm -f "$BUNDLE"
# HAL SWORD expects the TEI file to be named as the metadata and the PDF as the file attachment.
cp "$PDF" ./eci.pdf
zip -q "$BUNDLE" "$TEI" eci.pdf
rm -f ./eci.pdf

echo "Depositing to: $SWORD_URL"
echo "Bundle: $BUNDLE ($(stat -c %s "$BUNDLE") bytes)"
echo

# Use a temporary netrc to keep creds off argv.
NETRC=$(mktemp)
trap 'rm -f "$NETRC"' EXIT
HOST=$(echo "$SWORD_URL" | awk -F/ '{print $3}')
printf 'machine %s login %s password %s\n' "$HOST" "$LOGIN" "$PASS" > "$NETRC"
chmod 600 "$NETRC"

curl --netrc-file "$NETRC" \
    -H "Content-Type: application/zip" \
    -H "Content-Disposition: attachment; filename=$TEI" \
    -H "Packaging: http://purl.org/net/sword-types/AOfr" \
    -H "X-Packaging: http://purl.org/net/sword-types/AOfr" \
    -H "X-Allow-Completion: false" \
    --data-binary "@$BUNDLE" \
    "$SWORD_URL" \
    -o response.xml -w "HTTP %{http_code}\n"

echo
echo "Response saved to: response.xml"
echo
if grep -q '<error' response.xml 2>/dev/null; then
    echo "DEPOSIT REJECTED — inspect response.xml"
    exit 2
fi
echo "If the HTTP code is 201, the deposit is accepted and pending HAL moderation (1–5 days)."
echo "Switch SWORD_URL to the prod endpoint once the preprod test is clean:"
echo "    SWORD_URL=https://api.archives-ouvertes.fr/sword/hal ./deposit.sh $LOGIN"
