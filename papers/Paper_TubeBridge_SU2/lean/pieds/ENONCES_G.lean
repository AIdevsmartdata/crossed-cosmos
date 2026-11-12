/-- Edges of the discrete torus `(ℤ/m) × (ℤ/n)`: `Sum.inl (i,j)` is the horizontal edge from `(i,j)` to `(i+1,j)`,
`Sum.inr (i,j)` the vertical edge from `(i,j)` to `(i,j+1)`; indices are cyclic. -/
abbrev TorusEdge (m n : ℕ) := (Fin m × Fin n) ⊕ (Fin m × Fin n)

/-- The four boundary edges of the plaquette with lower-left corner `p = (i,j)`: bottom `H(i,j)`, top `H(i,j+1)`,
left `V(i,j)`, right `V(i+1,j)`; the cyclic successor is `finRotate`. -/
def torusBd {m n : ℕ} (p : Fin m × Fin n) : Finset (TorusEdge m n) :=
  {Sum.inl (p.1, p.2), Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2), Sum.inr (finRotate m p.1, p.2)}

/-- G3. For periods at least two the four boundary edges are distinct. -/
theorem torus_plaq_explicit {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n)
    (σ : TorusEdge m n → ℤˣ) (p : Fin m × Fin n) :
    plaq torusBd σ p =
      σ (Sum.inl (p.1, p.2)) * σ (Sum.inl (p.1, finRotate n p.2)) *
        σ (Sum.inr (p.1, p.2)) * σ (Sum.inr (finRotate m p.1, p.2)) := by
  PROOF_G3

/-- G1. Parity: on the torus the product of all plaquette signs is one. -/
theorem torus_plaq_parity {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (σ : TorusEdge m n → ℤˣ) :
    ∏ p : Fin m × Fin n, plaq torusBd σ p = 1 := by
  PROOF_G1

/-- G2. Image: every assignment of plaquette signs with product one is realised by edge signs. -/
theorem torus_plaq_image {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ℤˣ)
    (ht : ∏ p, t p = 1) : ∃ σ : TorusEdge m n → ℤˣ, ∀ p, plaq torusBd σ p = t p := by
  PROOF_G2
