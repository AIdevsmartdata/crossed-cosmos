/-!
# Critère scalaire uniforme ⟹ forme q du trou de ClayYM (piste 1, chantier critere_scalaire_2026-11-11)

Ce fichier est compilé APRÈS les sources ClayYM v1.1 (Basic, OS, Gap, Fake/Trivial, Transfer, GapQ), recopiées
verbatim (imports retirés) en tête de `main.lean` par `assembler.sh`.

Contenu :
* §1  lemme scalaire FIN (p(2n) ≤ 2(eᵖ − 1)²) pour un spectre DÉNOMBRABLE (T-A ne l'avait qu'en spectre fini) ;
* §2  chaîne 4D fine : Δ₄(n) ≤ 2⁻⁹ ⟹ Δ₄(2n) ≤ 256 Δ₄(n)² (T-A : C₄(2⁻⁹) ≤ 247,3 sur papier ; ici 256, en Lean) ;
* §3  itération et trou de transfert : (λ_i/λ₀)ⁿ ≤ 256 Δ₄(n) ≤ 1/2 sur TOUTES les sections (2ᵏn)³ ;
* §4  la même chose en dimension 3 : Δ₃(n) ≤ 2⁻⁷ ⟹ Δ₃(2n) ≤ 64 Δ₃(n)² et (λ_i/λ₀)ⁿ ≤ 64 Δ₃(n) ≤ 1/2 ;
* §5  représentation spectrale de la forme OS (HYPOTHÈSE NOMMÉE `SpecLink`) ⟹ forme q ;
* §6  ASSEMBLAGE : critère uniforme le long d'une suite (filtre) + lien spectral + convergence des formes OS
      ⟹ la limite vérifie `QGapOn … ℓ (256 η)` (même q) ; variante tores carrés ; en termes ClayYM :
      `QGap R S univ ℓ (256 η)` et `HasMassGap R S (−log(256 η)/ℓ)` avec −log(256η)/ℓ ≥ (log 2)/ℓ.

Hypothèses nommées (aucun axiome) : symétrie de log Z (hs12, hs23, hs34) ; `HypSpecTC` (transfert positif à trace) ;
`SpecLink` / `LienTransfert4` (forme OS du cylindre = même transfert) ; `ConvergesOn` (sens exact de « limite ») ;
`OSReconstruction` de ClayYM pour la limite. Rien sur l'unicité de l'état de Gibbs ni de la limite.
-/

namespace CritereScalaire

open Real Filter Topology

/-! ## §1 Lemme scalaire fin, spectre dénombrable -/

/-- Queue excitée `s_n = Σ' r_i^n` (rapports λ_i/λ₀ des états excités). -/
noncomputable def sT (r : ℕ → ℝ) (n : ℕ) : ℝ := ∑' i, r i ^ n

/-- `p(n) = 2 log(1 + s_n) − log(1 + s_{2n})` (λ₀ se simplifie). -/
noncomputable def pT (r : ℕ → ℝ) (n : ℕ) : ℝ :=
  2 * Real.log (1 + sT r n) - Real.log (1 + sT r (2 * n))

lemma summable_pow_mono (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1) {n m : ℕ}
    (hnm : n ≤ m) (hs : Summable (fun i => r i ^ n)) : Summable (fun i => r i ^ m) :=
  Summable.of_nonneg_of_le (fun i => pow_nonneg (h0 i) m)
    (fun i => pow_le_pow_of_le_one (h0 i) (h1 i) hnm) hs

/-- **Lemme fin (spectre dénombrable).** p ≥ 0, chaque r_i^n ≤ s_n ≤ eᵖ − 1, et p(2n) ≤ 2(e^{p(n)} − 1)²,
SANS condition de petitesse. -/
theorem lemme_fin_tc (r : ℕ → ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1) (n : ℕ)
    (hsum : Summable (fun i => r i ^ n)) :
    0 ≤ pT r n ∧ sT r n ≤ Real.exp (pT r n) - 1 ∧ (∀ i, r i ^ n ≤ sT r n) ∧
      pT r (2 * n) ≤ 2 * (Real.exp (pT r n) - 1) ^ 2 := by
  have hsum2 : Summable (fun i => r i ^ (2 * n)) := summable_pow_mono r h0 h1 (by omega) hsum
  have hs : 0 ≤ sT r n := tsum_nonneg (fun i => pow_nonneg (h0 i) n)
  have hs2 : 0 ≤ sT r (2 * n) := tsum_nonneg (fun i => pow_nonneg (h0 i) (2 * n))
  have hs4 : 0 ≤ sT r (2 * (2 * n)) := tsum_nonneg (fun i => pow_nonneg (h0 i) (2 * (2 * n)))
  have h21 : sT r (2 * n) ≤ sT r n :=
    Summable.tsum_le_tsum (fun i => pow_le_pow_of_le_one (h0 i) (h1 i) (by omega)) hsum2 hsum
  have hterm : ∀ j, r j ^ n ≤ sT r n := fun j =>
    hsum.le_tsum j (fun i _ => pow_nonneg (h0 i) n)
  have h2sq : sT r (2 * n) ≤ (sT r n) ^ 2 := by
    calc sT r (2 * n) = ∑' i, r i ^ n * r i ^ n := by
          unfold sT; congr 1; funext i; rw [two_mul, pow_add]
      _ ≤ ∑' i, r i ^ n * sT r n := by
          apply Summable.tsum_le_tsum
          · intro i; exact mul_le_mul_of_nonneg_left (hterm i) (pow_nonneg (h0 i) n)
          · refine hsum2.congr (fun i => ?_); rw [two_mul, pow_add]
          · exact hsum.mul_right _
      _ = (sT r n) ^ 2 := by rw [tsum_mul_right]; unfold sT; ring
  have hpdef : pT r n = 2 * Real.log (1 + sT r n) - Real.log (1 + sT r (2 * n)) := rfl
  have hp2def : pT r (2 * n) =
      2 * Real.log (1 + sT r (2 * n)) - Real.log (1 + sT r (2 * (2 * n))) := rfl
  have hlog1 : Real.log (1 + sT r (2 * n)) ≤ Real.log (1 + sT r n) :=
    Real.log_le_log (by linarith) (by linarith)
  have hl0 : 0 ≤ Real.log (1 + sT r n) := Real.log_nonneg (by linarith)
  have hp_ge : Real.log (1 + sT r n) ≤ pT r n := by rw [hpdef]; linarith
  have hsE : sT r n ≤ Real.exp (pT r n) - 1 := by
    have : 1 + sT r n ≤ Real.exp (pT r n) := by
      calc 1 + sT r n = Real.exp (Real.log (1 + sT r n)) := (Real.exp_log (by linarith)).symm
        _ ≤ Real.exp (pT r n) := Real.exp_le_exp.mpr hp_ge
    linarith
  refine ⟨by linarith, hsE, hterm, ?_⟩
  have e1 : Real.log (1 + sT r (2 * n)) ≤ sT r (2 * n) := by
    have := Real.log_le_sub_one_of_pos (show 0 < 1 + sT r (2 * n) by linarith); linarith
  have e2 : 0 ≤ Real.log (1 + sT r (2 * (2 * n))) := Real.log_nonneg (by linarith)
  have hsq : (sT r n) ^ 2 ≤ (Real.exp (pT r n) - 1) ^ 2 := pow_le_pow_left₀ hs hsE 2
  rw [hp2def]
  nlinarith

/-- Majoration polynomiale : e^x − 1 ≤ x + x² sur [0,1]. -/
lemma expm1_le (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) : Real.exp x - 1 ≤ x + x ^ 2 := by
  have h := Real.abs_exp_sub_one_sub_id_le (x := x) (by rw [abs_of_nonneg h0]; exact h1)
  have := (abs_le.mp h).2
  linarith

