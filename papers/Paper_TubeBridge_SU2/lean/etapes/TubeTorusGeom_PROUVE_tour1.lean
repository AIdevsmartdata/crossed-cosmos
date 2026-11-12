open MeasureTheory Finset

namespace TubeArea

/-- A cyclic successor has no fixed point when the period is at least two. -/
lemma torusGeom_rotate_ne {k : ℕ} (hk : 2 ≤ k) (i : Fin k) :
    finRotate k i ≠ i := by
  obtain ⟨l, rfl⟩ : ∃ l, k = l + 1 := ⟨k - 1, by omega⟩
  intro h
  have hv := congrArg Fin.val h
  rw [coe_finRotate] at hv
  split_ifs at hv with hi
  · have hi' := congrArg Fin.val hi
    change i.val = l at hi'
    omega
  · omega

/-- Product of the entries whose natural index is strictly smaller than `r`. -/
def torusGeom_prefix {k : ℕ} (g : Fin k → ℤˣ) (r : ℕ) : ℤˣ :=
  ∏ j ∈ Finset.univ.filter (fun j : Fin k => j.val < r), g j

lemma torusGeom_prefix_zero {k : ℕ} (g : Fin k → ℤˣ) :
    torusGeom_prefix g 0 = 1 := by
  simp [torusGeom_prefix]

lemma torusGeom_prefix_total {k : ℕ} (g : Fin k → ℤˣ) :
    torusGeom_prefix g k = ∏ j, g j := by
  have hs : Finset.univ.filter (fun j : Fin k => j.val < k) = Finset.univ := by
    ext j
    simp [j.isLt]
  unfold torusGeom_prefix
  rw [hs]

lemma torusGeom_prefix_succ {k : ℕ} (g : Fin k → ℤˣ) (i : Fin k) :
    torusGeom_prefix g (i.val + 1) = torusGeom_prefix g i.val * g i := by
  have hs : Finset.univ.filter (fun j : Fin k => j.val < i.val + 1) =
      insert i (Finset.univ.filter (fun j : Fin k => j.val < i.val)) := by
    ext j
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert]
    constructor
    · intro hj
      by_cases he : j = i
      · exact Or.inl he
      · right
        have hne : j.val ≠ i.val := by
          intro h
          exact he (Fin.ext h)
        omega
    · intro hj
      rcases hj with rfl | hj
      · omega
      · omega
  have hi : i ∉ Finset.univ.filter (fun j : Fin k => j.val < i.val) := by
    simp
  unfold torusGeom_prefix
  rw [hs, Finset.prod_insert hi]
  exact mul_comm _ _

