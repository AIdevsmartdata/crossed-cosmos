/-
PART D: the explicit rectangular patch.  The harness compiles the concatenation
  PARTIE_ABC_gelee.lean (frozen: column_flip_bound, sharp_one_edge, wilson_column_flip_bound)  ++  this file  ++  a footer.
So this file must NOT contain `import` lines and may use everything from the frozen parts.
-/

open MeasureTheory Finset

namespace TubeArea

/-- Vertices `(i,j)` with `0 ≤ i ≤ m` and `0 ≤ j ≤ n`. -/
abbrev GridVertex (m n : ℕ) := Fin (m + 1) × Fin (n + 1)

/-- Unoriented edges of the free rectangular grid.  The left summand is
horizontal, the right summand vertical. -/
abbrev GridEdge (m n : ℕ) :=
  (Fin m × Fin (n + 1)) ⊕ (Fin (m + 1) × Fin n)

/-- The horizontal edge from `(i,j)` to `(i+1,j)`. -/
def gridH {m n : ℕ} (i : Fin m) (j : Fin (n + 1)) : GridEdge m n :=
  Sum.inl (i, j)

/-- The vertical edge from `(i,j)` to `(i,j+1)`. -/
def gridV {m n : ℕ} (i : Fin (m + 1)) (j : Fin n) : GridEdge m n :=
  Sum.inr (i, j)

/-- The four literal boundary edges of the plaquette with lower-left corner `p`.
`castSucc` keeps a coordinate; `succ` adds one to it. -/
def gridBd {m n : ℕ} (p : Fin m × Fin n) : Finset (GridEdge m n) :=
  {gridH p.1 p.2.castSucc, gridH p.1 p.2.succ,
    gridV p.1.castSucc p.2, gridV p.1.succ p.2}

lemma grid_castSucc_ne_succ {k : ℕ} (i : Fin k) : i.castSucc ≠ i.succ := by
  intro h
  have hv := congrArg Fin.val h
  change i.val = i.val + 1 at hv
  omega

lemma grid_sign_square (u : ℤˣ) : u * u = 1 := by
  rcases cf_sign_cases u with rfl | rfl <;> simp

lemma grid_sign_inv (u : ℤˣ) : u⁻¹ = u := by
  rcases cf_sign_cases u with rfl | rfl <;> simp

lemma grid_plaq_eq {m n : ℕ} (σ : GridEdge m n → ℤˣ) (i : Fin m) (j : Fin n) :
    plaq gridBd σ (i, j) =
      (σ (gridH i j.castSucc) * σ (gridH i j.succ)) *
        (σ (gridV i.castSucc j) * σ (gridV i.succ j)) := by
  have hi := grid_castSucc_ne_succ i
  have hj := grid_castSucc_ne_succ j
  have hi' : i.succ ≠ i.castSucc := fun h => hi h.symm
  have hj' : j.succ ≠ j.castSucc := fun h => hj h.symm
  simp [plaq, gridBd, gridH, gridV, hi, hj, hi', hj', mul_assoc]

/-- Product of the target signs below height `r` in column `i`.
The extra `if` merely makes this a function of every natural `r`; all its uses
on grid edges have `r ≤ n`. -/
def gridPrefix {m n : ℕ} (t : Fin m × Fin n → ℤˣ) (i : Fin m) (r : ℕ) : ℤˣ :=
  ∏ k ∈ Finset.range r, if hk : k < n then t (i, ⟨k, hk⟩) else 1

lemma gridPrefix_succ {m n : ℕ} (t : Fin m × Fin n → ℤˣ)
    (i : Fin m) (j : Fin n) :
    gridPrefix t i (j.val + 1) = gridPrefix t i j.val * t (i, j) := by
  unfold gridPrefix
  rw [Finset.prod_range_succ]
  simp [j.isLt]