lemma expm1_nonneg (x : ℝ) (h0 : 0 ≤ x) : 0 ≤ Real.exp x - 1 := by
  have := Real.add_one_le_exp x; linarith

lemma f_le (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    2 * (Real.exp x - 1) ^ 2 ≤ 2 * (x + x ^ 2) ^ 2 := by
  have := pow_le_pow_left₀ (expm1_nonneg x h0) (expm1_le x h0 h1) 2
  linarith

/-- Pas élémentaire de la chaîne : si `0 ≤ B ≤ c·D`, `D ≤ δ`, `c·δ ≤ 1` et `A ≤ 2(e^B − 1)²`, alors
`A ≤ 2 c²(1 + cδ)² D²`. -/
lemma pas_chaine (A B D c δ : ℝ) (hD0 : 0 ≤ D) (hDδ : D ≤ δ) (hc0 : 0 ≤ c) (hcδ : c * δ ≤ 1)
    (hB0 : 0 ≤ B) (hB : B ≤ c * D) (hA : A ≤ 2 * (Real.exp B - 1) ^ 2) :
    A ≤ 2 * (c * (1 + c * δ)) ^ 2 * D ^ 2 := by
  have hcD : c * D ≤ 1 := le_trans (mul_le_mul_of_nonneg_left hDδ hc0) hcδ
  have hf := f_le B hB0 (le_trans hB hcD)
  have hBB : B ^ 2 ≤ (c * D) * (c * δ) := by
    have h1 : B * B ≤ (c * D) * (c * D) := mul_le_mul hB hB hB0 (by positivity)
    have h2 : (c * D) * (c * D) ≤ (c * D) * (c * δ) :=
      mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hDδ hc0) (by positivity)
    nlinarith
  have hsum : B + B ^ 2 ≤ c * (1 + c * δ) * D := by nlinarith
  have hsq : (B + B ^ 2) ^ 2 ≤ (c * (1 + c * δ) * D) ^ 2 :=
    pow_le_pow_left₀ (by positivity) hsum 2
  have e : (c * (1 + c * δ) * D) ^ 2 = (c * (1 + c * δ)) ^ 2 * D ^ 2 := by ring
  nlinarith

/-! ## §2 Chaîne 4D fine -/

/-- Défaut de doublement dans la 4ᵉ direction. -/
def Q (F : ℕ → ℕ → ℕ → ℕ → ℝ) (a b c d : ℕ) : ℝ := 2 * F a b c d - F a b c (2 * d)

/-- Δ₄(n) = 16 log Z(n⁴) − log Z((2n)⁴). -/
def Delta (F : ℕ → ℕ → ℕ → ℕ → ℝ) (n : ℕ) : ℝ :=
  16 * F n n n n - F (2 * n) (2 * n) (2 * n) (2 * n)

/-- Partie numérique de la chaîne fine 4D : seuil 2⁻⁹, constante 256. -/
lemma chaine_num_fin4 (D B0 B1 B2 B3 A0 A1 A2 A3 : ℝ) (hD0 : 0 ≤ D) (hD : D ≤ 1 / 512)
    (hB0n : 0 ≤ B0) (hB1n : 0 ≤ B1) (hB2n : 0 ≤ B2) (hB3n : 0 ≤ B3)
    (hB0 : B0 ≤ D)
    (hA0 : A0 ≤ 2 * (Real.exp B0 - 1) ^ 2) (hB1 : B1 ≤ 2 * B0 + A0)
    (hA1 : A1 ≤ 2 * (Real.exp B1 - 1) ^ 2) (hB2 : B2 ≤ 2 * B1 + A1)
    (hA2 : A2 ≤ 2 * (Real.exp B2 - 1) ^ 2) (hB3 : B3 ≤ 2 * B2 + A2)
    (hA3 : A3 ≤ 2 * (Real.exp B3 - 1) ^ 2) :
    8 * A0 + 4 * A1 + 2 * A2 + A3 ≤ 256 * D ^ 2 := by
  have hDD : D ^ 2 ≤ D / 512 := by nlinarith
  have a0 := pas_chaine A0 B0 D 1 (1 / 512) hD0 hD (by norm_num) (by norm_num) hB0n (by linarith) hA0
  have a0' : A0 ≤ 2008 / 1000 * D ^ 2 := by
    norm_num at a0
    nlinarith [sq_nonneg D]
  have b1 : B1 ≤ 2004 / 1000 * D := by nlinarith
  have a1 := pas_chaine A1 B1 D (2004 / 1000) (1 / 512) hD0 hD (by norm_num) (by norm_num) hB1n b1 hA1
  have a1' : A1 ≤ 8096 / 1000 * D ^ 2 := by
    norm_num at a1
    nlinarith [sq_nonneg D]
  have b2 : B2 ≤ 4024 / 1000 * D := by nlinarith
  have a2 := pas_chaine A2 B2 D (4024 / 1000) (1 / 512) hD0 hD (by norm_num) (by norm_num) hB2n b2 hA2
  have a2' : A2 ≤ 329 / 10 * D ^ 2 := by
    norm_num at a2
    nlinarith [sq_nonneg D]
  have b3 : B3 ≤ 8113 / 1000 * D := by nlinarith
  have a3 := pas_chaine A3 B3 D (8113 / 1000) (1 / 512) hD0 hD (by norm_num) (by norm_num) hB3n b3 hA3
  have a3' : A3 ≤ 1359 / 10 * D ^ 2 := by
    norm_num at a3
    nlinarith [sq_nonneg D]
  nlinarith

/-- Décomposition (D) et positivité : Δ₄(n) ≥ 0, Q(n⁴) ≤ Δ₄(n)/8, Q(2n,2n,2n | n) ≤ Δ₄(n). -/
theorem decomp_4d (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d)
    (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hpos : ∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d → 0 ≤ Q F a b c d)
    (n : ℕ) (hn : 0 < n) :
    0 ≤ Delta F n ∧ Q F n n n n ≤ Delta F n / 8 ∧ Q F (2 * n) (2 * n) (2 * n) n ≤ Delta F n := by
  have h2 : 0 < 2 * n := by omega
  unfold Q at hpos ⊢
  unfold Delta
  have e1 : F (2 * n) n n n = F n n n (2 * n) := (hs12 (2 * n) n n n).trans ((hs23 n (2 * n) n n).trans ((hs34 n n (2 * n) n)))
  have e2 : F (2 * n) n n (2 * n) = F n n (2 * n) (2 * n) := (hs12 (2 * n) n n (2 * n)).trans ((hs23 n (2 * n) n (2 * n)))
  have e3 : F (2 * n) (2 * n) n n = F n n (2 * n) (2 * n) := (hs23 (2 * n) (2 * n) n n).trans ((hs12 (2 * n) n (2 * n) n).trans ((hs34 n (2 * n) (2 * n) n).trans ((hs23 n (2 * n) n (2 * n)))))
  have e4 : F (2 * n) (2 * n) n (2 * n) = F n (2 * n) (2 * n) (2 * n) := (hs23 (2 * n) (2 * n) n (2 * n)).trans ((hs12 (2 * n) n (2 * n) (2 * n)))
  have e5 : F (2 * n) (2 * n) (2 * n) n = F n (2 * n) (2 * n) (2 * n) := (hs34 (2 * n) (2 * n) (2 * n) n).trans ((hs23 (2 * n) (2 * n) n (2 * n)).trans ((hs12 (2 * n) n (2 * n) (2 * n))))
  have q1 := hpos n n n n hn hn hn hn
  have q2 := hpos (2 * n) n n n h2 hn hn hn
  have q3 := hpos (2 * n) (2 * n) n n h2 h2 hn hn
  have q4 := hpos (2 * n) (2 * n) (2 * n) n h2 h2 h2 hn
  have hdec : 16 * F n n n n - F (2 * n) (2 * n) (2 * n) (2 * n) =
      8 * (2 * F n n n n - F n n n (2 * n)) + 4 * (2 * F (2 * n) n n n - F (2 * n) n n (2 * n)) +
      2 * (2 * F (2 * n) (2 * n) n n - F (2 * n) (2 * n) n (2 * n)) + (2 * F (2 * n) (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n) (2 * n)) := by
    rw [e1, e2, e3, e4, e5]; ring
  refine ⟨?_, ?_, ?_⟩
  · rw [hdec]; linarith
  · rw [hdec]; linarith
  · rw [hdec]; linarith

