#!/bin/bash
mkdir -p sorties
for f in constantes_verif hodge_check gauss_formules gauss_forme_mp boite_projecteurs ct_schwinger; do
  s=$(date +%s); python3 $f.py > sorties/$f.out 2> sorties/$f.err; echo "$f rc=$? $(( $(date +%s)-s )) s" >> sorties/RC.txt
done
python3 -c "import sys,numpy,scipy,sympy,mpmath;print(sys.version,numpy.__version__,scipy.__version__,sympy.__version__,mpmath.__version__)" > sorties/versions.txt 2>&1