/-- Every assignment of plaquette signs is realised by edge signs.
Vertical edges are `1`; a horizontal edge receives the prefix product below it.
This includes grids with zero rows or zero columns. -/
theorem grid_plaq_surjective (m n : ℕ) :
    Function.Surjective (fun σ : GridEdge m n → ℤˣ => plaq gridBd σ) := by
  intro t
  let σ : GridEdge m n → ℤˣ := fun e =>
    match e with
    | Sum.inl ij => gridPrefix t ij.1 ij.2.val
    | Sum.inr _ => 1
  refine ⟨σ, ?_⟩
  funext p
  rcases p with ⟨i, j⟩
  change plaq gridBd σ (i, j) = t (i, j)
  rw [grid_plaq_eq]
  change (gridPrefix t i j.val * gridPrefix t i (j.val + 1)) * (1 * 1) = t (i, j)
  rw [gridPrefix_succ]
  simp only [mul_one, ← mul_assoc, grid_sign_square, one_mul]

/-- Grid indices in the half-open natural interval `[a,b)`.
Using a filter makes its membership condition literal, even for an empty interval. -/
def gridInterval (k a b : ℕ) : Finset (Fin k) :=
  Finset.univ.filter (fun i => a ≤ i.val ∧ i.val < b)

lemma mem_gridInterval {k a b : ℕ} (i : Fin k) :
    i ∈ gridInterval k a b ↔ a ≤ i.val ∧ i.val < b := by
  simp [gridInterval]

lemma gridInterval_card (k a b : ℕ) (hb : b ≤ k) :
    (gridInterval k a b).card = b - a := by
  have hcard : (gridInterval k a b).card = (Finset.Ico a b).card := by
    apply Finset.card_bij (fun i _ => i.val)
    · intro i hi
      exact Finset.mem_Ico.mpr ((mem_gridInterval i).mp hi)
    · intro i _ j _ hij
      exact Fin.ext hij
    · intro r hr
      have hr' := Finset.mem_Ico.mp hr
      have hrk : r < k := by omega
      refine ⟨⟨r, hrk⟩, ?_, rfl⟩
      exact (mem_gridInterval ⟨r, hrk⟩).mpr hr'
  simpa only [Nat.card_Ico] using hcard

lemma gridInterval_prod {M : Type*} [CommMonoid M]
    (k a b : ℕ) (hb : b ≤ k) (f : ℕ → M) :
    (∏ i ∈ gridInterval k a b, f i.val) = ∏ r ∈ Finset.Ico a b, f r := by
  apply Finset.prod_bij (fun i _ => i.val)
  · intro i hi
    exact Finset.mem_Ico.mpr ((mem_gridInterval i).mp hi)
  · intro i _ j _ hij
    exact Fin.ext hij
  · intro r hr
    have hr' := Finset.mem_Ico.mp hr
    have hrk : r < k := by omega
    refine ⟨⟨r, hrk⟩, ?_, rfl⟩
    exact (mem_gridInterval ⟨r, hrk⟩).mpr hr'
  · intro _ _
    rfl

lemma grid_sign_telescope (f : ℕ → ℤˣ) {a b : ℕ} (hab : a ≤ b) :
    (∏ r ∈ Finset.Ico a b, f r * f (r + 1)) = f a * f b := by
  calc
    (∏ r ∈ Finset.Ico a b, f r * f (r + 1)) =
        ∏ r ∈ Finset.Ico a b, f (r + 1) / f r := by
      apply Finset.prod_congr rfl
      intro r _
      simp only [div_eq_mul_inv, grid_sign_inv, mul_comm]
    _ = f b / f a := Finset.prod_Ico_div f hab
    _ = f a * f b := by simp only [div_eq_mul_inv, grid_sign_inv, mul_comm]

/-- Extend a finite sequence of vertex signs to natural indices, using `1`
outside its domain.  Only values inside the domain enter the telescope. -/
def gridExtend {k : ℕ} (f : Fin (k + 1) → ℤˣ) (r : ℕ) : ℤˣ :=
  if hr : r < k + 1 then f ⟨r, hr⟩ else 1