/-- **Doublement 4D fin** : Δ₄(n) ≤ 2⁻⁹ ⟹ Δ₄(2n) ≤ 256 Δ₄(n)². Hypothèses : symétrie de F = log Z, positivité
du défaut et lemme fin dans la 4ᵉ direction (fournis par `HypSpecTC`). -/
theorem doublement_fin_4d (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d)
    (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hpos : ∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d → 0 ≤ Q F a b c d)
    (hsq : ∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d →
      Q F a b c (2 * d) ≤ 2 * (Real.exp (Q F a b c d) - 1) ^ 2)
    (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :
    Delta F (2 * n) ≤ 256 * (Delta F n) ^ 2 := by
  obtain ⟨hD0, -, hB0⟩ := decomp_4d F hs12 hs23 hs34 hpos n hn
  have h2 : 0 < 2 * n := by omega
  have h4 : 0 < 2 * (2 * n) := by omega
  unfold Q at hpos hsq hB0
  unfold Delta at hD hD0 hB0 ⊢
  have e5 : F (2 * n) (2 * n) (2 * n) n = F n (2 * n) (2 * n) (2 * n) := (hs34 (2 * n) (2 * n) (2 * n) n).trans ((hs23 (2 * n) (2 * n) n (2 * n)).trans ((hs12 (2 * n) n (2 * n) (2 * n))))
  have e6 : F (2 * (2 * n)) (2 * n) (2 * n) n = F n (2 * n) (2 * n) (2 * (2 * n)) := (hs12 (2 * (2 * n)) (2 * n) (2 * n) n).trans ((hs23 (2 * n) (2 * (2 * n)) (2 * n) n).trans ((hs34 (2 * n) (2 * n) (2 * (2 * n)) n).trans ((hs23 (2 * n) (2 * n) n (2 * (2 * n))).trans ((hs12 (2 * n) n (2 * n) (2 * (2 * n)))))))
  have e7 : F (2 * n) (2 * n) (2 * n) (2 * (2 * n)) = F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) := (hs34 (2 * n) (2 * n) (2 * n) (2 * (2 * n))).trans ((hs23 (2 * n) (2 * n) (2 * (2 * n)) (2 * n)).trans ((hs12 (2 * n) (2 * (2 * n)) (2 * n) (2 * n))))
  have e8 : F (2 * (2 * n)) (2 * n) (2 * n) n = F (2 * (2 * n)) n (2 * n) (2 * n) := (hs34 (2 * (2 * n)) (2 * n) (2 * n) n).trans ((hs23 (2 * (2 * n)) (2 * n) n (2 * n)))
  have e9 : F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n = F (2 * (2 * n)) n (2 * n) (2 * (2 * n)) := (hs23 (2 * (2 * n)) (2 * (2 * n)) (2 * n) n).trans ((hs34 (2 * (2 * n)) (2 * n) (2 * (2 * n)) n).trans ((hs23 (2 * (2 * n)) (2 * n) n (2 * (2 * n)))))
  have e10 : F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n)) = F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) := (hs34 (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))).trans ((hs23 (2 * (2 * n)) (2 * n) (2 * (2 * n)) (2 * n)))
  have e11 : F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n = F (2 * (2 * n)) (2 * (2 * n)) n (2 * n) := (hs34 (2 * (2 * n)) (2 * (2 * n)) (2 * n) n)
  have e12 : F (2 * (2 * n)) (2 * (2 * n)) n (2 * (2 * n)) = F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n := (hs34 (2 * (2 * n)) (2 * (2 * n)) n (2 * (2 * n)))
  have e13 : F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n)) = F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) := (hs34 (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n)))
  have xA := hpos n (2 * n) (2 * n) (2 * n) hn h2 h2 h2
  have xB := hpos (2 * (2 * n)) n (2 * n) (2 * n) h4 hn h2 h2
  have xC := hpos (2 * (2 * n)) (2 * (2 * n)) n (2 * n) h4 h4 hn h2
  have hB0n := hpos (2 * n) (2 * n) (2 * n) n h2 h2 h2 hn
  have hB1n := hpos (2 * (2 * n)) (2 * n) (2 * n) n h4 h2 h2 hn
  have hB2n := hpos (2 * (2 * n)) (2 * (2 * n)) (2 * n) n h4 h4 h2 hn
  have hB3n := hpos (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n h4 h4 h4 hn
  have hA0 := hsq (2 * n) (2 * n) (2 * n) n h2 h2 h2 hn
  have hA1 := hsq (2 * (2 * n)) (2 * n) (2 * n) n h4 h2 h2 hn
  have hA2 := hsq (2 * (2 * n)) (2 * (2 * n)) (2 * n) n h4 h4 h2 hn
  have hA3 := hsq (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n h4 h4 h4 hn
  have hD2 : 16 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) =
      8 * (2 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * n) (2 * n) (2 * n) (2 * (2 * n))) + 4 * (2 * F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))) +
      2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n))) + (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n))) := by
    rw [e7, e10, e13]; ring
  have hB1 : 2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) ≤
      2 * (2 * F (2 * n) (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n) (2 * n)) + (2 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * n) (2 * n) (2 * n) (2 * (2 * n))) := by
    have r : 2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) = 2 * (2 * F (2 * n) (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n) (2 * n))
        - 2 * (2 * F n (2 * n) (2 * n) (2 * n) - F n (2 * n) (2 * n) (2 * (2 * n))) + (2 * F (2 * n) (2 * n) (2 * n) (2 * n) - F (2 * n) (2 * n) (2 * n) (2 * (2 * n))) := by
      rw [e5, e6, e7]; ring
    linarith
  have hB2 : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) ≤
      2 * (2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n)) + (2 * F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))) := by
    have r : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) = 2 * (2 * F (2 * (2 * n)) (2 * n) (2 * n) n - F (2 * (2 * n)) (2 * n) (2 * n) (2 * n))
        - 2 * (2 * F (2 * (2 * n)) n (2 * n) (2 * n) - F (2 * (2 * n)) n (2 * n) (2 * (2 * n))) + (2 * F (2 * (2 * n)) (2 * n) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * n) (2 * n) (2 * (2 * n))) := by
      rw [e8, e9, e10]; ring
    linarith
  have hB3 : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) ≤
      2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n)) + (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n))) := by
    have r : 2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * (2 * n)) (2 * n) = 2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) n - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n))
        - 2 * (2 * F (2 * (2 * n)) (2 * (2 * n)) n (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) n (2 * (2 * n))) + (2 * F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * n) - F (2 * (2 * n)) (2 * (2 * n)) (2 * n) (2 * (2 * n))) := by
      rw [e11, e12, e13]; ring
    linarith
  rw [hD2]
  exact chaine_num_fin4 _ _ _ _ _ _ _ _ _ hD0 hD hB0n hB1n hB2n hB3n hB0 hA0 hB1 hA1 hB2 hA2 hB3 hA3

/-! ## §3 Itération et trou de transfert (4D) -/

