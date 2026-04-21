# HAL deposit via SWORD API

Programmatic deposit of the ECI v4 framework paper on [HAL](https://hal.science), the French CNRS open archive. This serves as a **second timestamp** (CNRS) complementing the Zenodo DOI (CERN).

## Prerequisites

1. **HAL account** — create one at https://hal.science/user/create (email = `kevin.remondiere@gmail.com`, affiliation = "Chercheur indépendant / Independent Researcher"). Link your ORCID in the account settings afterwards.
2. **Compiled PDF** — `paper/eci.pdf` must exist. Run `cd paper && latexmk -pdf eci.tex` first.
3. **Local tools** — `curl` and `zip` (standard on Ubuntu).

## Two-step deposit (preprod → prod)

HAL provides a preprod instance that accepts the same SWORD API but does NOT publish. Use it to validate the TEI + PDF bundle before real deposit.

```bash
cd submission/hal

# Step 1 — preprod dry-run (default)
./deposit.sh
#   prompts for HAL login + password (password not echoed, not logged)
#   expected: HTTP 201, response.xml contains <deposit_receipt>

# Step 2 — prod, once preprod is clean
SWORD_URL=https://api.archives-ouvertes.fr/sword/hal ./deposit.sh
```

## What happens next

- HAL returns HTTP 201 immediately if the bundle is well-formed.
- The deposit enters **moderation queue** (humans at HAL CCSD curate every first-time deposit, ~1–5 business days).
- You'll receive an email when the deposit is accepted; the record gets a permanent `hal-XXXXXXXX` ID and a public URL `https://hal.science/hal-XXXXXXXX`.
- If rejected, the email explains what to fix in the TEI. Iterate on `eci.tei.xml` and re-run `deposit.sh`.

## Files

- `eci.tei.xml` — TEI-HAL metadata (title, author, ORCID, abstract, keywords, domain `phys.astr.co` + `phys.grqc`, CC-BY licence, Zenodo DOI cross-ref).
- `deposit.sh` — curl wrapper, credential-safe (netrc tempfile, `read -s` for password).
- `response.xml` — created by `deposit.sh` after each run; contains the server's SWORD deposit receipt.
- `eci-hal-bundle.zip` — ephemeral, rebuilt on every run.

## Security

- Password is read with `read -s` (not echoed, not saved to bash history).
- Password is written to a `mktemp` netrc file with mode 600, deleted on script exit via `trap`.
- The `--user user:pass` form is avoided because it exposes the password in `ps` output.
- No credentials are ever written to any repo file or committed to git.

## Moderation notes for first-time HAL depositors

HAL curators typically check:
- Author affiliation — `Chercheur indépendant` is accepted. No institutional affiliation required.
- DOI cross-reference — Zenodo DOI in TEI is fine, it helps the moderator verify novelty.
- Domain classification — `phys.astr.co` (astro-ph.CO) + `phys.grqc` (gr-qc) is accurate for this paper.
- File quality — compiled, non-password-protected PDF, ≤50 MB. `paper/eci.pdf` is 472 KB, well within limits.