lemma gridExtend_at {k : ℕ} (f : Fin (k + 1) → ℤˣ) (i : Fin (k + 1)) :
    gridExtend f i.val = f i := by
  simp [gridExtend, i.isLt]

lemma grid_interval_telescope {k : ℕ} (f : Fin (k + 1) → ℤˣ)
    (a b : Fin (k + 1)) (hab : a.val ≤ b.val) :
    (∏ i ∈ gridInterval k a.val b.val, f i.castSucc * f i.succ) = f a * f b := by
  have hb : b.val ≤ k := by have h := b.isLt; omega
  have hl (i : Fin k) : gridExtend f i.val = f i.castSucc :=
    gridExtend_at f i.castSucc
  have hr (i : Fin k) : gridExtend f (i.val + 1) = f i.succ :=
    gridExtend_at f i.succ
  calc
    (∏ i ∈ gridInterval k a.val b.val, f i.castSucc * f i.succ) =
        ∏ i ∈ gridInterval k a.val b.val,
          gridExtend f i.val * gridExtend f (i.val + 1) := by
      apply Finset.prod_congr rfl
      intro i _
      rw [hl, hr]
    _ = ∏ r ∈ Finset.Ico a.val b.val,
          gridExtend f r * gridExtend f (r + 1) :=
      gridInterval_prod k a.val b.val hb
        (fun r => gridExtend f r * gridExtend f (r + 1))
    _ = gridExtend f a.val * gridExtend f b.val := grid_sign_telescope _ hab
    _ = f a * f b := by rw [gridExtend_at, gridExtend_at]