/-- Prefix products solve the cyclic sign equation when the total is one. -/
lemma torusGeom_cycle {k : ℕ} (g : Fin (k + 1) → ℤˣ)
    (hg : ∏ j, g j = 1) (i : Fin (k + 1)) :
    torusGeom_prefix g i.val *
        torusGeom_prefix g (finRotate (k + 1) i).val = g i := by
  by_cases hi : i = Fin.last k
  · subst i
    rw [finRotate_last]
    change torusGeom_prefix g k * torusGeom_prefix g 0 = g (Fin.last k)
    rw [torusGeom_prefix_zero, mul_one]
    have hs : 1 = torusGeom_prefix g k * g (Fin.last k) := by
      calc
        1 = torusGeom_prefix g (k + 1) := by
          rw [torusGeom_prefix_total, hg]
        _ = torusGeom_prefix g k * g (Fin.last k) :=
          torusGeom_prefix_succ g (Fin.last k)
    calc
      torusGeom_prefix g k =
          (torusGeom_prefix g k * g (Fin.last k)) * g (Fin.last k) := by
        rw [mul_assoc, grid_sign_square, mul_one]
      _ = g (Fin.last k) := by rw [← hs, one_mul]
  · rw [coe_finRotate_of_ne_last hi, torusGeom_prefix_succ]
    rw [← mul_assoc, grid_sign_square, one_mul]

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
  classical
  have hi := torusGeom_rotate_ne hm p.1
  have hj := torusGeom_rotate_ne hn p.2
  have hA : (Sum.inl (p.1, p.2) : TorusEdge m n) ∉
      ({Sum.inl (p.1, finRotate n p.2), Sum.inr (p.1, p.2),
        Sum.inr (finRotate m p.1, p.2)} : Finset (TorusEdge m n)) := by
    intro he
    simp only [Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he | he
    · exact hj (congrArg Prod.snd (Sum.inl.inj he)).symm
    · cases he
    · cases he
  have hB : (Sum.inl (p.1, finRotate n p.2) : TorusEdge m n) ∉
      ({Sum.inr (p.1, p.2), Sum.inr (finRotate m p.1, p.2)} :
        Finset (TorusEdge m n)) := by
    intro he
    simp only [Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he <;> cases he
  have hC : (Sum.inr (p.1, p.2) : TorusEdge m n) ∉
      ({Sum.inr (finRotate m p.1, p.2)} : Finset (TorusEdge m n)) := by
    intro he
    exact hi (congrArg Prod.fst (Sum.inr.inj (Finset.mem_singleton.mp he))).symm
  unfold plaq torusBd
  rw [Finset.prod_insert hA, Finset.prod_insert hB, Finset.prod_insert hC,
    Finset.prod_singleton]
  simp only [mul_assoc]

/-- G1. Parity: on the torus the product of all plaquette signs is one. -/
theorem torus_plaq_parity {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (σ : TorusEdge m n → ℤˣ) :
    ∏ p : Fin m × Fin n, plaq torusBd σ p = 1 := by
  classical
  have hH : (∏ p : Fin m × Fin n, σ (Sum.inl (p.1, finRotate n p.2))) =
      ∏ p : Fin m × Fin n, σ (Sum.inl p) := by
    exact Equiv.prod_comp (Equiv.prodCongr (Equiv.refl (Fin m)) (finRotate n))
      (fun p : Fin m × Fin n => σ (Sum.inl p))
  have hV : (∏ p : Fin m × Fin n, σ (Sum.inr (finRotate m p.1, p.2))) =
      ∏ p : Fin m × Fin n, σ (Sum.inr p) := by
    exact Equiv.prod_comp (Equiv.prodCongr (finRotate m) (Equiv.refl (Fin n)))
      (fun p : Fin m × Fin n => σ (Sum.inr p))
  simp only [torus_plaq_explicit hm hn, Finset.prod_mul_distrib]
  rw [hH, hV]
  simp only [grid_sign_square, one_mul]

/-- G2. Image: every assignment of plaquette signs with product one is realised by edge signs. -/
theorem torus_plaq_image {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ℤˣ)
    (ht : ∏ p, t p = 1) : ∃ σ : TorusEdge m n → ℤˣ, ∀ p, plaq torusBd σ p = t p := by
  classical
  obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  obtain ⟨n', rfl⟩ : ∃ n', n = n' + 1 := ⟨n - 1, by omega⟩
  let torusGeom_c : Fin (m' + 1) → ℤˣ :=
    fun i => ∏ j : Fin (n' + 1), t (i, j)
  have hc : (∏ i, torusGeom_c i) = 1 := by
    dsimp only [torusGeom_c]
    exact (Fintype.prod_prod_type t).symm.trans ht
  let torusGeom_d : Fin (m' + 1) → Fin (n' + 1) → ℤˣ :=
    fun i j => t (i, j) * (if j = 0 then torusGeom_c i else 1)
  have hd (i : Fin (m' + 1)) : (∏ j, torusGeom_d i j) = 1 := by
    dsimp only [torusGeom_d]
    rw [Finset.prod_mul_distrib]
    have hcorr : (∏ j : Fin (n' + 1),
        if j = 0 then torusGeom_c i else (1 : ℤˣ)) = torusGeom_c i := by
      simpa only [Finset.mem_univ, if_true] using
        (Finset.prod_ite_eq' (Finset.univ : Finset (Fin (n' + 1)))
          (0 : Fin (n' + 1)) (fun _ => torusGeom_c i))
    rw [hcorr]
    exact grid_sign_square (torusGeom_c i)
  let torusGeom_v : Fin (m' + 1) → Fin (n' + 1) → ℤˣ :=
    fun i j => if j = 0 then torusGeom_prefix torusGeom_c i.val else 1
  let torusGeom_h : Fin (m' + 1) → Fin (n' + 1) → ℤˣ :=
    fun i j => torusGeom_prefix (torusGeom_d i) j.val
  have hv (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j =
        (if j = 0 then torusGeom_c i else 1) := by
    by_cases hj : j = 0
    · simp only [torusGeom_v, if_pos hj]
      exact torusGeom_cycle torusGeom_c hc i
    · simp only [torusGeom_v, if_neg hj, one_mul]
  have hh (i : Fin (m' + 1)) (j : Fin (n' + 1)) :
      torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j) =
        torusGeom_d i j :=
    torusGeom_cycle (torusGeom_d i) (hd i) j
  let torusGeom_σ : TorusEdge (m' + 1) (n' + 1) → ℤˣ := fun e =>
    match e with
    | Sum.inl p => torusGeom_h p.1 p.2
    | Sum.inr p => torusGeom_v p.1 p.2
  refine ⟨torusGeom_σ, ?_⟩
  intro p
  rcases p with ⟨i, j⟩
  rw [torus_plaq_explicit hm hn]
  change torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j) *
      torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j = t (i, j)
  calc
    torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j) *
        torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j =
        (torusGeom_h i j * torusGeom_h i (finRotate (n' + 1) j)) *
          (torusGeom_v i j * torusGeom_v (finRotate (m' + 1) i) j) := by
      rw [mul_assoc]
    _ = torusGeom_d i j * (if j = 0 then torusGeom_c i else 1) := by
      rw [hh, hv]
    _ = t (i, j) := by
      dsimp only [torusGeom_d]
      rw [mul_assoc, grid_sign_square, mul_one]

end TubeArea
