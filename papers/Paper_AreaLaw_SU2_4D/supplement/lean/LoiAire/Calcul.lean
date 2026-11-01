/-!
# Fonctions calculatoires (sans Mathlib)

Ce module n'importe que le cœur de Lean : il est partagé par la bibliothèque (preuves, Mathlib) et par
l'exécutable `verifcert` (qui ne doit pas lier Mathlib). Les énoncés de correction sont dans `Marches.lean`
et `Certificat.lean`.

Représentation : un historique (ou un état) est une liste de pas, le PLUS RÉCENT EN TÊTE.
-/

namespace LoiAire

/-- Les 6 directions de ℤ³ : 0:+e₀, 1:−e₀, 2:+e₁, 3:−e₁, 4:+e₂, 5:−e₂ (codage de tm_cert/verif_cert). -/
abbrev Dir := Fin 6

/-- Vecteur unité d'une direction. -/
def vec (d : Dir) : Int × Int × Int :=
  if d.val = 0 then (1, 0, 0) else if d.val = 1 then (-1, 0, 0)
  else if d.val = 2 then (0, 1, 0) else if d.val = 3 then (0, -1, 0)
  else if d.val = 4 then (0, 0, 1) else (0, 0, -1)

/-- Opposé d'un vecteur de ℤ³ (le cœur de Lean n'a pas d'instance `Neg` sur les produits). -/
def negV (p : Int × Int × Int) : Int × Int × Int := (-p.1, -p.2.1, -p.2.2)

/-- Différence de deux vecteurs de ℤ³. -/
def subV (p q : Int × Int × Int) : Int × Int × Int := (p.1 - q.1, p.2.1 - q.2.1, p.2.2 - q.2.2)

/-- Positions relatives des sites antérieurs : `posList w = [P_1, …, P_len]`, `P_i` = position du site visité
`i` pas plus tôt, relativement au site courant (`P_i = -(d_{j-1} + ⋯ + d_{j-i})`). -/
def posList : List Dir → List (Int × Int × Int)
  | [] => []
  | d :: w => negV (vec d) :: (posList w).map (fun q => subV q (vec d))

/-- Nombre de visites vu dans la fenêtre de mémoire `m` (le `N_j^{(m)}` de PREUVE.md). -/
def Nwin (m : Nat) (w : List Dir) (d : Dir) : Nat := 1 + ((posList w).take m).count (vec d)

/-- Décalage de l'état : nouveau pas en tête, oubli du plus ancien. -/
def shift (m : Nat) (d : Dir) (s : List Dir) : List Dir := (d :: s).take m

/-- Les 6 directions, en liste. -/
def dirs : List Dir := [0, 1, 2, 3, 4, 5]

/-- Numérateur du poids plafonné : `p_{min(N, K)}` avec `K = p.length` (indices à partir de 1). -/
def pval (p : List Nat) (N : Nat) : Nat := p.getD (min N p.length - 1) 0

/-- Somme entière `Σ_d p_{Nwin(s,d)} · H(shift d s)`. -/
def sommeEtat (m : Nat) (p : List Nat) (Hof : List Dir → Nat) (s : List Dir) : Nat :=
  dirs.foldr (fun d acc => pval p (Nwin m s d) * Hof (shift m d s) + acc) 0

/-- Test d'un état : `H_min ≤ H(s) ≤ H_max` et `B · Σ_d p_{Nwin(s,d)} H(shift d s) ≤ A · Q · H(s)`. -/
def testEtat (m : Nat) (p : List Nat) (Q A B Hmin Hmax : Nat) (Hof : List Dir → Nat) (s : List Dir) : Bool :=
  Nat.ble Hmin (Hof s) && Nat.ble (Hof s) Hmax && Nat.ble (B * sommeEtat m p Hof s) (A * Q * Hof s)

/-- Parcours de toutes les listes `acc ++ u`, `u` de longueur `k`. -/
def pourTous : Nat → List Dir → (List Dir → Bool) → Bool
  | 0, acc, t => t acc
  | k + 1, acc, t => dirs.all (fun d => pourTous k (acc ++ [d]) t)

/-- Vérification séquentielle de tous les états de longueur `m`. -/
def verifie (m : Nat) (p : List Nat) (Q A B Hmin Hmax : Nat) (Hof : List Dir → Nat) : Bool :=
  pourTous m [] (testEtat m p Q A B Hmin Hmax Hof)

/-- Tous les préfixes de longueur `k`. -/
def prefixes : Nat → List (List Dir)
  | 0 => [[]]
  | k + 1 => (prefixes k).flatMap (fun a => dirs.map (fun d => a ++ [d]))

/-- Version parallèle : une tâche par préfixe de longueur `k`. -/
def verifiePar (k : Nat) (m : Nat) (p : List Nat) (Q A B Hmin Hmax : Nat) (Hof : List Dir → Nat) : Bool :=
  let taches := (prefixes k).map
    (fun a => Task.spawn (fun _ => pourTous (m - k) a (testEtat m p Q A B Hmin Hmax Hof)))
  taches.all (fun t => t.get)

/-- Arbre à 6 branches pour stocker `H` sur les états bruts (accès en `m` pas, adapté au noyau). -/
inductive Arbre6 where
  | feuille (v : Nat)
  | noeud (t0 t1 t2 t3 t4 t5 : Arbre6)

def Arbre6.get : Arbre6 → List Dir → Nat
  | feuille v, _ => v
  | noeud _ _ _ _ _ _, [] => 0
  | noeud t0 t1 t2 t3 t4 t5, d :: s =>
    if d.val = 0 then t0.get s else if d.val = 1 then t1.get s else if d.val = 2 then t2.get s
    else if d.val = 3 then t3.get s else if d.val = 4 then t4.get s else t5.get s

end LoiAire
