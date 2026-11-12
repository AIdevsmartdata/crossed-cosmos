
noncomputable section

namespace CentreZN

/-! ## Partie B : théorie de type Wilson à élément central d'ordre `N` (définitions figées) -/

/-- Configurations: long links `(e, y)` (base edge `e`, fibre site `y`) and other links `x`. -/
abbrev Config (G E F X : Type*) := ((E × F) → G) × (X → G)

/-- The product of the single-link measure over all links. -/
def configMeasure {G E F X : Type*} [MeasurableSpace G] [Fintype E] [Fintype F] [Fintype X]
    (haarG : Measure G) : Measure (Config G E F X) :=
  (Measure.pi fun _ : E × F => haarG).prod (Measure.pi fun _ : X => haarG)

/-- Column twist: every long link `(e, y)` is left-multiplied by `z ^ (σ e).val`; other links are unchanged. -/
def columnTwist {G E F X : Type*} [Monoid G] {N : ℕ} (z : G) (σ : E → ZMod N)
    (ω : Config G E F X) : Config G E F X :=
  (fun ey => z ^ (σ ey.1).val * ω.1 ey, ω.2)

/-- Positive orientation: the link itself; negative orientation: its inverse. -/
def orientedLink {G : Type*} [Inv G] : Bool → G → G
  | true, g => g
  | false, g => g⁻¹

/-- A word: a list of oriented letters, each a long link `Sum.inl (e, y)` or another link `Sum.inr x`. -/
abbrev Word (E F X : Type*) := List (((E × F) ⊕ X) × Bool)

/-- Ordered holonomy of a word (empty word: `1`). -/
def holonomy {G E F X : Type*} [Group G] : Word E F X → Config G E F X → G
  | [], _ => 1
  | (Sum.inl ey, b) :: w, ω => orientedLink b (ω.1 ey) * holonomy w ω
  | (Sum.inr x, b) :: w, ω => orientedLink b (ω.2 x) * holonomy w ω

/-- Charge of a word: signed sum (with multiplicity) of the column variables of its long letters. -/
def charge {E F X : Type*} {N : ℕ} : Word E F X → (E → ZMod N) → ZMod N
  | [], _ => 0
  | (Sum.inl ey, b) :: w, σ => (if b then σ ey.1 else -σ ey.1) + charge w σ
  | (Sum.inr _, _) :: w, σ => charge w σ

/-- A word is neutral for `ZMod N` when its charge vanishes for all column variables. -/
def Neutral {E F X : Type*} (N : ℕ) (w : Word E F X) : Prop :=
  ∀ σ : E → ZMod N, charge w σ = 0

/-- The word of a base path (list of oriented base edges) at the fibre site `y`. -/
def baseWord {E F X : Type*} (w : List (E × Bool)) (y : F) : Word E F X :=
  w.map fun a => (Sum.inl (a.1, y), a.2)

/-- Charge of a base path: signed sum (with multiplicity) of the column variables along it. -/
def baseCharge {E : Type*} {N : ℕ} : List (E × Bool) → (E → ZMod N) → ZMod N
  | [], _ => 0
  | a :: w, σ => (if a.2 then σ a.1 else -σ a.1) + baseCharge w σ

/-- Complex Wilson coupling of the base plaquette `p`: `β Σ_y c p y χ(holonomy of its word at y)`.
The action uses its real part. -/
def coupling {G E F X P : Type*} [Group G] [Fintype F]
    (β : ℝ) (c : P → F → ℂ) (chi : G → ℂ) (w : P → List (E × Bool)) (p : P)
    (ω : Config G E F X) : ℂ :=
  (β : ℂ) * ∑ y, c p y * chi (holonomy (baseWord (w p) y) ω)

/-- Weight of a finite family of extra terms: `exp (Σ_k Re (coef k · χ(holonomy of the word k)))`. -/
def termsWeight {G E F X Q : Type*} [Group G] [Fintype Q]
    (chi : G → ℂ) (wq : Q → Word E F X) (coef : Q → ℂ) (ω : Config G E F X) : ℝ :=
  Real.exp (∑ k, (coef k * chi (holonomy (wq k) ω)).re)

/-- Edges of the discrete torus `(ℤ/m) × (ℤ/n)`: `Sum.inl (i,j)` is the horizontal edge from `(i,j)` to `(i+1,j)`,
`Sum.inr (i,j)` the vertical edge from `(i,j)` to `(i,j+1)`; indices are cyclic (`finRotate`). -/
abbrev TorusEdge (m n : ℕ) := (Fin m × Fin n) ⊕ (Fin m × Fin n)

/-- Counterclockwise plaquette path from the corner `p = (i,j)`: bottom `H(i,j)` forwards, right `V(i+1,j)`
forwards, top `H(i,j+1)` backwards, left `V(i,j)` backwards. -/
def torusWord {m n : ℕ} (p : Fin m × Fin n) : List (TorusEdge m n × Bool) :=
  [(Sum.inl (p.1, p.2), true), (Sum.inr (finRotate m p.1, p.2), true),
    (Sum.inl (p.1, finRotate n p.2), false), (Sum.inr (p.1, p.2), false)]

end CentreZN

end