/-- Itération : si d_{k+1} ≤ 256 d_k² dès que d_k ≤ 2⁻⁹, alors 256 d_k ≤ (256 d₀)^(2^k). -/
theorem iteration256 (d : ℕ → ℝ) (hnn : ∀ k, 0 ≤ d k)
    (hstep : ∀ k, d k ≤ 1 / 512 → d (k + 1) ≤ 256 * d k ^ 2) (h0 : d 0 ≤ 1 / 512) :
    ∀ k, 256 * d k ≤ (256 * d 0) ^ (2 ^ k) := by
  intro k
  induction k with
  | zero => simp
  | succ k ih =>
    have hq : 256 * d 0 ≤ 1 / 2 := by linarith
    have hq0 : 0 ≤ 256 * d 0 := by linarith [hnn 0]
    have hpow : (256 * d 0) ^ (2 ^ k) ≤ 256 * d 0 :=
      pow_le_of_le_one hq0 (by linarith) (by positivity)
    have hdk : d k ≤ 1 / 512 := by linarith
    have h1 := hstep k hdk
    have h2 : (256 * d k) ^ 2 ≤ ((256 * d 0) ^ (2 ^ k)) ^ 2 :=
      pow_le_pow_left₀ (by linarith [hnn k]) ih 2
    calc 256 * d (k + 1) ≤ 256 * (256 * d k ^ 2) := by linarith
      _ = (256 * d k) ^ 2 := by ring
      _ ≤ ((256 * d 0) ^ (2 ^ k)) ^ 2 := h2
      _ = (256 * d 0) ^ (2 ^ (k + 1)) := by rw [← pow_mul, pow_succ]

/-- Structure de transfert à trace dans la 4ᵉ direction, tailles > 0 (identique à P2 `HypSpecTC`). -/
def HypSpecTC (F : ℕ → ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ a b c : ℕ, 0 < a → 0 < b → 0 < c →
    ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
      (∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) ∧
      ∀ d : ℕ, 0 < d → F a b c d = (d : ℝ) * L + Real.log (1 + sT r d)

lemma Q_eq_pT (F : ℕ → ℕ → ℕ → ℕ → ℝ) (a b c : ℕ) (r : ℕ → ℝ) (L : ℝ)
    (hF : ∀ d : ℕ, 0 < d → F a b c d = (d : ℝ) * L + Real.log (1 + sT r d)) (d : ℕ)
    (hd : 0 < d) : Q F a b c d = pT r d := by
  unfold Q pT
  rw [hF d hd, hF (2 * d) (by omega)]
  push_cast
  ring

lemma hyp_of_specTC (F : ℕ → ℕ → ℕ → ℕ → ℝ) (hF : HypSpecTC F) :
    (∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d → 0 ≤ Q F a b c d) ∧
    (∀ a b c d, 0 < a → 0 < b → 0 < c → 0 < d →
      Q F a b c (2 * d) ≤ 2 * (Real.exp (Q F a b c d) - 1) ^ 2) := by
  constructor
  · intro a b c d ha hb hc hd
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b c ha hb hc
    rw [Q_eq_pT F a b c r L hF d hd]
    exact (lemme_fin_tc r h0 h1 d (hs d hd)).1
  · intro a b c d ha hb hc hd
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b c ha hb hc
    rw [Q_eq_pT F a b c r L hF (2 * d) (by omega), Q_eq_pT F a b c r L hF d hd]
    exact (lemme_fin_tc r h0 h1 d (hs d hd)).2.2.2

/-- **Trou de transfert 4D (constantes fines).** Si Δ₄(n) ≤ 2⁻⁹, alors pour tout k, sur la section (2ᵏn)³,
tout rapport excité r_i = λ_i/λ₀ du transfert vérifie r_iⁿ ≤ 256 Δ₄(n) (≤ 1/2), soit un trou ≥ −log(256Δ₄(n))/n. -/
theorem gap_4d_fin (F : ℕ → ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c d, F a b c d = F b a c d)
    (hs23 : ∀ a b c d, F a b c d = F a c b d)
    (hs34 : ∀ a b c d, F a b c d = F a b d c)
    (hF : HypSpecTC F) (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) (k : ℕ)
    (r : ℕ → ℝ) (L : ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1)
    (hs : ∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d))
    (hFm : ∀ d : ℕ, 0 < d →
      F (2 ^ k * n) (2 ^ k * n) (2 ^ k * n) d = (d : ℝ) * L + Real.log (1 + sT r d)) :
    ∀ i, r i ^ n ≤ 256 * Delta F n := by
  obtain ⟨hpos, hsq⟩ := hyp_of_specTC F hF
  have hnn : ∀ k, 0 ≤ Delta F (2 ^ k * n) := fun k =>
    (decomp_4d F hs12 hs23 hs34 hpos _ (by positivity)).1
  have hit : ∀ k, 256 * Delta F (2 ^ k * n) ≤ (256 * Delta F (2 ^ 0 * n)) ^ (2 ^ k) := by
    apply iteration256 (fun k => Delta F (2 ^ k * n)) hnn
    · intro k hk
      have := doublement_fin_4d F hs12 hs23 hs34 hpos hsq _ (by positivity) hk
      have e : 2 ^ (k + 1) * n = 2 * (2 ^ k * n) := by ring
      simp only [e]
      exact this
    · simpa using hD
  have e0 : 2 ^ 0 * n = n := by simp
  rw [e0] at hit
  intro i
  set m := 2 ^ k * n with hm
  have hm0 : 0 < m := by positivity
  have hD0 : 0 ≤ Delta F n := (decomp_4d F hs12 hs23 hs34 hpos n hn).1
  have hq : 256 * Delta F n ≤ 1 / 2 := by linarith
  have hk := hit k
  have hpowle : (256 * Delta F n) ^ (2 ^ k) ≤ 256 * Delta F n :=
    pow_le_of_le_one (by linarith) (by linarith) (by positivity)
  have hDm0 : 0 ≤ Delta F m := hnn k
  have hDm : Delta F m ≤ 1 / 512 := by linarith
  obtain ⟨-, hq8, -⟩ := decomp_4d F hs12 hs23 hs34 hpos m hm0
  have hQ : Q F m m m m = pT r m := Q_eq_pT F m m m r L hFm m hm0
  obtain ⟨hp0, hsE, hterm, -⟩ := lemme_fin_tc r h0 h1 m (hs m hm0)
  have hp : pT r m ≤ Delta F m / 8 := by rw [← hQ]; exact hq8
  have hp1 : pT r m ≤ 1 := by linarith
  have hexp := expm1_le (pT r m) hp0 hp1
  have hpp : pT r m ^ 2 ≤ pT r m := by nlinarith
  have hri : r i ^ m ≤ Delta F m / 4 := by
    have := hterm i; linarith
  have hri' : (r i ^ n) ^ (2 ^ k) ≤ (256 * Delta F n) ^ (2 ^ k) := by
    rw [← pow_mul, mul_comm n (2 ^ k), ← hm]
    linarith
  exact (pow_le_pow_iff_left₀ (pow_nonneg (h0 i) n) (by linarith) (by positivity)).mp hri'

/-! ## §4 Dimension 3 -/

/-- Défaut de doublement dans la 3ᵉ direction. -/
def Q3 (F : ℕ → ℕ → ℕ → ℝ) (a b c : ℕ) : ℝ := 2 * F a b c - F a b (2 * c)

/-- Δ₃(n) = 8 log Z(n³) − log Z((2n)³). -/
def Delta3 (F : ℕ → ℕ → ℕ → ℝ) (n : ℕ) : ℝ := 8 * F n n n - F (2 * n) (2 * n) (2 * n)

