#!/usr/bin/env python3
"""ECI R10 prime Seiberg‑Witten curve at u=0.

Compute pure SU(2) SW curve y²=4x³-(u²/12-1)·x-(-u(u²-9)/216) at u=0,
i.e. y²=4x³+x, using PARI/GP.  Extract period ratio τ and j‑invariant.
Output JSON.
"""
import json, sys, logging, time, subprocess
from pathlib import Path
import mpmath as mp

CACHE_DIR = Path.home() / '.cache' / 'eci_r10p_sw_u0'

def compute_sw_data(dps=200):
    """Return dict with keys 'tau', 'j_invariant'."""
    # Use PARI/GP to compute tau and j‑invariant
    # Curve in short Weierstrass form: y² = x³ + (1/4)x
    # a4 = 1/4, a6 = 0
    script = (
        f"default(realprecision,{dps});"
        "E=ellinit([0,0,0,1/4,0]);"
        "w=ellperiods(E);"
        "tau=w[2]/w[1];"
        "print(tau);"
        "print(E.j);"
    )
    try:
        proc = subprocess.run(
            ["gp", "-q", "-e", script],
            capture_output=True, text=True, timeout=60
        )
    except FileNotFoundError:
        raise RuntimeError("PARI/GP (gp) not found on PATH. Cannot compute period ratio.")
    if proc.returncode != 0:
        raise RuntimeError(f"PARI/GP failed:\nstdout:{proc.stdout}\nstderr:{proc.stderr}")
    lines = [l.strip() for l in proc.stdout.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        raise RuntimeError("Insufficient output from PARI/GP")
    tau_str = lines[0]
    j_str = lines[1]
    # convert tau_str to mp.mpc (gp formats like "0.123 + 1.456*I")
    tau_c = complex(tau_str.replace('*I', 'j').replace('I', 'j'))
    tau_mp = mp.mpc(tau_c.real, tau_c.imag)
    # j‑invariant is real
    j_val = mp.mpf(complex(j_str.replace('*I','j').replace('I','j')).real)
    return {"tau": str(tau_mp), "j_invariant": str(j_val)}

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    start = time.monotonic()
    result = {
        "test": "eci_r10p_sw_u0",
        "status": "FAIL",
        "tau_value": "",
        "j_invariant": "",
        "comment": ""
    }
    try:
        sw_data = compute_sw_data(dps=200)
        tau_str = sw_data["tau"]
        j_str = sw_data["j_invariant"]

        # parse tau for comparison
        parts = tau_str.replace(" ", "").split("+")
        if len(parts) == 2:
            re = mp.mpf(parts[0])
            im_str = parts[1].replace("*I","").replace("I","")
            im = mp.mpf(im_str)
        else:
            # handle negative imag
            parts = tau_str.replace(" ", "").split("-")
            re = mp.mpf(parts[0])
            im_str = "-" + parts[1].replace("*I","").replace("I","")
            im = mp.mpf(im_str)
        tau_val = re + 1j * im
        diff = abs(tau_val - 1j)
        if diff < mp.mpf("1e-10"):
            result["status"] = "PASS"
            result["comment"] = "τ ≡ i (mod SL(2,Z))"
        else:
            result["status"] = "FAIL"
            result["comment"] = f"τ = {tau_str} differs from i by {diff}"

        result["tau_value"] = tau_str
        result["j_invariant"] = j_str

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
