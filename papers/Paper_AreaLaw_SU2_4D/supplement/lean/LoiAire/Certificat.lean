import LoiAire.Marches

/-!
# (b) Vérificateur de certificat de Perron, prouvé correct

Un certificat est la donnée de : la mémoire `m`, les 13 numérateurs entiers `p = [p_1, …, p_13]` des poids
`r̄(N) = p_{min(N,13)}/Q`, le rayon certifié `ρ' = A/B`, des bornes `H_min ≤ H ≤ H_max`, et une fonction
`Hof : List Dir → ℕ` (valeur de `H` sur chaque état de longueur `m`).

`verifie` teste, pour CHACUN des `6^m` états bruts `s` (aucun argument de symétrie) :
`H_min ≤ H(s) ≤ H_max` et `B · Σ_d p_{Nwin(s,d)} · H(shift d s) ≤ A · Q · H(s)` (entiers exacts).

Théorème `certificat_of_verifie` : si `verifie … = true`, alors `CertificatPerron` (forme réelle) est vrai,
pour N'IMPORTE QUELLE fonction `Hof`. La façon dont `Hof` est calculée (arbre, table d'orbites, fichier binaire
lu à l'exécution) n'intervient donc pas dans la correction.

* Petites mémoires (m = 3, 4, 5) : `verifie … = true` est démontré par `decide +kernel` (noyau de Lean seul).
* m = 11 : la MÊME fonction (version parallèle `verifiePar`, prouvée équivalente) est exécutée par un programme
  compilé (`VerifCert.lean`) ; confiance = compilateur + exécution, pas le noyau.
-/

namespace LoiAire

open Finset

theorem mem_dirs (d : Dir) : d ∈ dirs := by fin_cases d <;> simp [dirs]

/-- Poids réel `r̄(N) = p_{min(N,K)} / Q`. -/
noncomputable def rbar (p : List ℕ) (Q : ℕ) (N : ℕ) : ℝ := (pval p N : ℝ) / Q

theorem pourTous_correct (t : List Dir → Bool) :
    ∀ k acc, pourTous k acc t = true → ∀ u : List Dir, u.length = k → t (acc ++ u) = true := by
  intro k
  induction k with
  | zero =>
    intro acc h u hu
    rw [List.length_eq_zero_iff] at hu
    subst hu
    simpa [pourTous] using h
  | succ k ih =>
    intro acc h u hu
    cases u with
    | nil => simp at hu
    | cons d u =>
      simp only [pourTous, List.all_eq_true] at h
      have := ih (acc ++ [d]) (h d (mem_dirs d)) u (by simpa using hu)
      simpa using this

theorem mem_prefixes : ∀ (k : ℕ) (a : List Dir), a.length = k → a ∈ prefixes k := by
  intro k
  induction k with
  | zero => intro a ha; rw [List.length_eq_zero_iff] at ha; simp [prefixes, ha]
  | succ k ih =>
    intro a ha
    obtain ⟨b, d, rfl⟩ : ∃ b d, a = b ++ [d] := by
      rcases List.eq_nil_or_concat a with h | ⟨b, d, h⟩
      · subst h; simp at ha
      · exact ⟨b, d, by simpa using h⟩
    simp only [prefixes, List.mem_flatMap, List.mem_map]
    exact ⟨b, ih b (by simpa using ha), d, mem_dirs d, rfl⟩

theorem verifiePar_correct (k m : ℕ) (hk : k ≤ m) (p : List ℕ) (Q A B Hmin Hmax : ℕ) (Hof : List Dir → ℕ)
    (h : verifiePar k m p Q A B Hmin Hmax Hof = true) :
    ∀ s : List Dir, s.length = m → testEtat m p Q A B Hmin Hmax Hof s = true := by
  intro s hs
  simp only [verifiePar, List.all_eq_true, List.mem_map] at h
  have ha : s.take k ∈ prefixes k := mem_prefixes k _ (by simp [hs]; omega)
  have h1 := h _ ⟨s.take k, ha, rfl⟩
  have h2 : pourTous (m - k) (s.take k) (testEtat m p Q A B Hmin Hmax Hof) = true := h1
  have := pourTous_correct _ (m - k) (s.take k) h2 (s.drop k) (by simp [hs])
  simpa using this

theorem verifie_correct (m : ℕ) (p : List ℕ) (Q A B Hmin Hmax : ℕ) (Hof : List Dir → ℕ)
    (h : verifie m p Q A B Hmin Hmax Hof = true) :
    ∀ s : List Dir, s.length = m → testEtat m p Q A B Hmin Hmax Hof s = true := by
  intro s hs
  have := pourTous_correct _ m [] h s hs
  simpa using this