lemma chaine_num_fin3 (D B0 B1 B2 A0 A1 A2 : ℝ) (hD0 : 0 ≤ D) (hD : D ≤ 1 / 128)
    (hB0n : 0 ≤ B0) (hB1n : 0 ≤ B1) (hB2n : 0 ≤ B2)
    (hB0 : B0 ≤ D)
    (hA0 : A0 ≤ 2 * (Real.exp B0 - 1) ^ 2) (hB1 : B1 ≤ 2 * B0 + A0)
    (hA1 : A1 ≤ 2 * (Real.exp B1 - 1) ^ 2) (hB2 : B2 ≤ 2 * B1 + A1)
    (hA2 : A2 ≤ 2 * (Real.exp B2 - 1) ^ 2) :
    4 * A0 + 2 * A1 + A2 ≤ 64 * D ^ 2 := by
  have hDD : D ^ 2 ≤ D / 128 := by nlinarith
  have a0 := pas_chaine A0 B0 D 1 (1 / 128) hD0 hD (by norm_num) (by norm_num) hB0n (by linarith) hA0
  have a0' : A0 ≤ 2032 / 1000 * D ^ 2 := by
    norm_num at a0
    nlinarith [sq_nonneg D]
  have b1 : B1 ≤ 2016 / 1000 * D := by nlinarith
  have a1 := pas_chaine A1 B1 D (2016 / 1000) (1 / 128) hD0 hD (by norm_num) (by norm_num) hB1n b1 hA1
  have a1' : A1 ≤ 8387 / 1000 * D ^ 2 := by
    norm_num at a1
    nlinarith [sq_nonneg D]
  have b2 : B2 ≤ 4098 / 1000 * D := by nlinarith
  have a2 := pas_chaine A2 B2 D (4098 / 1000) (1 / 128) hD0 hD (by norm_num) (by norm_num) hB2n b2 hA2
  have a2' : A2 ≤ 3578 / 100 * D ^ 2 := by
    norm_num at a2
    nlinarith [sq_nonneg D]
  nlinarith

theorem decomp_3d (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b)
    (hpos : ∀ a b c, 0 < a → 0 < b → 0 < c → 0 ≤ Q3 F a b c) (n : ℕ) (hn : 0 < n) :
    0 ≤ Delta3 F n ∧ Q3 F n n n ≤ Delta3 F n / 4 ∧ Q3 F (2 * n) (2 * n) n ≤ Delta3 F n := by
  have h2 : 0 < 2 * n := by omega
  unfold Q3 at hpos ⊢
  unfold Delta3
  have e1 : F n n (2 * n) = F n (2 * n) n := hs23 n n (2 * n)
  have e2 : F n (2 * n) (2 * n) = F (2 * n) (2 * n) n :=
    ((hs12 n (2 * n) (2 * n)).trans (hs23 (2 * n) n (2 * n)))
  have q1 := hpos n n n hn hn hn
  have q2 := hpos n (2 * n) n hn h2 hn
  have q3 := hpos (2 * n) (2 * n) n h2 h2 hn
  have hdec : 8 * F n n n - F (2 * n) (2 * n) (2 * n) =
      4 * (2 * F n n n - F n n (2 * n)) + 2 * (2 * F n (2 * n) n - F n (2 * n) (2 * n)) +
      (2 * F (2 * n) (2 * n) n - F (2 * n) (2 * n) (2 * n)) := by
    rw [e1, e2]; ring
  refine ⟨?_, ?_, ?_⟩
  · rw [hdec]; linarith
  · rw [hdec]; linarith
  · rw [hdec]; linarith


/-- Identité de décomposition 3D : Δ₃(n) = 4 Q₃(n,n,n) + 2 Q₃(n,2n,n) + Q₃(2n,2n,n). -/
lemma dec3_eq (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b) (n : ℕ) :
    Delta3 F n = 4 * Q3 F n n n + 2 * Q3 F n (2 * n) n + Q3 F (2 * n) (2 * n) n := by
  unfold Delta3 Q3
  have e1 : F n n (2 * n) = F n (2 * n) n := hs23 n n (2 * n)
  have e2 : F n (2 * n) (2 * n) = F (2 * n) (2 * n) n :=
    ((hs12 n (2 * n) (2 * n)).trans (hs23 (2 * n) n (2 * n)))
  rw [e1, e2]; ring

/-- Transposition (1 3) à partir des transpositions adjacentes. -/
lemma t13 (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b) (a b c : ℕ) :
    F a b c = F c b a :=
  (hs23 a b c).trans ((hs12 a c b).trans (hs23 c a b))

/-- **Doublement 3D fin** : Δ₃(n) ≤ 2⁻⁷ ⟹ Δ₃(2n) ≤ 64 Δ₃(n)². -/
theorem doublement_fin_3d (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b)
    (hpos : ∀ a b c, 0 < a → 0 < b → 0 < c → 0 ≤ Q3 F a b c)
    (hsq : ∀ a b c, 0 < a → 0 < b → 0 < c →
      Q3 F a b (2 * c) ≤ 2 * (Real.exp (Q3 F a b c) - 1) ^ 2)
    (n : ℕ) (hn : 0 < n) (hD : Delta3 F n ≤ 1 / 128) :
    Delta3 F (2 * n) ≤ 64 * (Delta3 F n) ^ 2 := by
  obtain ⟨hD0, -, hB0⟩ := decomp_3d F hs12 hs23 hpos n hn
  have h2 : 0 < 2 * n := by omega
  have h4 : 0 < 2 * (2 * n) := by omega
  have hB0n := hpos (2 * n) (2 * n) n h2 h2 hn
  have hB1n := hpos (2 * (2 * n)) (2 * n) n h4 h2 hn
  have hB2n := hpos (2 * (2 * n)) (2 * (2 * n)) n h4 h4 hn
  have hX := hpos n (2 * n) (2 * n) hn h2 h2
  have hY := hpos (2 * (2 * n)) n (2 * n) h4 hn h2
  have hA0 := hsq (2 * n) (2 * n) n h2 h2 hn
  have hA1 := hsq (2 * (2 * n)) (2 * n) n h4 h2 hn
  have hA2 := hsq (2 * (2 * n)) (2 * (2 * n)) n h4 h4 hn
  have s1 : F (2 * n) (2 * n) n = F n (2 * n) (2 * n) :=
    ((hs12 n (2 * n) (2 * n)).trans (hs23 (2 * n) n (2 * n))).symm
  have hB1 : Q3 F (2 * (2 * n)) (2 * n) n ≤
      2 * Q3 F (2 * n) (2 * n) n + Q3 F (2 * n) (2 * n) (2 * n) := by
    have r : Q3 F (2 * (2 * n)) (2 * n) n =
        2 * Q3 F (2 * n) (2 * n) n - 2 * Q3 F n (2 * n) (2 * n) + Q3 F (2 * n) (2 * n) (2 * n) := by
      unfold Q3
      rw [s1, t13 F hs12 hs23 n (2 * n) (2 * (2 * n)), t13 F hs12 hs23 (2 * n) (2 * n) (2 * (2 * n))]
      ring
    linarith
  have hB2 : Q3 F (2 * (2 * n)) (2 * (2 * n)) n ≤
      2 * Q3 F (2 * (2 * n)) (2 * n) n + Q3 F (2 * (2 * n)) (2 * n) (2 * n) := by
    have r : Q3 F (2 * (2 * n)) (2 * (2 * n)) n =
        2 * Q3 F (2 * (2 * n)) (2 * n) n - 2 * Q3 F (2 * (2 * n)) n (2 * n) +
          Q3 F (2 * (2 * n)) (2 * n) (2 * n) := by
      unfold Q3
      rw [hs23 (2 * (2 * n)) (2 * n) n, hs23 (2 * (2 * n)) n (2 * (2 * n)),
        hs23 (2 * (2 * n)) (2 * n) (2 * (2 * n))]
      ring
    linarith
  have hdec2 := dec3_eq F hs12 hs23 (2 * n)
  have hA1eq : Q3 F (2 * n) (2 * (2 * n)) (2 * n) = Q3 F (2 * (2 * n)) (2 * n) (2 * n) := by
    unfold Q3
    rw [hs12 (2 * n) (2 * (2 * n)) (2 * n), hs12 (2 * n) (2 * (2 * n)) (2 * (2 * n))]
  rw [hdec2, hA1eq]
  exact chaine_num_fin3 _ _ _ _ _ _ _ hD0 hD hB0n hB1n hB2n hB0 hA0 hB1 hA1 hB2 hA2

