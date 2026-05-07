#!/usr/bin/env python3
"""
M177 step 2 — Reconcile NPP20 Table 7 (symmetric basis) ρ_3̂(S) with the
modular form basis of Y_3̂^(3) given in eq (3.14).

The Y_3̂^(3) basis given in NPP20 (eq 3.14) is:
    Y_3̂^(3) = (
        ε^5 θ + ε θ^5 ,
        (1/(2√2)) (5 ε² θ^4 - ε^6) ,
        (1/(2√2)) (θ^6 - 5 ε^4 θ²)
    )

Let's first verify Y_3̂^(3) actually transforms under ρ_3̂(S) of Table 7 using the
S-action on θ, ε:
    θ -- S --> √(-iτ) (θ + ε)/√2
    ε -- S --> √(-iτ) (θ - ε)/√2
(eq 3.8 NPP20)

Then check Y(Sτ) = (-τ)^3 ρ_3̂(S) Y(τ) at a generic τ.
"""

import mpmath as mp
mp.mp.dps = 30

import numpy as np


def theta_eps(tau, N=200):
    q4 = mp.exp(1j * mp.pi * tau / 2)
    th = mp.mpc(1)
    ep = mp.mpc(0)
    for k in range(1, N + 1):
        th += 2 * q4 ** ((2 * k) ** 2)
        ep += 2 * q4 ** ((2 * k - 1) ** 2)
    return th, ep


def Y3_hat_w3(tau):
    th, ep = theta_eps(tau)
    pre = 1 / (2 * mp.sqrt(2))
    return mp.matrix([[pre * (ep ** 5 * th + ep * th ** 5)],
                      [pre * (5 * ep ** 2 * th ** 4 - ep ** 6)],
                      [pre * (th ** 6 - 5 * ep ** 4 * th ** 2)]])


# Table 7 ρ_3̂(S) (in the working symmetric basis)
sq2 = mp.sqrt(2)
M_block = mp.matrix([[0, sq2, sq2],
                     [sq2, -1, 1],
                     [sq2, 1, -1]])
rho_3hat_S = (-mp.mpc(0, 1)/2) * M_block

print("=" * 72)
print("Verify NPP20 Y_3̂^(3) lives in Table 7 working basis")
print("=" * 72)

# Test transformation at several taus
for r_str, i_str in [("0.1", "1.3"), ("0.0", "2.0"), ("0.2", "1.7")]:
    tau = mp.mpc(r_str, i_str)
    Y_tau = Y3_hat_w3(tau)
    Y_Stau = Y3_hat_w3(-1/tau)
    # Predicted: Y(Sτ) = (-τ)^3 ρ(S) Y(τ)
    Y_pred = ((-tau) ** 3) * (rho_3hat_S * Y_tau)
    diffs = [abs(Y_Stau[i] - Y_pred[i]) for i in range(3)]
    print(f"\nτ = {tau}:")
    print(f"  Y(Sτ)        = {[Y_Stau[i] for i in range(3)]}")
    print(f"  (-τ)³ρ(S)Y(τ) = {[Y_pred[i] for i in range(3)]}")
    print(f"  max diff = {max(diffs)}")


# Now the question: is the Y_3̂^(3) prefactor in eq (3.14) actually as I wrote?
# Looking at eq (3.14) again VERBATIM:
#    Y_3̂^(3) = (
#       ε^5 θ + ε θ^5 ,            <-- NO (1/(2√2)) prefactor!
#       (1/(2√2)) (5 ε² θ^4 - ε^6) ,
#       (1/(2√2)) (θ^6 - 5 ε^4 θ²)
#    )
# I was applying (1/(2√2)) to ALL three components, but eq (3.14) only puts it on
# the lower two!
# Let me re-read: page 9 says
#   Y_3̂^(3) = (
#       ε^5 θ + ε θ^5,
#       (1/(2√2))(5 ε² θ^4 - ε^6),
#       (1/(2√2))(θ^6 - 5 ε^4 θ²)
#   )
# Yes — first component has NO prefactor. Let me fix this and retest.

print("\n" + "=" * 72)
print("CORRECTED Y_3̂^(3) per NPP20 eq (3.14)")
print("=" * 72)

def Y3_hat_w3_correct(tau):
    th, ep = theta_eps(tau)
    return mp.matrix([[ep ** 5 * th + ep * th ** 5],
                      [(1/(2*mp.sqrt(2))) * (5 * ep ** 2 * th ** 4 - ep ** 6)],
                      [(1/(2*mp.sqrt(2))) * (th ** 6 - 5 * ep ** 4 * th ** 2)]])

for r_str, i_str in [("0.1", "1.3"), ("0.0", "2.0"), ("0.2", "1.7")]:
    tau = mp.mpc(r_str, i_str)
    Y_tau = Y3_hat_w3_correct(tau)
    Y_Stau = Y3_hat_w3_correct(-1/tau)
    Y_pred = ((-tau) ** 3) * (rho_3hat_S * Y_tau)
    diffs = [abs(Y_Stau[i] - Y_pred[i]) for i in range(3)]
    print(f"\nτ = {tau}:")
    print(f"  max |Y(Sτ) - (-τ)³ρ(S)Y(τ)| = {max(diffs)}")

# Actually hold on, looking at the PDF page 9 image more carefully:
# Y_3̂^(3) = (
#   ε^5 θ + ε θ^5
#   (1/(2√2)) (5 ε² θ^4 - ε^6)
#   (1/(2√2)) (θ^6 - 5 ε^4 θ²)
# )
# It says all three with the same outer  -- there's no overall 1/(2√2) factor!
# Let me re-check the image once more at page 9.

# Looking again at page 9: there IS NO common 1/(2√2) factor.  Component 1 is just
# "ε^5θ + εθ^5" (no prefactor); components 2 and 3 each have their own (1/(2√2)).
# So the corrected version is right.

# Final test: does Y_3̂^(3)(i) lie in -i eigenspace?
tau_i = mp.mpc(0, 1)
Y_at_i = Y3_hat_w3_correct(tau_i)
print(f"\nY_3̂^(3)(i) [corrected per (3.14)] = ")
for r in range(3):
    print(f"  [{r}] = {Y_at_i[r]}")

Y_vec = np.array([complex(Y_at_i[r]) for r in range(3)])
print(f"\nAs np vector: {Y_vec}")

rho_np = np.array([[complex(rho_3hat_S[i, j]) for j in range(3)] for i in range(3)])
eigvals, eigvecs = np.linalg.eig(rho_np)
print(f"\nEigvals of ρ_3̂(S): {eigvals}")
mask_minus_i = [k for k in range(3) if abs(eigvals[k] - (-1j)) < 1e-6]
print(f"-i eigenspace dim: {len(mask_minus_i)}")
V = eigvecs[:, mask_minus_i]
print(f"-i eigenvector(s):")
for k in range(V.shape[1]):
    v = V[:, k] / np.linalg.norm(V[:, k])
    print(f"  v_{k} = {v}")

P = V @ V.conj().T  # since v is normalized, P_minus_i = vv†
proj = P @ Y_vec
residual = Y_vec - proj
print(f"\n|Y - P_(-i) Y| / |Y| = {np.linalg.norm(residual)/np.linalg.norm(Y_vec):.2e}")

# Direct check: ρ(S) Y(i) should = -i Y(i)
SY = rho_np @ Y_vec
target = -1j * Y_vec
diff = SY - target
print(f"\n|ρ(S) Y(i) - (-i) Y(i)| = {np.linalg.norm(diff):.2e}")
print(f"  SY  = {SY}")
print(f"  -iY = {target}")
