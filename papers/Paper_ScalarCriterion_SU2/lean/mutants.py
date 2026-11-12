"""Mutants Lean : chacun change UN morceau de CritereScalaire.lean ; le build doit ÉCHOUER (ok=False)."""
import json, subprocess, sys, os
ICI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ICI, 'CritereScalaire.lean')).read()
M = {
 'M1_C4_200': ('    Delta F (2 * n) ≤ 256 * (Delta F n) ^ 2 := by', '    Delta F (2 * n) ≤ 200 * (Delta F n) ^ 2 := by'),
 'M2_seuil4_1_256': ('    (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 512) :\n    Delta F (2 * n) ≤ 256', '    (n : ℕ) (hn : 0 < n) (hD : Delta F n ≤ 1 / 128) :\n    Delta F (2 * n) ≤ 256'),
 'M3_sans_hs34': ('  rw [hdec]; linarith\n  · rw [hdec]; linarith\n  · rw [hdec]; linarith', None),
 'M4_vide_faux': ('    (∀ i, c o.Ω i = if i = 0 then 1 else 0) ∧', '    (∀ i, c o.Ω i = 1) ∧'),
 'M5_poison': ('end CritereScalaire', 'theorem poison : (0 : ℝ) = 1 := by norm_num\n\nend CritereScalaire'),
 'M6_C3_56': ('    Delta3 F (2 * n) ≤ 64 * (Delta3 F n) ^ 2 := by', '    Delta3 F (2 * n) ≤ 56 * (Delta3 F n) ^ 2 := by'),
 'M7_q_128': ('    QGapOn o Blim 𝒜₀ ℓ (256 * η) := by', '    QGapOn o Blim 𝒜₀ ℓ (128 * η) := by'),
 'M8_lien_sans_poids': ('    (∀ F, B F F ℓ = (c F 0) ^ 2 + ∑\' i, r i ^ n * (c F (i + 1)) ^ 2)', '    (∀ F, B F F ℓ = (c F 0) ^ 2 + ∑\' i, (c F (i + 1)) ^ 2)'),
}
res = {}
for nom, (a, b) in M.items():
    if nom == 'M3_sans_hs34':
        # retirer l'hypothèse de symétrie hs34 de decomp_4d : remplacer son usage par sorry-free échec
        m = src.replace('(hs34 n n (2 * n) n)))\n  have e2', '(hs12 n n (2 * n) n)))\n  have e2', 1)
    else:
        assert src.count(a) >= 1, nom
        m = src.replace(a, b, 1)
    assert m != src, nom
    open(os.path.join(ICI, 'mutants', nom + '.lean'), 'w').write(m)
    # assembler avec ce fichier
    env = dict(os.environ)
    tmp = os.path.join(ICI, 'mutants', 'CritereScalaire.lean')
    open(tmp, 'w').write(m)
    subprocess.run(['bash', '-c', f'sed "s#\\$ICI/CritereScalaire.lean#{tmp}#; s#OUT=\\$ICI/main.lean#OUT={ICI}/mutants/{nom}_main.lean#" {ICI}/assembler.sh > {ICI}/mutants/asm.sh && bash {ICI}/mutants/asm.sh'], check=True, capture_output=True)
    p = subprocess.run(['python3', '/root/physique/outils/qlab/qlab_exec.py', '--kind', 'lean', '--timeout', '900',
                        os.path.join(ICI, 'mutants', nom + '_main.lean')], capture_output=True, text=True)
    r = json.loads(p.stdout.strip().splitlines()[-1])
    res[nom] = {'ok': r['ok'], 'rc': r['rc'], 'lean': r['lean'], 'job': r['job_id']}
    print(nom, 'ok=', r['ok'], r['lean'], 'ATTENDU ok=False ->', 'ROUGE (bon)' if not r['ok'] else 'VERT (MAUVAIS)', flush=True)
json.dump(res, open(os.path.join(ICI, 'mutants', 'resultats.json'), 'w'), indent=1)