theorem iteration64 (d : ℕ → ℝ) (hnn : ∀ k, 0 ≤ d k)
    (hstep : ∀ k, d k ≤ 1 / 128 → d (k + 1) ≤ 64 * d k ^ 2) (h0 : d 0 ≤ 1 / 128) :
    ∀ k, 64 * d k ≤ (64 * d 0) ^ (2 ^ k) := by
  intro k
  induction k with
  | zero => simp
  | succ k ih =>
    have hq : 64 * d 0 ≤ 1 / 2 := by linarith
    have hq0 : 0 ≤ 64 * d 0 := by linarith [hnn 0]
    have hpow : (64 * d 0) ^ (2 ^ k) ≤ 64 * d 0 :=
      pow_le_of_le_one hq0 (by linarith) (by positivity)
    have hdk : d k ≤ 1 / 128 := by linarith
    have h1 := hstep k hdk
    have h2 : (64 * d k) ^ 2 ≤ ((64 * d 0) ^ (2 ^ k)) ^ 2 :=
      pow_le_pow_left₀ (by linarith [hnn k]) ih 2
    calc 64 * d (k + 1) ≤ 64 * (64 * d k ^ 2) := by linarith
      _ = (64 * d k) ^ 2 := by ring
      _ ≤ ((64 * d 0) ^ (2 ^ k)) ^ 2 := h2
      _ = (64 * d 0) ^ (2 ^ (k + 1)) := by rw [← pow_mul, pow_succ]

/-- Structure de transfert à trace dans la 3ᵉ direction (sections a × b). -/
def HypSpecTC3 (F : ℕ → ℕ → ℕ → ℝ) : Prop :=
  ∀ a b : ℕ, 0 < a → 0 < b →
    ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
      (∀ c : ℕ, 0 < c → Summable (fun i => r i ^ c)) ∧
      ∀ c : ℕ, 0 < c → F a b c = (c : ℝ) * L + Real.log (1 + sT r c)

lemma Q3_eq_pT (F : ℕ → ℕ → ℕ → ℝ) (a b : ℕ) (r : ℕ → ℝ) (L : ℝ)
    (hF : ∀ c : ℕ, 0 < c → F a b c = (c : ℝ) * L + Real.log (1 + sT r c)) (c : ℕ)
    (hc : 0 < c) : Q3 F a b c = pT r c := by
  unfold Q3 pT
  rw [hF c hc, hF (2 * c) (by omega)]
  push_cast
  ring

lemma hyp_of_specTC3 (F : ℕ → ℕ → ℕ → ℝ) (hF : HypSpecTC3 F) :
    (∀ a b c, 0 < a → 0 < b → 0 < c → 0 ≤ Q3 F a b c) ∧
    (∀ a b c, 0 < a → 0 < b → 0 < c →
      Q3 F a b (2 * c) ≤ 2 * (Real.exp (Q3 F a b c) - 1) ^ 2) := by
  constructor
  · intro a b c ha hb hc
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b ha hb
    rw [Q3_eq_pT F a b r L hF c hc]
    exact (lemme_fin_tc r h0 h1 c (hs c hc)).1
  · intro a b c ha hb hc
    obtain ⟨r, L, h0, h1, hs, hF⟩ := hF a b ha hb
    rw [Q3_eq_pT F a b r L hF (2 * c) (by omega), Q3_eq_pT F a b r L hF c hc]
    exact (lemme_fin_tc r h0 h1 c (hs c hc)).2.2.2

/-- **Trou de transfert 3D.** Δ₃(n) ≤ 2⁻⁷ ⟹ sur toute section (2ᵏn)², r_iⁿ ≤ 64 Δ₃(n) ≤ 1/2. -/
theorem gap_3d_fin (F : ℕ → ℕ → ℕ → ℝ)
    (hs12 : ∀ a b c, F a b c = F b a c) (hs23 : ∀ a b c, F a b c = F a c b)
    (hF : HypSpecTC3 F) (n : ℕ) (hn : 0 < n) (hD : Delta3 F n ≤ 1 / 128) (k : ℕ)
    (r : ℕ → ℝ) (L : ℝ) (h0 : ∀ i, 0 ≤ r i) (h1 : ∀ i, r i ≤ 1)
    (hs : ∀ c : ℕ, 0 < c → Summable (fun i => r i ^ c))
    (hFm : ∀ c : ℕ, 0 < c →
      F (2 ^ k * n) (2 ^ k * n) c = (c : ℝ) * L + Real.log (1 + sT r c)) :
    ∀ i, r i ^ n ≤ 64 * Delta3 F n := by
  obtain ⟨hpos, hsq⟩ := hyp_of_specTC3 F hF
  have hnn : ∀ k, 0 ≤ Delta3 F (2 ^ k * n) := fun k =>
    (decomp_3d F hs12 hs23 hpos _ (by positivity)).1
  have hit : ∀ k, 64 * Delta3 F (2 ^ k * n) ≤ (64 * Delta3 F (2 ^ 0 * n)) ^ (2 ^ k) := by
    apply iteration64 (fun k => Delta3 F (2 ^ k * n)) hnn
    · intro k hk
      have := doublement_fin_3d F hs12 hs23 hpos hsq _ (by positivity) hk
      have e : 2 ^ (k + 1) * n = 2 * (2 ^ k * n) := by ring
      simp only [e]
      exact this
    · simpa using hD
  have e0 : 2 ^ 0 * n = n := by simp
  rw [e0] at hit
  intro i
  set m := 2 ^ k * n with hm
  have hm0 : 0 < m := by positivity
  have hD0 : 0 ≤ Delta3 F n := (decomp_3d F hs12 hs23 hpos n hn).1
  have hk := hit k
  have hpowle : (64 * Delta3 F n) ^ (2 ^ k) ≤ 64 * Delta3 F n :=
    pow_le_of_le_one (by linarith) (by linarith) (by positivity)
  have hDm0 : 0 ≤ Delta3 F m := hnn k
  have hDm : Delta3 F m ≤ 1 / 128 := by linarith
  obtain ⟨-, hq4, -⟩ := decomp_3d F hs12 hs23 hpos m hm0
  have hQ : Q3 F m m m = pT r m := Q3_eq_pT F m m r L hFm m hm0
  obtain ⟨hp0, hsE, hterm, -⟩ := lemme_fin_tc r h0 h1 m (hs m hm0)
  have hp : pT r m ≤ Delta3 F m / 4 := by rw [← hQ]; exact hq4
  have hp1 : pT r m ≤ 1 := by linarith
  have hexp := expm1_le (pT r m) hp0 hp1
  have hpp : pT r m ^ 2 ≤ pT r m := by nlinarith
  have hri : r i ^ m ≤ Delta3 F m / 2 := by
    have := hterm i; linarith
  have hri' : (r i ^ n) ^ (2 ^ k) ≤ (64 * Delta3 F n) ^ (2 ^ k) := by
    rw [← pow_mul, mul_comm n (2 ^ k), ← hm]
    linarith
  exact (pow_le_pow_iff_left₀ (pow_nonneg (h0 i) n) (by linarith) (by positivity)).mp hri'

/-! ## §5 Lien spectral (HYPOTHÈSE NOMMÉE) ⟹ forme q -/

section Spectral

open ClayYM.Transfer

variable {V : Type}

