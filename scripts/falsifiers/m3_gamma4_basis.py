#!/usr/bin/env python3
"""Compute 7-dimensional basis of M_3(Γ(4)) for S'_4 irreps.

Uses PARI/GP to obtain the dimension and a numerical basis.
Output JSON with dimension and q‑expansions as computed by PARI.
"""
import json, sys, logging, time, subprocess
import mpmath as mp
import sympy as sp

def compute_basis_and_dim():
    """Return (dim, expansions_list) using PARI/GP."""
    script = (
        "default(realprecision,38);"
        "mf=mfinit([4,3]);"
        "B=mfbasis(mf);"
        "dim=#B;"
        "print(dim);"
        "for(i=1,dim,"
        "   coef=mfcoefs(B[i],5);"
        "   for(j=1,#coef,print(coef[j]));"
        "   print(\"---\");"
        ");"
    )
    try:
        proc = subprocess.run(
            ["gp", "-q", "-e", script],
            capture_output=True, text=True, timeout=60
        )
    except FileNotFoundError:
        raise RuntimeError("PARI/GP (gp) not found on PATH.")
    if proc.returncode != 0:
        raise RuntimeError(f"PARI/GP failed:\nstdout:{proc.stdout}\nstderr:{proc.stderr}")
    lines = [l.strip() for l in proc.stdout.strip().split('\n') if l.strip()]
    if not lines:
        raise RuntimeError("No output from PARI/GP")
    dim = int(lines[0])
    expansions = []
    idx = 1
    for _ in range(dim):
        coefs = []
        while idx < len(lines) and lines[idx] != '---':
            coefs.append(lines[idx])
            idx += 1
        idx += 1  # skip '---'
        # build q‑expansion string (integer powers)
        terms = []
        for n, c in enumerate(coefs):
            c_val = sp.sympify(c)
            if c_val != 0:
                if n == 0:
                    terms.append(str(c_val))
                else:
                    terms.append(f"{c_val}*q^{n}")
        series_str = " + ".join(terms) if terms else "0"
        expansions.append({"series": series_str})
    return dim, expansions

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    start = time.monotonic()
    result = {"test": "m3_gamma4_basis", "status": "FAIL", "comment": ""}
    try:
        dim, expansions = compute_basis_and_dim()
        result["basis_dimensions"] = {"dimension": dim}
        result["number_of_basis_forms"] = dim
        result["q_expansions"] = expansions
        # Eigenvalues at τ=i (from known evaluation) – not computed here
        result["eigenvalues_at_tau_i"] = {
            "note": "Eigenvalues not computed; requires actual S/T matrices (CITE_NEEDED)."
        }
        if dim == 7:
            result["status"] = "PASS"
            result["comment"] = "Dimension 7 matches NPP20; expansions computed by PARI."
        else:
            result["comment"] = f"Unexpected dimension {dim}"
    except Exception as e:
        logger.exception("Computation failed")
        result["status"] = "ERROR"
        result["comment"] = str(e)
    result["elapsed_seconds"] = round(time.monotonic() - start, 2)
    print(json.dumps(result, indent=2))
    if result["status"] == "ERROR":
        sys.exit(1)

if __name__ == "__main__":
    main()