theorem sommeEtat_eq (m : ℕ) (p : List ℕ) (Hof : List Dir → ℕ) (s : List Dir) :
    (sommeEtat m p Hof s : ℝ) = ∑ d : Dir, (pval p (Nwin m s d) : ℝ) * (Hof (shift m d s) : ℝ) := by
  simp [sommeEtat, dirs, Fin.sum_univ_six]
  ring

/-- **Certificat de Perron, forme réelle** : il existe `H` avec `H_min ≤ H ≤ H_max` sur les états de
longueur `m` et `T_m H ≤ ρ' H`, où `(T_m H)(s) = Σ_d r̄(Nwin(s,d)) H(shift d s)`, `r̄ = p/Q`, `ρ' = A/B`. -/
def CertificatPerron (m : ℕ) (p : List ℕ) (Q A B Hmin Hmax : ℕ) : Prop :=
  ∃ H : List Dir → ℝ, (∀ s : List Dir, s.length = m → (Hmin : ℝ) ≤ H s ∧ H s ≤ Hmax) ∧
    ∀ s : List Dir, s.length = m → ∑ d : Dir, rbar p Q (Nwin m s d) * H (shift m d s) ≤ ((A : ℝ) / B) * H s

theorem certificat_of_tests (m : ℕ) (p : List ℕ) (Q A B Hmin Hmax : ℕ) (hQ : 0 < Q) (hB : 0 < B)
    (Hof : List Dir → ℕ) (h : ∀ s : List Dir, s.length = m → testEtat m p Q A B Hmin Hmax Hof s = true) :
    CertificatPerron m p Q A B Hmin Hmax := by
  refine ⟨fun s => (Hof s : ℝ), ?_, ?_⟩
  · intro s hs
    have := h s hs
    simp only [testEtat, Bool.and_eq_true, Nat.ble_eq] at this
    exact ⟨by simpa using (show (Hmin : ℝ) ≤ Hof s by exact_mod_cast this.1.1),
           by simpa using (show (Hof s : ℝ) ≤ Hmax by exact_mod_cast this.1.2)⟩
  · intro s hs
    have := h s hs
    simp only [testEtat, Bool.and_eq_true, Nat.ble_eq] at this
    have key : (B : ℝ) * (sommeEtat m p Hof s : ℝ) ≤ (A : ℝ) * Q * (Hof s : ℝ) := by exact_mod_cast this.2
    rw [sommeEtat_eq] at key
    have hQ' : (0 : ℝ) < Q := by exact_mod_cast hQ
    have hB' : (0 : ℝ) < B := by exact_mod_cast hB
    have e : ∑ d : Dir, rbar p Q (Nwin m s d) * (Hof (shift m d s) : ℝ)
        = (∑ d : Dir, (pval p (Nwin m s d) : ℝ) * (Hof (shift m d s) : ℝ)) / Q := by
      rw [Finset.sum_div]
      refine Finset.sum_congr rfl (fun d _ => ?_)
      simp [rbar]; ring
    rw [e, div_le_iff₀ hQ']
    have e2 : (A : ℝ) / B * (Hof s : ℝ) * Q = (A * Q * Hof s) / B := by field_simp
    rw [e2, le_div_iff₀ hB']
    linarith [key]

theorem certificat_of_verifie (m : ℕ) (p : List ℕ) (Q A B Hmin Hmax : ℕ) (hQ : 0 < Q) (hB : 0 < B)
    (Hof : List Dir → ℕ) (h : verifie m p Q A B Hmin Hmax Hof = true) :
    CertificatPerron m p Q A B Hmin Hmax :=
  certificat_of_tests m p Q A B Hmin Hmax hQ hB Hof (verifie_correct m p Q A B Hmin Hmax Hof h)

theorem certificat_of_verifiePar (k m : ℕ) (hk : k ≤ m) (p : List ℕ) (Q A B Hmin Hmax : ℕ) (hQ : 0 < Q)
    (hB : 0 < B) (Hof : List Dir → ℕ) (h : verifiePar k m p Q A B Hmin Hmax Hof = true) :
    CertificatPerron m p Q A B Hmin Hmax :=
  certificat_of_tests m p Q A B Hmin Hmax hQ hB Hof (verifiePar_correct k m hk p Q A B Hmin Hmax Hof h)

end LoiAire
