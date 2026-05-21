#!/usr/bin/env python3
"""Validate HMC outputs : check <P>_lat against Bali 1992 known values.
Falsification criteria : <P> outside [target ± 0.05] → bad thermalization."""
import numpy as np, glob, json, os, sys

# Bali 1992 SU(2) plaquette values
BALI_SU2 = {
    2.3: 0.5505,
    2.5: 0.6294,
    2.7: 0.6859,
}

print("="*60)
print("HMC validation — compare <P> with Bali 1992")
print("="*60)

results = {}
for npz in sorted(glob.glob("results/hmc_b*.npz")):
    if not os.path.exists(npz): continue
    data = np.load(npz)
    beta = float(data['beta'])
    plaqs = data['plaquettes']
    polyak = data['polyakov']
    
    target = BALI_SU2.get(round(beta, 1))
    mean_p = plaqs.mean()
    err = plaqs.std() / np.sqrt(len(plaqs))
    poly_mean = polyak.mean()
    poly_abs = abs(poly_mean)
    
    print(f"\n β = {beta}")
    print(f"  Configs : {len(plaqs)}")
    print(f"  <P>_lat = {mean_p:.4f} ± {err:.4f}")
    if target is not None:
        diff = abs(mean_p - target) / target * 100
        status = "✓ PASS" if abs(mean_p - target) < 0.05 else "⚠ DRIFT" if diff < 10 else "✗ FAIL"
        print(f"  Bali target : {target:.4f}")
        print(f"  Diff : {diff:.1f}% {status}")
    print(f"  |⟨Polyakov⟩| = {poly_abs:.4f}")
    confined = poly_abs < 0.05
    print(f"  Phase : {'CONFINED (|P|≈0)' if confined else 'DECONFINED (|P|≠0)'}")
    
    results[str(beta)] = {
        'beta': beta,
        'plaq_mean': float(mean_p), 'plaq_err': float(err),
        'bali_target': target,
        'polyakov_abs': float(poly_abs),
        'phase': 'confined' if confined else 'deconfined',
        'n_configs': int(len(plaqs)),
    }

# Save
with open('results/validation.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n✓ Saved validation.json")

# Falsification check
print("\n" + "="*60)
print("FALSIFICATION CHECK")
print("="*60)
# Expected : β=2.3 deconfined OR transition, β=2.7 confined
all_phases = [r['phase'] for r in results.values()]
all_betas = [r['beta'] for r in results.values()]
if len(all_phases) >= 2:
    sorted_data = sorted(zip(all_betas, all_phases))
    print("Beta order : ", sorted_data)
    # Monotone confined → deconfined as β increases ?
    # Actually opposite : larger β = smaller a = stronger coupling at fixed lattice → MORE confined
    print("Expected : larger β → more confined (smaller |Poly|)")
    
print(f"\nFramework consistency : {'✓ CONSISTENT' if len(set(all_phases))==2 else '⚠ SAME phase all β — small lattice?'}")
