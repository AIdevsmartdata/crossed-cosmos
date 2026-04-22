#!/usr/bin/env python3
"""Run all D1-D6 and N1-N5; capture logs and timing."""
import subprocess, time, os, sys, json

REPO = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("PIPELINE_PYTHON", sys.executable)

JOBS = [
    ("derivations", ["D1-kg-nmc.py","D2-stress-nmc.py","D3-noghost.py",
                     "D4-wa-w0-nmc.py","D5-persistent-homology.py","D6-deltaNeff-kk.py"]),
    ("numerics",    ["N1-w0wa-scan.py","N2-kk-neff.py","N3-ppn-gamma.py",
                     "N4-Gdot-G.py","N5-ph-fnl-sensitivity.py"]),
]

results = []
for subdir, files in JOBS:
    d = os.path.join(REPO, subdir)
    os.makedirs(os.path.join(d, "_results"), exist_ok=True)
    os.makedirs(os.path.join(d, "figures"), exist_ok=True)
    for f in files:
        path = os.path.join(d, f)
        logp = os.path.join(d, "_results", f.replace(".py", ".log"))
        t0 = time.time()
        try:
            p = subprocess.run([PY, path], cwd=d, capture_output=True, text=True, timeout=900)
            out = p.stdout + "\n--- STDERR ---\n" + p.stderr
            rc = p.returncode
        except subprocess.TimeoutExpired as e:
            out = f"TIMEOUT after 900s\n{e}"
            rc = -1
        except Exception as e:
            out = f"EXCEPTION: {e}"
            rc = -2
        dt = time.time() - t0
        with open(logp, "w") as fh:
            fh.write(out)
        status = "PASS" if rc == 0 else f"FAIL(rc={rc})"
        print(f"{f:35s} {status:15s} {dt:7.2f}s")
        results.append((subdir, f, rc, dt))

with open(os.path.join(REPO, "_run_all_results.json"), "w") as fh:
    json.dump(results, fh, indent=2)