/-- Plaquettes of `[a,b] × [c,d]`: precisely `a ≤ i < b` and `c ≤ j < d`.
Endpoints are vertex indices, so their upper bounds by `m` and `n` are in their
`Fin` types rather than supplied as extra proof arguments. -/
def rectPlaquettes {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    Finset (Fin m × Fin n) :=
  (gridInterval m a.val b.val) ×ˢ (gridInterval n c.val d.val)

lemma mem_rectPlaquettes {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (p : Fin m × Fin n) :
    p ∈ rectPlaquettes a b c d ↔
      (a.val ≤ p.1.val ∧ p.1.val < b.val) ∧ (c.val ≤ p.2.val ∧ p.2.val < d.val) := by
  simp [rectPlaquettes, mem_gridInterval]

lemma rectPlaquettes_card {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    (rectPlaquettes a b c d).card = (b.val - a.val) * (d.val - c.val) := by
  have hb : b.val ≤ m := by have h := b.isLt; omega
  have hd : d.val ≤ n := by have h := d.isLt; omega
  unfold rectPlaquettes
  rw [Finset.card_product, gridInterval_card m a.val b.val hb,
    gridInterval_card n c.val d.val hd]

/-- Literal union of bottom, right, top, and left edge sets.
Stokes for this set requires positive width and height: coincident sides in a
degenerate rectangle would occur only once in a finset. -/
def rectBoundary {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    Finset (GridEdge m n) :=
  (((gridInterval m a.val b.val).image (fun i => gridH i c) ∪
    (gridInterval n c.val d.val).image (fun j => gridV b j)) ∪
    (gridInterval m a.val b.val).image (fun i => gridH i d)) ∪
    (gridInterval n c.val d.val).image (fun j => gridV a j)

/-- Counterclockwise plaquette word, starting at the lower-left corner:
bottom forwards, right forwards, top backwards, left backwards. -/
def gridWord {m n : ℕ} (p : Fin m × Fin n) : List (GridEdge m n × Bool) :=
  [(gridH p.1 p.2.castSucc, true), (gridV p.1.succ p.2, true),
    (gridH p.1 p.2.succ, false), (gridV p.1.castSucc p.2, false)]

lemma gridWord_nodup {m n : ℕ} (p : Fin m × Fin n) :
    ((gridWord p).map Prod.fst).Nodup := by
  rcases p with ⟨i, j⟩
  have hi := grid_castSucc_ne_succ i
  have hj := grid_castSucc_ne_succ j
  have hi' : i.succ ≠ i.castSucc := fun h => hi h.symm
  have hj' : j.succ ≠ j.castSucc := fun h => hj h.symm
  simp [gridWord, gridH, gridV, hi, hj, hi', hj']

lemma gridWord_boundary {m n : ℕ} (p : Fin m × Fin n) :
    wordBoundary (gridWord p) = gridBd p := by
  ext e
  simp [wordBoundary, gridWord, gridBd, or_assoc, or_left_comm, or_comm]

/-- Increasing list of grid indices in `[a,b)`.  Filtering `finRange` keeps
the natural order; its underlying finset is `gridInterval`. -/
def gridIndexList (k a b : ℕ) : List (Fin k) :=
  (List.finRange k).filter (fun i => decide (a ≤ i.val ∧ i.val < b))

lemma gridIndexList_nodup (k a b : ℕ) : (gridIndexList k a b).Nodup := by
  exact List.Nodup.filter _ (List.nodup_finRange k)

lemma gridIndexList_toFinset (k a b : ℕ) :
    (gridIndexList k a b).toFinset = gridInterval k a b := by
  ext i
  simp [gridIndexList, gridInterval]

/-- Horizontal edges at a fixed row, in the order supplied by the index list. -/
def gridHSide {m n : ℕ} (l : List (Fin m)) (r : Fin (n + 1)) :
    List (GridEdge m n) := l.map (fun i => gridH i r)

/-- Vertical edges at a fixed column, in the order supplied by the index list. -/
def gridVSide {m n : ℕ} (l : List (Fin n)) (r : Fin (m + 1)) :
    List (GridEdge m n) := l.map (fun j => gridV r j)

lemma gridHSide_nodup {m n : ℕ} (l : List (Fin m)) (r : Fin (n + 1))
    (hl : l.Nodup) : (gridHSide l r).Nodup := by
  unfold gridHSide
  apply List.Nodup.map ?_ hl
  intro i j hij
  simpa [gridH] using hij

lemma gridVSide_nodup {m n : ℕ} (l : List (Fin n)) (r : Fin (m + 1))
    (hl : l.Nodup) : (gridVSide l r).Nodup := by
  unfold gridVSide
  apply List.Nodup.map ?_ hl
  intro i j hij
  simpa [gridV] using hij

lemma gridHSide_disjoint {m n : ℕ} (l l' : List (Fin m))
    (r s : Fin (n + 1)) (hrs : r ≠ s) :
    List.Disjoint (gridHSide l r) (gridHSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  obtain ⟨i, _, hi⟩ := List.mem_map.mp he
  obtain ⟨j, _, hj⟩ := List.mem_map.mp he'
  have hp : i = j ∧ r = s := by simpa [gridH] using hi.trans hj.symm
  exact hrs hp.2

lemma gridVSide_disjoint {m n : ℕ} (l l' : List (Fin n))
    (r s : Fin (m + 1)) (hrs : r ≠ s) :
    List.Disjoint (gridVSide l r) (gridVSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  obtain ⟨i, _, hi⟩ := List.mem_map.mp he
  obtain ⟨j, _, hj⟩ := List.mem_map.mp he'
  have hp : r = s ∧ i = j := by simpa [gridV] using hi.trans hj.symm
  exact hrs hp.1

lemma gridHVSide_disjoint {m n : ℕ} (l : List (Fin m)) (l' : List (Fin n))
    (r : Fin (n + 1)) (s : Fin (m + 1)) :
    List.Disjoint (gridHSide l r) (gridVSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  obtain ⟨i, _, hi⟩ := List.mem_map.mp he
  obtain ⟨j, _, hj⟩ := List.mem_map.mp he'
  simpa [gridH, gridV] using hi.trans hj.symm

lemma gridVHSide_disjoint {m n : ℕ} (l : List (Fin n)) (l' : List (Fin m))
    (r : Fin (m + 1)) (s : Fin (n + 1)) :
    List.Disjoint (gridVSide l r) (gridHSide l' s) := by
  apply List.disjoint_left.mpr
  intro e he he'
  exact (List.disjoint_left.mp (gridHVSide_disjoint l' l s r)) he' he

lemma grid_four_lists_nodup {E : Type*} (B R T L : List E)
    (hB : B.Nodup) (hR : R.Nodup) (hT : T.Nodup) (hL : L.Nodup)
    (hBR : List.Disjoint B R) (hBT : List.Disjoint B T) (hBL : List.Disjoint B L)
    (hRT : List.Disjoint R T) (hRL : List.Disjoint R L) (hTL : List.Disjoint T L) :
    (((B ++ R) ++ T.reverse) ++ L.reverse).Nodup := by
  simp only [List.nodup_append', List.nodup_reverse, List.disjoint_left,
    List.mem_append, List.mem_reverse] at *
  aesop

/-- Counterclockwise rectangle word starting at `(a,c)`: bottom and right
in increasing order and with positive orientation, then top and left in
decreasing order and with negative orientation. -/
def rectWord {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    List (GridEdge m n × Bool) :=
  (((gridHSide (gridIndexList m a.val b.val) c).map (fun e => (e, true)) ++
    (gridVSide (gridIndexList n c.val d.val) b).map (fun e => (e, true))) ++
    (gridHSide (gridIndexList m a.val b.val) d).reverse.map (fun e => (e, false))) ++
    (gridVSide (gridIndexList n c.val d.val) a).reverse.map (fun e => (e, false))

lemma rectWord_edges {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    (rectWord a b c d).map Prod.fst =
      (((gridHSide (gridIndexList m a.val b.val) c ++
        gridVSide (gridIndexList n c.val d.val) b) ++
        (gridHSide (gridIndexList m a.val b.val) d).reverse) ++
        (gridVSide (gridIndexList n c.val d.val) a).reverse) := by
  simp [rectWord, List.map_append, List.map_map, Function.comp_def]

lemma rectWord_nodup {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val) :
    ((rectWord a b c d).map Prod.fst).Nodup := by
  have hab' : a ≠ b := by
    intro h
    have hv := congrArg Fin.val h
    omega
  have hcd' : c ≠ d := by
    intro h
    have hv := congrArg Fin.val h
    omega
  rw [rectWord_edges]
  apply grid_four_lists_nodup
  · exact gridHSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridVSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridHSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridVSide_nodup _ _ (gridIndexList_nodup _ _ _)
  · exact gridHVSide_disjoint _ _ _ _
  · exact gridHSide_disjoint _ _ _ _ hcd'
  · exact gridHVSide_disjoint _ _ _ _
  · exact gridVHSide_disjoint _ _ _ _
  · exact gridVSide_disjoint _ _ _ _ (fun h => hab' h.symm)
  · exact gridHVSide_disjoint _ _ _ _

lemma gridHSide_toFinset {m n : ℕ} (l : List (Fin m)) (r : Fin (n + 1)) :
    (gridHSide l r).toFinset = l.toFinset.image (fun i => gridH i r) := by
  ext e
  simp [gridHSide]

lemma gridVSide_toFinset {m n : ℕ} (l : List (Fin n)) (r : Fin (m + 1)) :
    (gridVSide l r).toFinset = l.toFinset.image (fun j => gridV r j) := by
  ext e
  simp [gridVSide]

lemma rectWord_boundary {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1)) :
    wordBoundary (rectWord a b c d) = rectBoundary a b c d := by
  unfold wordBoundary
  rw [rectWord_edges]
  simp only [List.toFinset_append, List.toFinset_reverse, gridHSide_toFinset,
    gridVSide_toFinset, gridIndexList_toFinset, rectBoundary]

lemma gridHSide_prod {m n : ℕ} (σ : GridEdge m n → ℤˣ) (a b : ℕ)
    (r : Fin (n + 1)) :
    ((gridHSide (gridIndexList m a b) r).map σ).prod =
      ∏ i ∈ gridInterval m a b, σ (gridH i r) := by
  simp only [gridHSide, List.map_map, Function.comp_def]
  simpa only [gridIndexList_toFinset] using
    (List.prod_toFinset (fun i : Fin m => σ (gridH i r)) (gridIndexList_nodup m a b)).symm

lemma gridVSide_prod {m n : ℕ} (σ : GridEdge m n → ℤˣ) (a b : ℕ)
    (r : Fin (m + 1)) :
    ((gridVSide (gridIndexList n a b) r).map σ).prod =
      ∏ j ∈ gridInterval n a b, σ (gridV r j) := by
  simp only [gridVSide, List.map_map, Function.comp_def]
  simpa only [gridIndexList_toFinset] using
    (List.prod_toFinset (fun j : Fin n => σ (gridV r j)) (gridIndexList_nodup n a b)).symm

lemma rectBoundary_prod {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val) (σ : GridEdge m n → ℤˣ) :
    (∏ e ∈ rectBoundary a b c d, σ e) =
      ((∏ i ∈ gridInterval m a.val b.val, σ (gridH i c)) *
        (∏ j ∈ gridInterval n c.val d.val, σ (gridV b j))) *
        (∏ i ∈ gridInterval m a.val b.val, σ (gridH i d)) *
        (∏ j ∈ gridInterval n c.val d.val, σ (gridV a j)) := by
  calc
    (∏ e ∈ rectBoundary a b c d, σ e) =
        (((rectWord a b c d).map Prod.fst).map σ).prod := by
      rw [← rectWord_boundary]
      exact List.prod_toFinset σ (rectWord_nodup a b c d hab hcd)
    _ = _ := by
      rw [rectWord_edges]
      simp only [List.map_append, List.prod_append, List.map_reverse,
        List.prod_reverse, gridHSide_prod, gridVSide_prod]

lemma grid_column_plaq_prod {m n : ℕ} (σ : GridEdge m n → ℤˣ) (i : Fin m)
    (c d : Fin (n + 1)) (hcd : c.val ≤ d.val) :
    (∏ j ∈ gridInterval n c.val d.val, plaq gridBd σ (i, j)) =
      (σ (gridH i c) * σ (gridH i d)) *
        ((∏ j ∈ gridInterval n c.val d.val, σ (gridV i.castSucc j)) *
          (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.succ j))) := by
  calc
    (∏ j ∈ gridInterval n c.val d.val, plaq gridBd σ (i, j)) =
        (∏ j ∈ gridInterval n c.val d.val,
          σ (gridH i j.castSucc) * σ (gridH i j.succ)) *
        (∏ j ∈ gridInterval n c.val d.val,
          σ (gridV i.castSucc j) * σ (gridV i.succ j)) := by
      simp only [grid_plaq_eq, Finset.prod_mul_distrib]
    _ = _ := by
      rw [grid_interval_telescope (fun r => σ (gridH i r)) c d hcd,
        Finset.prod_mul_distrib]

lemma rectPlaquettes_prod {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val ≤ b.val) (hcd : c.val ≤ d.val) (σ : GridEdge m n → ℤˣ) :
    (∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p) =
      ((∏ i ∈ gridInterval m a.val b.val, σ (gridH i c)) *
        (∏ i ∈ gridInterval m a.val b.val, σ (gridH i d))) *
        ((∏ j ∈ gridInterval n c.val d.val, σ (gridV a j)) *
          (∏ j ∈ gridInterval n c.val d.val, σ (gridV b j))) := by
  calc
    (∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p) =
        ∏ i ∈ gridInterval m a.val b.val,
          ∏ j ∈ gridInterval n c.val d.val, plaq gridBd σ (i, j) :=
      Finset.prod_product _ _ _
    _ = ∏ i ∈ gridInterval m a.val b.val,
        (σ (gridH i c) * σ (gridH i d)) *
          ((∏ j ∈ gridInterval n c.val d.val, σ (gridV i.castSucc j)) *
            (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.succ j))) := by
      apply Finset.prod_congr rfl
      intro i _
      exact grid_column_plaq_prod σ i c d hcd
    _ = (∏ i ∈ gridInterval m a.val b.val, σ (gridH i c) * σ (gridH i d)) *
        (∏ i ∈ gridInterval m a.val b.val,
          (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.castSucc j)) *
            (∏ j ∈ gridInterval n c.val d.val, σ (gridV i.succ j))) :=
      Finset.prod_mul_distrib
    _ = _ := by
      rw [Finset.prod_mul_distrib,
        grid_interval_telescope
          (fun r => ∏ j ∈ gridInterval n c.val d.val, σ (gridV r j)) a b hab]

/-- Stokes for a nondegenerate literal rectangle: each interior edge cancels
twice and each boundary edge occurs once.  Positive side lengths are necessary
for the literal set-union definition of `rectBoundary`. -/
theorem grid_stokes_rectangle {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val) (σ : GridEdge m n → ℤˣ) :
    (∏ e ∈ rectBoundary a b c d, σ e) =
      ∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p := by
  rw [rectBoundary_prod a b c d hab hcd σ,
    rectPlaquettes_prod a b c d (by omega) (by omega) σ]
  ac_rfl

/-- The elementary area law on the explicit free rectangular patch times a
finite fibre.  The geometry, sign surjectivity, and absence of repeated edges
are proved above.  The analytic and group hypotheses are precisely those of
the frozen Wilson column-flip bound; the exponent is the literal rectangle area.
The endpoint types encode `b ≤ m` and `d ≤ n`. -/
theorem tube_area_law_rectangle
    {G F X : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X]
    (m n : ℕ) (a b : Fin (m + 1)) (c d : Fin (n + 1))
    (hab : a.val < b.val) (hcd : c.val < d.val)
    (haarG : Measure G) [IsProbabilityMeasure haarG]
    (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
    (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
    (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
    (hodd : ∀ g, chi (z * g) = -chi g)
    (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
    (β : ℝ) (hβ : 0 ≤ β)
    (R : WilsonConfig G (GridEdge m n) F X → ℝ)
    (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
    (hRflip : ∀ σ ω, R (columnFlip z σ ω) = R ω)
    (hRint : Integrable
      (fun ω => R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
      (wilsonMeasure haarG))
    (y0 : F) :
    |∫ ω, wilsonLoop chi (rectWord a b c d) y0 ω *
        (R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
        ∂wilsonMeasure haarG| ≤
      Real.tanh (β * (Fintype.card F : ℝ)) ^ ((b.val - a.val) * (d.val - c.val)) *
        ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω)
          ∂wilsonMeasure haarG := by
  have hStokes (σ : GridEdge m n → ℤˣ) :
      (∏ e ∈ wordBoundary (rectWord a b c d), σ e) =
        ∏ p ∈ rectPlaquettes a b c d,
          plaq (fun p : Fin m × Fin n => wordBoundary (gridWord p)) σ p := by
    simpa only [rectWord_boundary, gridWord_boundary] using
      grid_stokes_rectangle a b c d hab hcd σ
  have hsurj : Function.Surjective
      (fun σ : GridEdge m n → ℤˣ =>
        plaq (fun p : Fin m × Fin n => wordBoundary (gridWord p)) σ) := by
    simpa only [gridWord_boundary] using grid_plaq_surjective m n
  have h := wilson_column_flip_bound (E := GridEdge m n) (P := Fin m × Fin n)
    (F := F) (X := X)
    haarG hleft z hz hcentral chi hchim hchi1 hodd
    gridWord gridWord_nodup weights hweights β hβ R hRm hR0 hRflip hRint
    (rectWord a b c d) (rectWord_nodup a b c d hab hcd) y0
    (rectPlaquettes a b c d) hStokes hsurj
  simpa only [rectPlaquettes_card] using h

end TubeArea
