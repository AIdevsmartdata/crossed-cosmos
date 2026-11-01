import LoiAire.Certificat
import LoiAire.Arith
import LoiAire.CertPetits
import LoiAire.DonneesM11
import LoiAire.Poids

/-!
# (d) Énoncé complet du théorème, conditionnel aux étapes analytiques

1. Définitions CONCRÈTES : SU(2) = quaternions unitaires avec la mesure de Haar normalisée, tore (ℤ/Lℤ)⁴,
   action de Wilson `β Σ_p ½ Re Tr U_p` (chaque plaquette une fois), boucle rectangulaire R × T (plan (e₀, e₃),
   coin à l'origine), espérance `wilson L β R T`. Poids par site `Atilde J n = ∫₀¹ f_n h_J` (PREUVE.md §5) et
   somme de marches `Gtilde` de (5.1) (marches du tore spatial (ℤ/Lℤ)³ de 0 à R e₀, poids `J^{|ω|} Π_z Ã_{n_z}`).
2. `HypothesesBS` : les étapes ANALYTIQUES, admises (non démontrées en Lean) :
   * `reduction` = (5.1), qui résume §§1–5 : tranches de Durhuus–Fröhlich, développement en marches (prop. 2.2),
     contraction en caractères (§3), matrice de transfert et positivité (4.1), Peter–Weyl (lemme 4.2, prop. 4.3),
     Douglas–Hölder (prop. 4.4), Cauchy–Schwarz (cor. 5.2) ;
   * `monotonie` (lemme 6.1), `poids_certifies` (lemme 5.3 + encadrements rationnels de c1, §7).
   (Les faits élémentaires Ã_n > 0 et Ã₁ ≤ 1/2 sont DÉMONTRÉS dans `Poids.lean`.)
3. Démontré ici : tout le reste (lecture pas à pas Π_z Ã_{n_z} = Π_j r̃(N_j), tore → fenêtre, lemme 7.1 avec le
   certificat, longueur ≥ R des marches de 0 à R e₀, série géométrique, constantes).
   * `loi_aire_conditionnelle` : énoncé générique (m, J*, poids, certificat quelconques) ;
   * `theoreme1_conditionnel` : β ≤ 0,81348 (m = 11), sous `HypothesesBS` et `CertificatM11` (établi par
     l'exécutable compilé `verifcert`, pas par le noyau) ;
   * `theoreme_m5_conditionnel` : β ≤ 0,80438 (m = 5), sous `HypothesesBS` SEULEMENT (certificat vérifié par le
     noyau).
-/

namespace LoiAire

open MeasureTheory Finset

noncomputable section

/-! ## 1. La mesure de Wilson SU(2) sur le tore (ℤ/Lℤ)⁴ -/

/-- SU(2) ≅ quaternions unitaires (½ Tr U = Re q, U⁻¹ ↔ q̄ = star q). -/
abbrev SU2 := Metric.sphere (0 : Quaternion ℝ) 1

instance : MeasurableSpace (Quaternion ℝ) := borel _
instance : BorelSpace (Quaternion ℝ) := ⟨rfl⟩

/-- Mesure de Haar normalisée de SU(2). -/
def haarSU2 : Measure SU2 := Measure.haarMeasure ⊤

theorem haarSU2_univ : haarSU2 Set.univ = 1 := by
  unfold haarSU2
  simpa using Measure.haarMeasure_self (G := SU2) (K₀ := ⊤)

abbrev Site (L : ℕ) := Fin 4 → ZMod L
abbrev Config (L : ℕ) := Site L × Fin 4 → SU2

/-- Vecteur unité du tore 4D. -/
def eμ (L : ℕ) (μ : Fin 4) : Site L := Pi.single μ 1

/-- Holonomie de la plaquette (x; μ, ν) : U_{x,μ} U_{x+μ,ν} U_{x+ν,μ}⁻¹ U_{x,ν}⁻¹. -/
def plaquette {L : ℕ} (U : Config L) (x : Site L) (μ ν : Fin 4) : Quaternion ℝ :=
  (U (x, μ) : Quaternion ℝ) * (U (x + eμ L μ, ν) : Quaternion ℝ) * star (U (x + eμ L ν, μ) : Quaternion ℝ) *
    star (U (x, ν) : Quaternion ℝ)

/-- Action de Wilson `β Σ_p ½ Re Tr U_p`, chaque plaquette (x, μ < ν) comptée une fois. -/
def action (L : ℕ) [NeZero L] (β : ℝ) (U : Config L) : ℝ :=
  β * ∑ x : Site L, ∑ μ : Fin 4, ∑ ν : Fin 4, if μ < ν then (plaquette U x μ ν).re else 0

/-- Holonomie du rectangle R × T du plan (e₀, e₃) de coin 0 : R pas selon e₀, T selon e₃, retour. -/
def holonomieRect {L : ℕ} (U : Config L) (R T : ℕ) : Quaternion ℝ :=
  ((List.range R).map (fun i => (U ((i : ZMod L) • eμ L 0, 0) : Quaternion ℝ)) ++
   (List.range T).map (fun k => (U ((R : ZMod L) • eμ L 0 + (k : ZMod L) • eμ L 3, 3) : Quaternion ℝ)) ++
   (List.range R).reverse.map
      (fun i => star (U ((i : ZMod L) • eμ L 0 + (T : ZMod L) • eμ L 3, 0) : Quaternion ℝ)) ++
   (List.range T).reverse.map (fun k => star (U ((k : ZMod L) • eμ L 3, 3) : Quaternion ℝ))).prod

/-- Produit des mesures de Haar sur les liens. -/
def mesureLiens (L : ℕ) [NeZero L] : Measure (Config L) := Measure.pi (fun _ => haarSU2)

/-- ⟨W_{R×T}⟩_{L,β} avec W = ½ tr U_γ = Re(holonomie). -/
def wilson (L : ℕ) [NeZero L] (β : ℝ) (R T : ℕ) : ℝ :=
  (∫ U, (holonomieRect U R T).re * Real.exp (action L β U) ∂(mesureLiens L)) /
    (∫ U, Real.exp (action L β U) ∂(mesureLiens L))

/-! ## 2. Poids par site (PREUVE.md §5) -/

/-- Les poids `Atilde J n = ∫₀¹ λ^{n−1}(1−λ)/(n−1)! · ρ_J((1−λ)²)³ dλ` sont définis dans `LoiAire/Poids.lean`
(`Poids.Mser`, `Poids.rhoJ`, `Poids.hJ`, `Poids.fpoids`, `Poids.Atilde`), où sont DÉMONTRÉS `Poids.Atilde_pos`
(Ã_n(J) > 0) et `Poids.Atilde_one_le` (Ã₁(J) ≤ 1/2). -/
abbrev Atilde := Poids.Atilde

/-- r̃(1) = Ã₁, r̃(N) = Ã_N/Ã_{N−1}. -/
def rt (A : ℕ → ℝ) (N : ℕ) : ℝ := if N ≤ 1 then A 1 else A N / A (N - 1)

/-! ## 3. Marches du tore spatial et somme (5.1) -/

/-- Déplacement total d'un historique (dans ℤ³). -/
def dispZ : List Dir → ℤ × ℤ × ℤ
  | [] => 0
  | d :: w => vec d + dispZ w

/-- Sites visités sur le tore (le plus récent en tête), départ en 0. -/
def sitesT (L : ℕ) : List Dir → List (ZMod L × ZMod L × ZMod L)
  | [] => [0]
  | d :: w => castT L (dispZ (d :: w)) :: sitesT L w

/-- Π_{z visité} A(n_z). -/
def prodVisites {α : Type*} [BEq α] [DecidableEq α] (A : ℕ → ℝ) (l : List α) : ℝ :=
  ∏ z ∈ l.toFinset, A (l.count z)

def cible (L R : ℕ) : ZMod L × ZMod L × ZMod L := ((R : ZMod L), 0, 0)

/-- Poids d'une marche (historique `w`) de 0 à R e₀ : Π_z A(n_z) si elle aboutit, 0 sinon. -/
def poidsMarche (L : ℕ) (A : ℕ → ℝ) (R : ℕ) (w : List Dir) : ℝ :=
  if castT L (dispZ w) = cible L R then prodVisites A (sitesT L w) else 0

/-- G̃ = Σ_n J^n Σ_{|ω| = n, ω : 0 → R e₀} Π_z A(n_z) (somme dans [0, ∞]). -/
def GtildeA (L : ℕ) (A : ℕ → ℝ) (J : ℝ) (R : ℕ) : ENNReal :=
  ∑' n : ℕ, ENNReal.ofReal (J ^ n * sumHist (poidsMarche L A R) n [])

/-- G̃(x, y) de (5.1), avec les vrais poids Ã_n(J). -/
def Gtilde (L : ℕ) (J : ℝ) (R : ℕ) : ENNReal := GtildeA L (Atilde J) J R

/-! ## 4. Les hypothèses analytiques (admises) -/

/-- **Étapes analytiques de PREUVE.md, ADMISES.** Chaque champ est un énoncé précis sur les objets concrets
ci-dessus ; aucun n'est démontré en Lean (Ã_n > 0 et Ã₁ ≤ 1/2, eux, sont démontrés : `Poids.lean`). -/
structure HypothesesBS (Jstar : ℝ) (p : List ℕ) (Q : ℕ) : Prop where
  /-- Lemme 6.1 : J r̃(N; J) ≤ J* r̃(N; J*) pour J ≤ J*. -/
  monotonie : ∀ J, 0 ≤ J → J ≤ Jstar → ∀ N, 1 ≤ N → J * rt (Atilde J) N ≤ Jstar * rt (Atilde Jstar) N
  /-- Lemme 5.3 + certification des poids (c1, §7) : r̃(N; J*) ≤ p_{min(N,13)}/Q. -/
  poids_certifies : ∀ N, 1 ≤ N → rt (Atilde Jstar) N ≤ (pval p N : ℝ) / Q
  /-- (5.1) = §§1–5 : |⟨W_γ⟩| ≤ 2^T G̃^T (tranches, marches, caractères, transfert, Peter–Weyl, Douglas–Hölder,
  Cauchy–Schwarz). -/
  reduction : ∀ (L : ℕ) [NeZero L], 3 ≤ L → ∀ β : ℝ, 0 ≤ β → β ≤ 2 * Jstar → ∀ R T : ℕ, 1 ≤ R → 2 * R ≤ L →
    1 ≤ T → T + 1 ≤ L → ENNReal.ofReal |wilson L β R T| ≤ 2 ^ T * Gtilde L (β / 2) R ^ T

/-! ## 5. Lemmes combinatoires (démontrés) -/

theorem negV_eq (q : ℤ × ℤ × ℤ) : negV q = -q := by
  obtain ⟨a, b, c⟩ := q; rfl

theorem subV_eq (q r : ℤ × ℤ × ℤ) : subV q r = q - r := by
  obtain ⟨a, b, c⟩ := q; obtain ⟨a', b', c'⟩ := r; rfl

theorem castT_add (L : ℕ) (a b : ℤ × ℤ × ℤ) : castT L (a + b) = castT L a + castT L b := by
  obtain ⟨a1, a2, a3⟩ := a; obtain ⟨b1, b2, b3⟩ := b
  simp [castT]

theorem castT_zero (L : ℕ) : castT L 0 = 0 := by simp [castT]

theorem castT_vec_ne_zero (L : ℕ) (hL : 2 ≤ L) (d : Dir) : castT L (vec d) ≠ 0 := by
  have h1 : (1 : ZMod L) ≠ 0 := by
    have : Fact (1 < L) := ⟨by omega⟩
    exact one_ne_zero
  have hm1 : (-1 : ZMod L) ≠ 0 := neg_ne_zero.mpr h1
  fin_cases d <;> simp [castT, vec, h1, hm1, Prod.ext_iff]

/-- Les sites du tore s'obtiennent à partir des positions relatives. -/
theorem sitesT_eq (L : ℕ) (w : List Dir) :
    sitesT L w = (0 :: posList w).map (fun P => castT L (dispZ w + P)) := by
  induction w with
  | nil => simp [sitesT, dispZ, posList, castT_zero]
  | cons d w ih =>
    rw [sitesT, ih]
    simp only [List.map_cons, posList, List.map_map, negV_eq, subV_eq, dispZ, add_zero, Function.comp_def]
    congr 1
    congr 1
    · congr 1; abel
    · apply List.map_congr_left
      intro P _
      congr 1; abel

theorem count_map_add {α : Type*} [AddGroup α] [BEq α] [LawfulBEq α] (c y : α) (l : List α) :
    (l.map (fun x => c + x)).count (c + y) = l.count y :=
  List.count_map_of_injective l (fun x => c + x) (add_right_injective c) y

/-- Le nombre de visites sur le tore du nouveau site est `Ntor`. -/
theorem count_sitesT (L : ℕ) (hL : 2 ≤ L) (w : List Dir) (d : Dir) :
    (sitesT L w).count (castT L (dispZ (d :: w))) + 1 = Ntor L w d := by
  rw [sitesT_eq]
  have e1 : (0 :: posList w).map (fun P => castT L (dispZ w + P))
      = ((0 :: posList w).map (castT L)).map (fun x => castT L (dispZ w) + x) := by
    simp [List.map_map, Function.comp, castT_add]
  have e2 : castT L (dispZ (d :: w)) = castT L (dispZ w) + castT L (vec d) := by
    simp [dispZ, castT_add, add_comm]
  rw [e1, e2, count_map_add]
  simp only [List.map_cons, List.count_cons, castT_zero]
  have hne : ((0 : ZMod L × ZMod L × ZMod L) == castT L (vec d)) = false := by
    rw [beq_eq_false_iff_ne]
    exact fun h => castT_vec_ne_zero L hL d h.symm
  rw [hne]
  simp [Ntor]
  omega

/-- Lecture pas à pas (télescopage) : Π_z A(n_z) sur `z :: l` = r̃(n + 1) · Π_z A(n_z) sur `l`. -/
theorem prodVisites_cons {α : Type*} [BEq α] [LawfulBEq α] [DecidableEq α] (A : ℕ → ℝ) (hA : ∀ n, 1 ≤ n → 0 < A n)
    (z : α) (l : List α) : prodVisites A (z :: l) = rt A (l.count z + 1) * prodVisites A l := by
  unfold prodVisites
  by_cases hz : z ∈ l
  · have hc : 1 ≤ l.count z := List.count_pos_iff.mpr hz
    have hfs : (z :: l).toFinset = l.toFinset := by
      ext a; simp only [List.mem_toFinset, List.mem_cons]; constructor
      · rintro (rfl | h) <;> assumption
      · intro h; exact Or.inr h
    rw [hfs]
    have hzf : z ∈ l.toFinset := List.mem_toFinset.mpr hz
    rw [← Finset.mul_prod_erase _ _ hzf, ← Finset.mul_prod_erase _ (fun x => A (l.count x)) hzf]
    have hrest : ∏ x ∈ l.toFinset.erase z, A (List.count x (z :: l)) = ∏ x ∈ l.toFinset.erase z, A (l.count x) := by
      apply Finset.prod_congr rfl
      intro x hx
      have hxz : x ≠ z := Finset.ne_of_mem_erase hx
      rw [List.count_cons]
      have : (z == x) = false := by simpa using (Ne.symm hxz)
      simp [this]
    rw [hrest, List.count_cons_self]
    have hpos : 0 < A (l.count z) := hA _ hc
    simp only [rt, show ¬ (l.count z + 1 ≤ 1) by omega, ite_false, Nat.add_sub_cancel]
    field_simp
  · have hc : l.count z = 0 := List.count_eq_zero.mpr hz
    have hzf : z ∉ l.toFinset := by simpa using hz
    rw [List.toFinset_cons, Finset.prod_insert hzf, List.count_cons_self, hc]
    have hrest : ∏ x ∈ l.toFinset, A (List.count x (z :: l)) = ∏ x ∈ l.toFinset, A (l.count x) := by
      apply Finset.prod_congr rfl
      intro x hx
      have hxz : x ≠ z := fun h => hz (h ▸ List.mem_toFinset.mp hx)
      rw [List.count_cons]
      have : (z == x) = false := by simpa using (Ne.symm hxz)
      simp [this]
    rw [hrest]
    simp [rt]

/-- Produit des poids de pas le long d'un historique complet. -/
def prodPas (wt : List Dir → Dir → ℝ) : List Dir → ℝ
  | [] => 1
  | d :: w => wt w d * prodPas wt w

theorem prodVisites_sitesT (L : ℕ) (hL : 2 ≤ L) (A : ℕ → ℝ) (hA : ∀ n, 1 ≤ n → 0 < A n) (w : List Dir) :
    prodVisites A (sitesT L w) = A 1 * prodPas (fun w d => rt A (Ntor L w d)) w := by
  induction w with
  | nil => simp [sitesT, prodVisites, prodPas]
  | cons d w ih =>
    rw [sitesT, prodVisites_cons A hA, count_sitesT L hL w d, ih, prodPas]
    ring

theorem prodPas_mul_pow (wt : List Dir → Dir → ℝ) (J : ℝ) (w : List Dir) :
    J ^ w.length * prodPas wt w = prodPas (fun w d => J * wt w d) w := by
  induction w with
  | nil => simp [prodPas]
  | cons d w ih => simp only [prodPas, List.length_cons, pow_succ]; rw [← ih]; ring

theorem sumHist_prodPas (wt : List Dir → Dir → ℝ) :
    ∀ n w, sumHist (prodPas wt) n w = prodPas wt w * Gsum wt n w := by
  intro n
  induction n with
  | zero => intro w; simp [sumHist, Gsum]
  | succ n ih =>
    intro w
    simp only [sumHist, Gsum, ih, prodPas, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun d _ => ?_)
    ring

theorem sumHist_congr (F G : List Dir → ℝ) :
    ∀ n w, (∀ u : List Dir, u.length = w.length + n → F u = G u) → sumHist F n w = sumHist G n w := by
  intro n
  induction n with
  | zero => intro w h; simpa [sumHist] using h w (by simp)
  | succ n ih =>
    intro w h
    simp only [sumHist]
    refine Finset.sum_congr rfl (fun d _ => ih (d :: w) (fun u hu => h u (by simp at hu; omega)))

theorem sumHist_mono (F G : List Dir → ℝ) :
    ∀ n w, (∀ u : List Dir, u.length = w.length + n → F u ≤ G u) → sumHist F n w ≤ sumHist G n w := by
  intro n
  induction n with
  | zero => intro w h; simpa [sumHist] using h w (by simp)
  | succ n ih =>
    intro w h
    simp only [sumHist]
    exact Finset.sum_le_sum (fun d _ => ih (d :: w) (fun u hu => h u (by simp at hu; omega)))

theorem sumHist_const_mul (F : List Dir → ℝ) (a : ℝ) :
    ∀ n w, sumHist (fun u => a * F u) n w = a * sumHist F n w := by
  intro n
  induction n with
  | zero => intro w; simp [sumHist]
  | succ n ih => intro w; simp only [sumHist, ih, Finset.mul_sum]

theorem sumHist_zero : ∀ n w, sumHist (fun _ => (0 : ℝ)) n w = 0 := by
  intro n
  induction n with
  | zero => intro w; simp [sumHist]
  | succ n ih => intro w; simp [sumHist, ih]

theorem abs_dispZ_fst_le (w : List Dir) : |(dispZ w).1| ≤ w.length := by
  induction w with
  | nil => simp [dispZ]
  | cons d w ih =>
    have hd : |(vec d).1| ≤ 1 := by fin_cases d <;> simp [vec]
    simp only [dispZ, Prod.fst_add, List.length_cons, Nat.cast_add, Nat.cast_one]
    calc |(vec d).1 + (dispZ w).1| ≤ |(vec d).1| + |(dispZ w).1| := abs_add_le _ _
      _ ≤ 1 + w.length := by linarith
      _ = w.length + 1 := by ring

/-- Une marche du tore de 0 à R e₀ (1 ≤ R ≤ L/2) a au moins R pas. -/
theorem longueur_ge (L R : ℕ) (hR : 1 ≤ R) (hRL : 2 * R ≤ L) (w : List Dir)
    (hw : castT L (dispZ w) = cible L R) : R ≤ w.length := by
  by_contra hlt
  push Not at hlt
  have h1 : ((dispZ w).1 : ZMod L) = ((R : ℤ) : ZMod L) := by
    have := congrArg Prod.fst hw
    simpa [castT, cible] using this
  rw [ZMod.intCast_eq_intCast_iff_dvd_sub] at h1
  obtain ⟨k, hk⟩ := h1
  have hb := abs_dispZ_fst_le w
  have hlt' : (w.length : ℤ) < R := by exact_mod_cast hlt
  have hD : |(dispZ w).1| < R := lt_of_le_of_lt hb hlt'
  rw [abs_lt] at hD
  have hL : (2 * R : ℤ) ≤ L := by exact_mod_cast hRL
  -- R - D ∈ (0, 2R) ⊂ (0, L] et R - D = L k
  have hpos : 0 < (R : ℤ) - (dispZ w).1 := by linarith
  have hlt2 : (R : ℤ) - (dispZ w).1 < L := by linarith
  have hk' : (R : ℤ) - (dispZ w).1 = L * k := hk
  rcases lt_trichotomy k 0 with hk0 | hk0 | hk0
  · have : (L : ℤ) * k < 0 := by
      apply mul_neg_of_pos_of_neg _ hk0; linarith
    linarith
  · rw [hk0, mul_zero] at hk'; linarith
  · have : (L : ℤ) ≤ L * k := by nlinarith
    linarith

theorem prodVisites_nonneg {α : Type*} [BEq α] [LawfulBEq α] [DecidableEq α] (A : ℕ → ℝ) (hA : ∀ n, 1 ≤ n → 0 < A n)
    (l : List α) : 0 ≤ prodVisites A l := by
  unfold prodVisites
  apply Finset.prod_nonneg
  intro z hz
  exact (hA _ (List.count_pos_iff.mpr (List.mem_toFinset.mp hz))).le

theorem rt_nonneg (A : ℕ → ℝ) (hA : ∀ n, 1 ≤ n → 0 < A n) (N : ℕ) : 0 ≤ rt A N := by
  unfold rt
  split_ifs with h
  · exact (hA 1 le_rfl).le
  · exact div_nonneg (hA N (by omega)).le (hA (N - 1) (by omega)).le

/-! ## 6. Majoration de G̃ (démontrée) -/

/-- **Lemmes 7.1 + 7.2 + §8 (partie marches), démontrés.** Sous un certificat de Perron et la majoration des poids
de pas par une fonction de l'état, `G̃ ≤ ½ K₀ θ^R / (1 − θ)`, `K₀ = (6c/θ)^m (H_max/H_min)`. -/
theorem GtildeA_le (L : ℕ) (hL : 2 ≤ L) (A : ℕ → ℝ) (J : ℝ) (hJ : 0 ≤ J) (R : ℕ) (hR : 1 ≤ R) (hRL : 2 * R ≤ L)
    (hA : ∀ n, 1 ≤ n → 0 < A n) (hA1 : A 1 ≤ 1 / 2)
    (m : ℕ) (hm : 1 ≤ m) (c θ Hmin Hmax : ℝ) (f : List Dir → Dir → ℝ) (H : List Dir → ℝ)
    (hwt : ∀ w d, J * rt A (Ntor L w d) ≤ c)
    (hwin : ∀ w, m ≤ w.length → ∀ d, J * rt A (Ntor L w d) ≤ f (w.take m) d)
    (hf : ∀ s d, 0 ≤ f s d) (hHmin : 0 < Hmin) (hH : ∀ s, s.length = m → Hmin ≤ H s ∧ H s ≤ Hmax)
    (hθ0 : 0 < θ) (hθ1 : θ < 1) (hcθ : θ ≤ 6 * c) (hHH : Hmin ≤ Hmax)
    (hcert : ∀ s, s.length = m → ∑ d, f s d * H (shift m d s) ≤ θ * H s) :
    GtildeA L A J R ≤ ENNReal.ofReal (1 / 2 * ((6 * c / θ) ^ m * (Hmax / Hmin)) * θ ^ R / (1 - θ)) := by
  set K := (6 * c / θ) ^ m * (Hmax / Hmin) with hK
  set wt : List Dir → Dir → ℝ := fun w d => J * rt A (Ntor L w d) with hwtdef
  have hwt' : ∀ w d, 0 ≤ wt w d ∧ wt w d ≤ c := fun w d =>
    ⟨mul_nonneg hJ (rt_nonneg A hA _), hwt w d⟩
  have hG : ∀ n, Gsum wt n [] ≤ K * θ ^ n := fun n =>
    borne_marches_tout_n m hm wt f c θ Hmin Hmax H hwt' hf hwin hHmin hH hθ0 hcθ hHH hcert n
  have hK0 : 0 ≤ K := by
    have hc : 0 ≤ c := (hwt' [] 0).1.trans (hwt' [] 0).2
    exact mul_nonneg (pow_nonneg (div_nonneg (by linarith) hθ0.le) _) (div_nonneg (by linarith) hHmin.le)
  -- terme n : J^n S_n ≤ b n
  set b : ℕ → ℝ := fun n => if R ≤ n then 1 / 2 * K * θ ^ n else 0 with hbdef
  have hterm : ∀ n, J ^ n * sumHist (poidsMarche L A R) n [] ≤ b n := by
    intro n
    by_cases hn : R ≤ n
    · have h1 : sumHist (poidsMarche L A R) n [] ≤ sumHist (fun u => prodVisites A (sitesT L u)) n [] := by
        apply sumHist_mono
        intro u _
        unfold poidsMarche
        split_ifs
        · exact le_rfl
        · exact prodVisites_nonneg A hA _
      have h2 : J ^ n * sumHist (fun u => prodVisites A (sitesT L u)) n []
          = A 1 * Gsum wt n [] := by
        rw [← sumHist_const_mul]
        have : sumHist (fun u => J ^ n * prodVisites A (sitesT L u)) n []
            = sumHist (fun u => A 1 * prodPas wt u) n [] := by
          apply sumHist_congr
          intro u hu
          simp at hu
          rw [prodVisites_sitesT L hL A hA u, ← hu]
          rw [mul_left_comm, prodPas_mul_pow]
        rw [this, sumHist_const_mul, sumHist_prodPas]
        simp [prodPas]
      have hJn : 0 ≤ J ^ n := pow_nonneg hJ n
      calc J ^ n * sumHist (poidsMarche L A R) n []
          ≤ J ^ n * sumHist (fun u => prodVisites A (sitesT L u)) n [] := mul_le_mul_of_nonneg_left h1 hJn
        _ = A 1 * Gsum wt n [] := h2
        _ ≤ 1 / 2 * (K * θ ^ n) := by
            apply mul_le_mul hA1 (hG n) (Gsum_nonneg wt (fun w d => (hwt' w d).1) n []) (by norm_num)
        _ = b n := by simp [hbdef, hn]; ring
    · have h0 : sumHist (poidsMarche L A R) n [] = sumHist (fun _ => (0 : ℝ)) n [] := by
        apply sumHist_congr
        intro u hu
        simp at hu
        unfold poidsMarche
        split_ifs with hc
        · exact absurd (longueur_ge L R hR hRL u hc) (by omega)
        · rfl
      rw [h0, sumHist_zero]
      simp [hbdef, hn]
  -- série géométrique
  have hb0 : ∀ n, 0 ≤ b n := by
    intro n; simp only [hbdef]; split_ifs
    · positivity
    · exact le_rfl
  have hsum : HasSum b (1 / 2 * K * θ ^ R / (1 - θ)) := by
    rw [← hasSum_nat_add_iff' R]
    have hz : ∑ i ∈ Finset.range R, b i = 0 := by
      apply Finset.sum_eq_zero
      intro i hi
      simp only [Finset.mem_range] at hi
      simp [hbdef, show ¬ R ≤ i by omega]
    rw [hz, sub_zero]
    have hg := (hasSum_geometric_of_lt_one hθ0.le hθ1).mul_left (1 / 2 * K * θ ^ R)
    convert hg using 1
    · funext k
      simp only [hbdef, show R ≤ k + R by omega, ite_true]
      rw [pow_add]; ring
    · rw [div_eq_mul_inv]
  calc GtildeA L A J R = ∑' n, ENNReal.ofReal (J ^ n * sumHist (poidsMarche L A R) n []) := rfl
    _ ≤ ∑' n, ENNReal.ofReal (b n) := ENNReal.tsum_le_tsum (fun n => ENNReal.ofReal_le_ofReal (hterm n))
    _ = ENNReal.ofReal (∑' n, b n) := (ENNReal.ofReal_tsum_of_nonneg hb0 hsum.summable).symm
    _ = ENNReal.ofReal (1 / 2 * K * θ ^ R / (1 - θ)) := by rw [hsum.tsum_eq]

/-! ## 7. Le théorème (conditionnel) -/

/-- **Théorème générique conditionnel.** Pour toute mémoire `m`, tout `J*`, tous poids `p/Q` décroissants et tout
certificat de Perron `CertificatPerron m p Q A B Hmin Hmax`, sous `HypothesesBS J* p Q` :
`|⟨W_{R×T}⟩_{L,β}| ≤ (K₀/(1 − θ))^T θ^{RT}` avec `θ = J* A/B`, `K₀ = (6 r̄(1)/ρ')^m H_max/H_min`. -/
theorem loi_aire_conditionnelle (m : ℕ) (hm : 1 ≤ m) (Jstar : ℝ) (hJ0 : 0 < Jstar) (p : List ℕ)
    (Q A B Hmin Hmax : ℕ) (hQ : 0 < Q) (hB : 0 < B) (hA : 0 < A) (hHmin : 0 < Hmin) (hHH : Hmin ≤ Hmax)
    (hp : ∀ N N', 1 ≤ N' → N' ≤ N → pval p N ≤ pval p N')
    (hθ1 : Jstar * ((A : ℝ) / B) < 1) (hcθ : (A : ℝ) / B ≤ 6 * ((pval p 1 : ℝ) / Q))
    (hyp : HypothesesBS Jstar p Q) (cert : CertificatPerron m p Q A B Hmin Hmax)
    (L : ℕ) [NeZero L] (hL : 3 ≤ L) (β : ℝ) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 2 * Jstar) (R T : ℕ)
    (hR : 1 ≤ R) (hRL : 2 * R ≤ L) (hT : 1 ≤ T) (hTL : T + 1 ≤ L) :
    |wilson L β R T| ≤
      (((6 * ((pval p 1 : ℝ) / Q) / ((A : ℝ) / B)) ^ m * ((Hmax : ℝ) / Hmin)) / (1 - Jstar * ((A : ℝ) / B))) ^ T *
        (Jstar * ((A : ℝ) / B)) ^ (R * T) := by
  obtain ⟨H, hHb, hHc⟩ := cert
  set θ : ℝ := Jstar * ((A : ℝ) / B) with hθdef
  set c : ℝ := Jstar * ((pval p 1 : ℝ) / Q) with hcdef
  set J : ℝ := β / 2 with hJdef
  have hJ0' : 0 ≤ J := by positivity
  have hJ1 : J ≤ Jstar := by linarith
  have hQ' : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hB' : (0 : ℝ) < B := by exact_mod_cast hB
  have hA' : (0 : ℝ) < A := by exact_mod_cast hA
  have hθ0 : 0 < θ := by positivity
  have hApos : ∀ n, 1 ≤ n → 0 < Atilde J n := fun n _ => Poids.Atilde_pos J n
  -- domination des poids de pas
  have hdom : ∀ N N', 1 ≤ N' → N' ≤ N → J * rt (Atilde J) N ≤ Jstar * ((pval p N' : ℝ) / Q) := by
    intro N N' h1 h2
    calc J * rt (Atilde J) N ≤ Jstar * rt (Atilde Jstar) N := hyp.monotonie J hJ0' hJ1 N (by omega)
      _ ≤ Jstar * ((pval p N : ℝ) / Q) :=
          mul_le_mul_of_nonneg_left (hyp.poids_certifies N (by omega)) hJ0.le
      _ ≤ Jstar * ((pval p N' : ℝ) / Q) := by
          apply mul_le_mul_of_nonneg_left _ hJ0.le
          apply div_le_div_of_nonneg_right _ hQ'.le
          exact_mod_cast hp N N' h1 h2
  have hNtor1 : ∀ w d, 1 ≤ Ntor L w d := fun w d => by unfold Ntor; omega
  set f : List Dir → Dir → ℝ := fun s d => Jstar * ((pval p (Nwin m s d) : ℝ) / Q) with hfdef
  have hG := GtildeA_le L (by omega) (Atilde J) J hJ0' R hR hRL hApos (Poids.Atilde_one_le J) m hm c θ
    (Hmin : ℝ) (Hmax : ℝ) f H
    (fun w d => hdom (Ntor L w d) 1 le_rfl (hNtor1 w d))
    (fun w hw d => by
      have := hdom (Ntor L w d) (Nwin m w d) (one_le_Nwin m w d) (Nwin_le_Ntor L m w d)
      simpa [hfdef, Nwin_take] using this)
    (fun s d => by positivity) (by exact_mod_cast hHmin) hHb hθ0 hθ1
    (by rw [hθdef, hcdef]; nlinarith) (by exact_mod_cast hHH)
    (fun s hs => by
      have h := hHc s hs
      have e : ∑ d, f s d * H (shift m d s) = Jstar * ∑ d, rbar p Q (Nwin m s d) * H (shift m d s) := by
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl (fun d _ => ?_)
        simp [hfdef, rbar]; ring
      rw [e, hθdef, mul_assoc]
      exact mul_le_mul_of_nonneg_left h hJ0.le)
  have hred := hyp.reduction L hL β hβ0 hβ1 R T hR hRL hT hTL
  -- conclusion réelle
  set K : ℝ := (6 * c / θ) ^ m * ((Hmax : ℝ) / Hmin) with hKdef
  have hc0 : 0 ≤ c := by rw [hcdef]; positivity
  have hHmin' : (0 : ℝ) < Hmin := by exact_mod_cast hHmin
  have hK0 : 0 ≤ K := mul_nonneg (pow_nonneg (div_nonneg (by linarith) hθ0.le) _) (div_nonneg (by positivity) hHmin'.le)
  have hg0 : 0 ≤ 1 / 2 * K * θ ^ R / (1 - θ) := by
    have : 0 < 1 - θ := by linarith
    positivity
  have key : ENNReal.ofReal |wilson L β R T| ≤ ENNReal.ofReal ((K * θ ^ R / (1 - θ)) ^ T) := by
    calc ENNReal.ofReal |wilson L β R T| ≤ 2 ^ T * Gtilde L J R ^ T := hred
      _ ≤ 2 ^ T * ENNReal.ofReal (1 / 2 * K * θ ^ R / (1 - θ)) ^ T := by
          gcongr
          exact hG
      _ = ENNReal.ofReal ((K * θ ^ R / (1 - θ)) ^ T) := by
          rw [← ENNReal.ofReal_pow hg0, show (2 : ENNReal) ^ T = ENNReal.ofReal (2 ^ T) by
            rw [ENNReal.ofReal_pow (by norm_num)]; simp]
          rw [← ENNReal.ofReal_mul (by positivity), ← mul_pow]
          congr 2
          ring
  have hX : 0 ≤ (K * θ ^ R / (1 - θ)) ^ T := by
    have : 0 < 1 - θ := by linarith
    positivity
  have h := (ENNReal.ofReal_le_ofReal_iff hX).mp key
  have e6 : 6 * c / θ = 6 * ((pval p 1 : ℝ) / Q) / ((A : ℝ) / B) := by
    rw [hcdef, hθdef]; field_simp
  calc |wilson L β R T| ≤ (K * θ ^ R / (1 - θ)) ^ T := h
    _ = (K / (1 - θ)) ^ T * θ ^ (R * T) := by rw [div_pow, mul_pow, pow_mul, div_pow]; ring
    _ = _ := by rw [hKdef, e6]

/-- **Théorème 1 (β ≤ 0,81348, m = 11), conditionnel** à `HypothesesBS` (analyse, admise) et à `CertificatM11`
(établi par l'exécutable compilé `verifcert` sur les 6¹¹ états bruts ; pas par le noyau). -/
theorem theoreme1_conditionnel (hyp : HypothesesBS (40674 / 100000) p_m11 (2 ^ 40)) (cert : CertificatM11)
    (L : ℕ) [NeZero L] (hL : 3 ≤ L) (β : ℝ) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 81348 / 100000) (R T : ℕ)
    (hR : 1 ≤ R) (hRL : 2 * R ≤ L) (hT : 1 ≤ T) (hTL : T + 1 ≤ L) :
    |wilson L β R T| ≤ (C11 : ℝ) ^ T * (theta11 : ℝ) ^ (R * T) := by
  have hp : ∀ N N', 1 ≤ N' → N' ≤ N → pval p_m11 N ≤ pval p_m11 N' := by
    intro N N' h1 h2
    have hl : p_m11.length = 13 := rfl
    unfold pval
    rw [hl]
    have := p_m11_decroissants ⟨min N 13 - 1, by omega⟩ ⟨min N' 13 - 1, by omega⟩ (by simp; omega)
    simpa using this
  have h := loi_aire_conditionnelle 11 (by norm_num) (40674 / 100000) (by norm_num) p_m11 (2 ^ 40) A_m11 B_m11
    Hmin_m11 Hmax_m11 (by norm_num) (by norm_num [B_m11]) (by norm_num [A_m11]) (by norm_num [Hmin_m11])
    (by norm_num [Hmin_m11, Hmax_m11]) hp
    (by norm_num [A_m11, B_m11]) (by norm_num [A_m11, B_m11, pval, p_m11]) hyp cert L hL β hβ0
    (by linarith) R T hR hRL hT hTL
  have e1 : ((40674 / 100000 : ℝ) * ((A_m11 : ℝ) / B_m11)) = (theta11 : ℝ) := by
    norm_num [theta11, A_m11, B_m11]
  have e2 : ((6 * ((pval p_m11 1 : ℝ) / (2 ^ 40 : ℕ)) / ((A_m11 : ℝ) / B_m11)) ^ 11 *
      ((Hmax_m11 : ℝ) / Hmin_m11)) / (1 - (40674 / 100000 : ℝ) * ((A_m11 : ℝ) / B_m11)) = (C11 : ℝ) := by
    norm_num [C11, K11, q11, theta11, pval, p_m11, A_m11, B_m11, Hmin_m11, Hmax_m11]
  rw [e2, e1] at h
  exact h

/-- **Jonction exécution compilée ↔ noyau.** Pour TOUTE fonction `Hof` telle que
`verifiePar 2 11 p_m11 (2^40) A_m11 B_m11 Hmin_m11 Hmax_m11 Hof = true` (c'est exactement le booléen calculé et
affiché par l'exécutable `verifcert`), la loi d'aire du théorème 1 vaut sous `HypothesesBS`. -/
theorem theoreme1_de_verifiePar (Hof : List Dir → ℕ)
    (hexec : verifiePar 2 11 p_m11 (2 ^ 40) A_m11 B_m11 Hmin_m11 Hmax_m11 Hof = true)
    (hyp : HypothesesBS (40674 / 100000) p_m11 (2 ^ 40))
    (L : ℕ) [NeZero L] (hL : 3 ≤ L) (β : ℝ) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 81348 / 100000) (R T : ℕ)
    (hR : 1 ≤ R) (hRL : 2 * R ≤ L) (hT : 1 ≤ T) (hTL : T + 1 ≤ L) :
    |wilson L β R T| ≤ (C11 : ℝ) ^ T * (theta11 : ℝ) ^ (R * T) :=
  theoreme1_conditionnel hyp
    (certificat_of_verifiePar 2 11 (by norm_num) p_m11 (2 ^ 40) A_m11 B_m11 Hmin_m11 Hmax_m11 (by norm_num)
      (by norm_num [B_m11]) Hof hexec)
    L hL β hβ0 hβ1 R T hR hRL hT hTL

/-- **Variante m = 5 (β ≤ 0,80438)** : la partie combinatoire ET le certificat sont vérifiés par le noyau ; seule
`HypothesesBS` (l'analyse) est admise. -/
theorem theoreme_m5_conditionnel (hyp : HypothesesBS (40219 / 100000) p_m5 (2 ^ 40))
    (L : ℕ) [NeZero L] (hL : 3 ≤ L) (β : ℝ) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 80438 / 100000) (R T : ℕ)
    (hR : 1 ≤ R) (hRL : 2 * R ≤ L) (hT : 1 ≤ T) (hTL : T + 1 ≤ L) :
    |wilson L β R T| ≤
      (((6 * ((pval p_m5 1 : ℝ) / (2 ^ 40 : ℕ)) / ((A_m5 : ℝ) / B_m5)) ^ 5 * ((Hmax_m5 : ℝ) / Hmin_m5)) /
        (1 - (40219 / 100000 : ℝ) * ((A_m5 : ℝ) / B_m5))) ^ T * ((40219 / 100000 : ℝ) * ((A_m5 : ℝ) / B_m5)) ^ (R * T) := by
  have hp : ∀ N N', 1 ≤ N' → N' ≤ N → pval p_m5 N ≤ pval p_m5 N' := by
    have hdec : ∀ i j : Fin 13, j ≤ i → p_m5.getD i.val 0 ≤ p_m5.getD j.val 0 := by decide
    intro N N' h1 h2
    have hl : p_m5.length = 13 := rfl
    unfold pval
    rw [hl]
    have := hdec ⟨min N 13 - 1, by omega⟩ ⟨min N' 13 - 1, by omega⟩ (by simp; omega)
    simpa using this
  exact loi_aire_conditionnelle 5 (by norm_num) (40219 / 100000) (by norm_num) p_m5 (2 ^ 40) A_m5 B_m5
    Hmin_m5 Hmax_m5 (by norm_num) (by norm_num [B_m5]) (by norm_num [A_m5]) (by norm_num [Hmin_m5])
    (by norm_num [Hmin_m5, Hmax_m5]) hp
    (by norm_num [A_m5, B_m5]) (by norm_num [A_m5, B_m5, pval, p_m5]) hyp certificat_m5 L hL β hβ0
    (by linarith) R T hR hRL hT hTL

end

end LoiAire
