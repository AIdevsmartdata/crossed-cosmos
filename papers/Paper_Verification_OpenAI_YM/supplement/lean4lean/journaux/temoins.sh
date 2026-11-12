#!/bin/bash
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home
cd /work/lean4lean_essai/temoins
mkdir -p build
cat > TemoinVrai.lean <<'X'
theorem temoin_vrai : 2 + 2 = 4 := rfl
theorem temoin_vrai2 (a b : Nat) : a + b = b + a := Nat.add_comm a b
X
cat > TemoinFaux1.lean <<'X'
import Lean
open Lean Elab Command
set_option debug.skipKernelTC true in
run_cmd liftCoreM <| addDecl <| .thmDecl { name := `Faux1.bad, levelParams := [], type := mkConst ``False, value := mkConst ``True.intro }
X
cat > TemoinFaux2.lean <<'X'
import Lean
open Lean Elab Command
set_option debug.skipKernelTC true in
run_cmd liftCoreM <| addDecl <| .thmDecl { name := `Faux2.bad, levelParams := [],
  type := mkApp3 (mkConst ``Eq [1]) (mkConst ``Nat) (mkNatLit 1) (mkNatLit 2),
  value := mkApp2 (mkConst ``Eq.refl [1]) (mkConst ``Nat) (mkNatLit 1) }
X
for m in TemoinVrai TemoinFaux1 TemoinFaux2; do
  LEAN_PATH=/work/lean4lean_essai/temoins/build lean $m.lean -o build/$m.olean; echo "compile $m rc=$?"
done
# sanity: le noyau de Lean refuse-t-il quand on ne saute pas le controle ?
cat > Controle.lean <<'X'
theorem ctl : False := True.intro
X
lean Controle.lean >/dev/null 2>&1; echo "controle (doit etre != 0) rc=$?"
L=/work/lean4lean_essai/src/.lake/build/bin/lean4lean
export LEAN_PATH=/work/lean4lean_essai/temoins/build
for m in TemoinVrai TemoinFaux1 TemoinFaux2; do
  /usr/bin/time -v nice -n 10 $L -v $m > run_$m.out 2> run_$m.err; echo "lean4lean $m rc=$?"; tail -4 run_$m.out; grep -E "lean4lean found|error|mismatch" run_$m.err | head -3
done