/-- **Hypothèse nommée (W3) : représentation spectrale de la forme OS de réseau** au temps physique `ℓ`
(= `n` pas de réseau). `c F i` = coordonnée du vecteur OS de `F` sur le i-ième vecteur d'une base orthonormée
de vecteurs propres du transfert normalisé `K̂ = K/λ₀` (indice 0 = vide de Perron, indices i+1 = états excités,
de valeurs propres `r i`). Justification : théorème spectral de Hilbert–Schmidt pour `K̂` compact autoadjoint
positif sur `H_inv`, et formule de transfert de la forme OS du cylindre (Lüscher 1977 ; Osterwalder–Seiler 1978). -/
def SpecLink (o : VecOps V) (B : V → V → ℝ → ℝ) (ℓ : ℝ) (r : ℕ → ℝ) (n : ℕ) : Prop :=
  ∃ c : V → ℕ → ℝ,
    (∀ F G i, c (o.add F G) i = c F i + c G i) ∧
    (∀ a F i, c (o.smul a F) i = a * c F i) ∧
    (∀ i, c o.Ω i = 1) ∧
    (∀ F, Summable (fun i => (c F i) ^ 2)) ∧
    (∀ F, B o.Ω F 0 = c F 0) ∧
    (∀ F, B F F 0 = ∑' i, (c F i) ^ 2) ∧
    (∀ F, B F F ℓ = (c F 0) ^ 2 + ∑' i, r i ^ n * (c F (i + 1)) ^ 2)

/-- Lien spectral + rapports excités `r_iⁿ ≤ q` ⟹ forme q de la forme OS, sur tout `𝒜₀`. -/
theorem qGapOn_of_specLink (o : VecOps V) (B : V → V → ℝ → ℝ) {ℓ q : ℝ} (r : ℕ → ℝ) (n : ℕ)
    (hℓ : 0 < ℓ) (hq0 : 0 < q) (hq1 : q < 1) (hr0 : ∀ i, 0 ≤ r i) (hrq : ∀ i, r i ^ n ≤ q)
    (h : SpecLink o B ℓ r n) (𝒜₀ : Set V) : QGapOn o B 𝒜₀ ℓ q := by
  obtain ⟨c, cadd, csmul, cvac, csum, cB0, cdiag0, cdiagℓ⟩ := h
  refine ⟨hℓ, hq0, hq1, fun A _ => ?_⟩
  have hc : ∀ i, c (o.trunc B A) i = c A i + (-(B o.Ω A 0)) * (if i = 0 then 1 else 0) := by
    intro i
    show c (o.add A (o.smul (-(B o.Ω A 0)) o.Ω)) i = _
    rw [cadd, csmul, cvac]
  have hc0 : c (o.trunc B A) 0 = 0 := by rw [hc 0, cB0]; simp
  have hs : Summable (fun i => (c (o.trunc B A) (i + 1)) ^ 2) :=
    (summable_nat_add_iff 1).mpr (csum (o.trunc B A))
  have hle : ∀ i, r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2 ≤ q * (c (o.trunc B A) (i + 1)) ^ 2 :=
    fun i => mul_le_mul_of_nonneg_right (hrq i) (sq_nonneg _)
  have hs' : Summable (fun i => r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2) :=
    Summable.of_nonneg_of_le (fun i => mul_nonneg (pow_nonneg (hr0 i) n) (sq_nonneg _)) hle
      (hs.mul_left q)
  have h0 : B (o.trunc B A) (o.trunc B A) 0 = ∑' i, (c (o.trunc B A) (i + 1)) ^ 2 := by
    rw [cdiag0, (csum (o.trunc B A)).tsum_eq_zero_add, hc0]; simp
  rw [cdiagℓ, hc0, h0]
  calc (0 : ℝ) ^ 2 + ∑' i, r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2
      = ∑' i, r i ^ n * (c (o.trunc B A) (i + 1)) ^ 2 := by simp
    _ ≤ ∑' i, q * (c (o.trunc B A) (i + 1)) ^ 2 := Summable.tsum_le_tsum hle hs' (hs.mul_left q)
    _ = q * ∑' i, (c (o.trunc B A) (i + 1)) ^ 2 := tsum_mul_left

/-! ## §6 Assemblage -/

/-- **Hypothèse nommée (W2)+(W3) au rang k, 4D** : sur la section (2^j n)³, le spectre excité `r` du transfert
qui apparaît dans log Z (forme `HypSpecTC`) est celui de la représentation spectrale de la forme OS `B` au temps ℓ
(= n pas). -/
def LienTransfert4 (o : VecOps V) (F : ℕ → ℕ → ℕ → ℕ → ℝ) (n j : ℕ) (B : V → V → ℝ → ℝ) (ℓ : ℝ) : Prop :=
  ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
    (∀ d : ℕ, 0 < d → Summable (fun i => r i ^ d)) ∧
    (∀ d : ℕ, 0 < d → F (2 ^ j * n) (2 ^ j * n) (2 ^ j * n) d = (d : ℝ) * L + Real.log (1 + sT r d)) ∧
    SpecLink o B ℓ r n

/-- Version 3D (sections (2^j n)²). -/
def LienTransfert3 (o : VecOps V) (F : ℕ → ℕ → ℕ → ℝ) (n j : ℕ) (B : V → V → ℝ → ℝ) (ℓ : ℝ) : Prop :=
  ∃ (r : ℕ → ℝ) (L : ℝ), (∀ i, 0 ≤ r i) ∧ (∀ i, r i ≤ 1) ∧
    (∀ c : ℕ, 0 < c → Summable (fun i => r i ^ c)) ∧
    (∀ c : ℕ, 0 < c → F (2 ^ j * n) (2 ^ j * n) c = (c : ℝ) * L + Real.log (1 + sT r c)) ∧
    SpecLink o B ℓ r n

/-- **Théorème (b), forme abstraite, 4D.** Le long d'un filtre non trivial (suite, sous-suite, double limite
volume puis maille), si `sup_k Δ₄^{(k)}(n_k) ≤ η ≤ 2⁻⁹`, si chaque forme OS de réseau `B k` est reliée au
transfert de la section (2^{j_k} n_k)³ (hypothèse nommée) et si les `B k` convergent vers `Blim` sur
𝒜₀ ∪ {Ω} aux temps 0 et ℓ, alors `Blim` vérifie la forme q au temps ℓ avec q = 256η (≤ 1/2), le MÊME pour tous. -/
theorem qGapOn_limite_4d (o : VecOps V) {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c d, F k a b c d = F k b a c d)
    (hs23 : ∀ k a b c d, F k a b c d = F k a c b d)
    (hs34 : ∀ k a b c d, F k a b c d = F k a b d c)
    (hF : ∀ k, HypSpecTC (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 512) (hΔ : ∀ k, Delta (F k) (n k) ≤ η)
    (B : α → V → V → ℝ → ℝ) (hB : ∀ k, IsBilin o (B k)) {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert4 o (F k) (n k) (j k) (B k) ℓ)
    (Blim : V → V → ℝ → ℝ) (hBlim : IsBilin o Blim) (𝒜₀ : Set V)
    (hconv : ConvergesOn L o B Blim 𝒜₀ ℓ) :
    QGapOn o Blim 𝒜₀ ℓ (256 * η) := by
  have hk : ∀ k, QGapOn o (B k) 𝒜₀ ℓ (256 * η) := by
    intro k
    obtain ⟨r, Lk, h0, h1, hs, hFm, hsl⟩ := hlink k
    have hD : Delta (F k) (n k) ≤ 1 / 512 := le_trans (hΔ k) hη
    have hr := gap_4d_fin (F k) (hs12 k) (hs23 k) (hs34 k) (hF k) (n k) (hn k) hD (j k) r Lk h0 h1 hs hFm
    have hrq : ∀ i, r i ^ n k ≤ 256 * η := fun i => le_trans (hr i) (by linarith [hΔ k])
    exact qGapOn_of_specLink o (B k) r (n k) hℓ (by linarith) (by linarith) h0 hrq hsl 𝒜₀
  exact QGapOn.of_tendsto hB hBlim hconv (Eventually.of_forall hk)

/-- **Théorème (b), version 3D** : seuil 2⁻⁷, q = 64η. -/
theorem qGapOn_limite_3d (o : VecOps V) {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c, F k a b c = F k b a c) (hs23 : ∀ k a b c, F k a b c = F k a c b)
    (hF : ∀ k, HypSpecTC3 (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 128) (hΔ : ∀ k, Delta3 (F k) (n k) ≤ η)
    (B : α → V → V → ℝ → ℝ) (hB : ∀ k, IsBilin o (B k)) {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert3 o (F k) (n k) (j k) (B k) ℓ)
    (Blim : V → V → ℝ → ℝ) (hBlim : IsBilin o Blim) (𝒜₀ : Set V)
    (hconv : ConvergesOn L o B Blim 𝒜₀ ℓ) :
    QGapOn o Blim 𝒜₀ ℓ (64 * η) := by
  have hk : ∀ k, QGapOn o (B k) 𝒜₀ ℓ (64 * η) := by
    intro k
    obtain ⟨r, Lk, h0, h1, hs, hFm, hsl⟩ := hlink k
    have hD : Delta3 (F k) (n k) ≤ 1 / 128 := le_trans (hΔ k) hη
    have hr := gap_3d_fin (F k) (hs12 k) (hs23 k) (hF k) (n k) (hn k) hD (j k) r Lk h0 h1 hs hFm
    have hrq : ∀ i, r i ^ n k ≤ 64 * η := fun i => le_trans (hr i) (by linarith [hΔ k])
    exact qGapOn_of_specLink o (B k) r (n k) hℓ (by linarith) (by linarith) h0 hrq hsl 𝒜₀
  exact QGapOn.of_tendsto hB hBlim hconv (Eventually.of_forall hk)

/-- **Variante tores (hypothèse W5)** : si les formes des tores `Btor k` convergent vers `Blim` et ne diffèrent
de celles des cylindres `B k` que par un terme qui tend vers 0 (sur 𝒜₀ ∪ {Ω}, temps 0 et ℓ), alors les
formes des cylindres convergent aussi vers `Blim` : on se ramène au cas précédent. -/
theorem convergesOn_of_proche (o : VecOps V) {α : Type} {L : Filter α}
    (B Btor : α → V → V → ℝ → ℝ) (Blim : V → V → ℝ → ℝ) (𝒜₀ : Set V) {ℓ : ℝ}
    (hproche : ∀ F ∈ insert o.Ω 𝒜₀, ∀ G ∈ insert o.Ω 𝒜₀, ∀ t ∈ ({0, ℓ} : Set ℝ),
      Tendsto (fun k => Btor k F G t - B k F G t) L (𝓝 0))
    (hconv : ConvergesOn L o Btor Blim 𝒜₀ ℓ) : ConvergesOn L o B Blim 𝒜₀ ℓ := by
  intro F hF G hG t ht
  have h := (hconv F hF G hG t ht).sub (hproche F hF G hG t ht)
  simp only [sub_zero, sub_sub_cancel] at h
  exact h

end Spectral

/-! ## §7 En termes ClayYM -/

section Clay

open ClayYM ClayYM.Transfer

lemma log_deux_le {η ℓ : ℝ} (hℓ : 0 < ℓ) (hη0 : 0 < η) (hq : 256 * η ≤ 1 / 2) :
    Real.log 2 / ℓ ≤ -Real.log (256 * η) / ℓ := by
  have h1 : Real.log (256 * η) ≤ Real.log (1 / 2) := Real.log_le_log (by linarith) hq
  have h2 : Real.log (1 / 2) = -Real.log 2 := by rw [one_div, Real.log_inv]
  apply div_le_div_of_nonneg_right _ hℓ.le
  linarith

/-- **Théorème (b) en termes de ClayYM (4D)** : la limite `S` (noyaux de Schwinger de ClayYM sur ℝ⁴) des formes
OS de réseau vérifie `QGap R S univ ℓ (256η)` ; avec l'hypothèse nommée `OSReconstruction R S` et `S [] = 1`,
elle a le trou `HasMassGap R S (−log(256η)/ℓ)`, et −log(256η)/ℓ ≥ (log 2)/ℓ. -/
theorem clay_trou_de_critere_4d {ι : Type} [Fintype ι] (R : CompRep ι 4) (S : Schwinger ι 4)
    {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c d, F k a b c d = F k b a c d)
    (hs23 : ∀ k a b c d, F k a b c d = F k a c b d)
    (hs34 : ∀ k a b c d, F k a b c d = F k a b d c)
    (hF : ∀ k, HypSpecTC (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 512) (hΔ : ∀ k, Delta (F k) (n k) ≤ η)
    (B : α → Family ι 4 → Family ι 4 → ℝ → ℝ) (hB : ∀ k, IsBilin (famOps ι 4) (B k))
    {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert4 (famOps ι 4) (F k) (n k) (j k) (B k) ℓ)
    (hconv : ConvergesOn L (famOps ι 4) B (rpForm R S) Set.univ ℓ)
    (rec : OSReconstruction R S) (hnorm : S [] = 1) :
    QGap R S Set.univ ℓ (256 * η) ∧ HasMassGap R S (-Real.log (256 * η) / ℓ) ∧
      Real.log 2 / ℓ ≤ -Real.log (256 * η) / ℓ := by
  have hq : QGap R S Set.univ ℓ (256 * η) :=
    (qGap_iff_qGapOn R S Set.univ ℓ _).2
      (qGapOn_limite_4d (famOps ι 4) F n j hn hs12 hs23 hs34 hF hη0 hη hΔ B hB hℓ hlink
        (rpForm R S) (rpForm_isBilin R S) Set.univ hconv)
  exact ⟨hq, hq.hasMassGap_univ rec hnorm, log_deux_le hℓ hη0 (by linarith)⟩

/-- **Théorème (b) en termes de ClayYM (3D)** : q = 64η, seuil 2⁻⁷. -/
theorem clay_trou_de_critere_3d {ι : Type} [Fintype ι] (R : CompRep ι 3) (S : Schwinger ι 3)
    {α : Type} {L : Filter α} [L.NeBot]
    (F : α → ℕ → ℕ → ℕ → ℝ) (n j : α → ℕ) (hn : ∀ k, 0 < n k)
    (hs12 : ∀ k a b c, F k a b c = F k b a c) (hs23 : ∀ k a b c, F k a b c = F k a c b)
    (hF : ∀ k, HypSpecTC3 (F k))
    {η : ℝ} (hη0 : 0 < η) (hη : η ≤ 1 / 128) (hΔ : ∀ k, Delta3 (F k) (n k) ≤ η)
    (B : α → Family ι 3 → Family ι 3 → ℝ → ℝ) (hB : ∀ k, IsBilin (famOps ι 3) (B k))
    {ℓ : ℝ} (hℓ : 0 < ℓ)
    (hlink : ∀ k, LienTransfert3 (famOps ι 3) (F k) (n k) (j k) (B k) ℓ)
    (hconv : ConvergesOn L (famOps ι 3) B (rpForm R S) Set.univ ℓ)
    (rec : OSReconstruction R S) (hnorm : S [] = 1) :
    QGap R S Set.univ ℓ (64 * η) ∧ HasMassGap R S (-Real.log (64 * η) / ℓ) := by
  have hq : QGap R S Set.univ ℓ (64 * η) :=
    (qGap_iff_qGapOn R S Set.univ ℓ _).2
      (qGapOn_limite_3d (famOps ι 3) F n j hn hs12 hs23 hF hη0 hη hΔ B hB hℓ hlink
        (rpForm R S) (rpForm_isBilin R S) Set.univ hconv)
  exact ⟨hq, hq.hasMassGap_univ rec hnorm⟩

end Clay

end CritereScalaire
