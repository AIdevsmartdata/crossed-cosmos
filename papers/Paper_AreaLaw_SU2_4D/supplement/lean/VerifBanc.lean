import LoiAire.DonneesM11Calcul

/-!
# Vérificateur compilé du certificat m = 11 (6¹¹ = 362 797 056 états BRUTS)

Exécute `LoiAire.verifiePar 2 11 p_m11 (2^40) A_m11 B_m11 Hmin_m11 Hmax_m11 Hof`, c'est-à-dire la fonction dont
la correction est démontrée dans le noyau (`LoiAire.certificat_of_verifiePar`, valable pour TOUTE fonction `Hof`).
Ici `Hof s` = valeur de `H` lue dans le fichier binaire de tm_cert pour l'orbite de `s` (forme canonique
constructive de tm_cert + recherche dichotomique). Une erreur dans cette lecture ne peut pas produire un faux
« true » : elle ferait échouer le test `H_min ≤ H(s)` ou l'inégalité. Confiance : compilateur Lean → C, compilateur C,
environnement d'exécution (GMP, tâches), lecture du fichier ; PAS le noyau.
Usage : verifcert <certificat.bin> <poids.txt>
-/

open LoiAire

def readU64 (b : ByteArray) (i : Nat) : Nat :=
  (b.get! i).toNat ||| ((b.get! (i+1)).toNat <<< 8) ||| ((b.get! (i+2)).toNat <<< 16) |||
  ((b.get! (i+3)).toNat <<< 24) ||| ((b.get! (i+4)).toNat <<< 32) ||| ((b.get! (i+5)).toNat <<< 40) |||
  ((b.get! (i+6)).toNat <<< 48) ||| ((b.get! (i+7)).toNat <<< 56)

/-- Forme canonique constructive de tm_cert : le pas le plus récent devient +x, le premier pas hors de son axe
devient +y, le premier pas selon le troisième axe devient +z ; code en base 6, pas le plus récent en poids fort. -/
def canonCode (s : List Dir) : Nat :=
  match s with
  | [] => 0
  | d0 :: _ =>
    let a0 := d0.val / 2
    let e0 := d0.val % 2
    match s.find? (fun d => d.val / 2 != a0) with
    | none => s.foldl (fun c d => 6 * c + (d.val % 2 ^^^ e0)) 0
    | some d1 =>
      let a1 := d1.val / 2
      let e1 := d1.val % 2
      let a2 := 3 - a0 - a1
      let e2 := match s.find? (fun d => d.val / 2 == a2) with
        | none => 0
        | some d2 => d2.val % 2
      s.foldl (fun c d =>
        let a := d.val / 2
        let e := d.val % 2
        let dig := if a == a0 then (e ^^^ e0) else if a == a1 then 2 + (e ^^^ e1) else 4 + (e ^^^ e2)
        6 * c + dig) 0

/-- Recherche dichotomique du code `c` parmi les `n` codes triés (décalage 8 octets). -/
def chercher (b : ByteArray) (n c : Nat) : Option Nat :=
  let rec go (fuel lo hi : Nat) : Nat :=
    match fuel with
    | 0 => lo
    | f + 1 =>
      if lo < hi then
        let mid := (lo + hi) / 2
        if readU64 b (8 + 8 * mid) < c then go f (mid + 1) hi else go f lo mid
      else lo
  let k := go 80 0 n
  if k < n && readU64 b (8 + 8 * k) == c then some k else none

/-- Entiers décimaux d'un texte (séparés par des blancs). -/
def entiers (s : String) : List Nat :=
  let r := s.toList.foldl (fun (st : List Nat × Option Nat) ch =>
    if ch.isDigit then (st.1, some ((st.2.getD 0) * 10 + (ch.toNat - '0'.toNat)))
    else match st.2 with
      | some v => (st.1 ++ [v], none)
      | none => (st.1, none)) ([], none)
  match r.2 with
  | some v => r.1 ++ [v]
  | none => r.1

def main (args : List String) : IO UInt32 := do
  match args with
  | [chemin] =>
    let b ← IO.FS.readBinFile chemin
    let n := readU64 b 0
    let hOff := 8 + 8 * n
    let Hof : List Dir → Nat := fun s =>
      match chercher b n (canonCode s) with
      | some k => readU64 b (hOff + 8 * k)
      | none => 0
    let t0 ← IO.monoMsNow
    let ok := pourTous 7 [0, 2, 1, 4] (testEtat 11 p_m11 (2 ^ 40) A_m11 B_m11 Hmin_m11 Hmax_m11 Hof)
    let t1 ← IO.monoMsNow
    IO.println s!"banc : 6^7 = 279936 états, ok = {ok}, {t1 - t0} ms"
    return 0
  | _ => return 2
