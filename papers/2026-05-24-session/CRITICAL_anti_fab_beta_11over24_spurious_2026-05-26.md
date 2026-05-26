---
name: critical-anti-fab-beta-11over24-spurious-2026-05-26
description: "🚨🚨🚨 BIG CATCH 2026-05-26 nuit : Le claim 'β_lattice = -11/24 à 0.06σ' était SPURIOUS. Refit direct des 8-points dense data donne K41 β=+0.4025 (POSITIF) et affine β=-0.047. PAS -0.458. Tout le H51→H59→H61 Solodukhin uplift résolvait un faux problème. Le décodeur perd β comme anchor structural. Reste valide : κ_FP=1/6, b_0=11N/48π², c∞=1/4 EXACT + d_s=7/3 conjecture (indépendante). P(decoder structural) 45-55% → 25-40% honest."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74bad51b-2b92-48e2-ba55-e4534c5565f3
---

# CRITICAL anti-fab catch : β = -11/24 SPURIOUS

## Le fait

L'agent Casini-Huerta n=2 max-effort a fait quelque chose qu'aucun agent précédent n'avait fait : **refit direct des 8 points dense data SU(5)..SU(12)**.

Résultats :
- K41 fit `κ = α·N^{5/3} + β` : **α=0.02008, β=+0.4025** ★ POSITIF
- Affine fit `κ = α·N + β` : β = **-0.047 ± 0.007** (mauvais χ²/dof=46)
- Free fit `κ = α·N^p + β` : p=1.81, β=+0.455 ★ POSITIF
- N² fit : β = +0.516

**Aucun fit ne donne β = -0.4583 = -11/24** sur les 8 points.

## Le claim spurious

Paper `Paper_Kolmogorov_53_SUN_PRL/main.tex` ligne ~104 dit :
> "The offset β = 0.421 is the boundary-Casimir contribution... we note that the offset is consistent at the 0.06σ level with -11/24 in the affine refit"

Ce wording est **internally inconsistent** :
- K41 offset = +0.421
- "affine refit" = -11/24 = -0.458
- "consistent at 0.06σ" — DEUX nombres complètement différents

L'origine likely : 4-point fit initial sur N=5,6,7,8 a peut-être donné -0.458 par fluctuation, mais sur 8 points cela disparaît.

## Conséquences

1. **TOUT le chemin H51 → H59 → H61 Solodukhin uplift** résolvait un problème qui n'existait pas. Le "β=-a_4/4" n'a pas d'ancre empirique solide.

2. **H62 d_s=7/3 RESTE valide** (indépendant de β) — c'est conjecture sur poles ζ_Δ_FP, pas sur β.

3. **3 anchors EXACT restent** : κ_FP=1/6 Kostant, b_0=11N/48π² Vassilevich, c∞=1/4 Bekenstein.

4. **β = +0.4025 K41 offset** reste empirique sans interprétation structurale claire (paper dit "Cartan generators" hypothesis mais pas dérivé).

## P(decoder structural) trajectoire honnête

| Stage | P |
|-------|---|
| Pré-H51 | 40-55% |
| Post-H51 brut (β=-a_4 fait) | 65-75% (over-claim) |
| Post-correction Vassilevich (-11/24 not -a_4) | 25-40% |
| Post-H51 refiné (β = -a_4/4) | 60-70% (still over-claim) |
| **Post-H61 + Casini-Huerta refit (β spurious)** | **25-40% honest** |

## Pourquoi cette catch matters

Cette session a montré comment les claims s'auto-propagent :
1. H51 agent initial fait wrong claim "exact -11/24"
2. Paper PRL répète "0.06σ consistent with -11/24"
3. Plusieurs sessions construisent dessus (H59, H61, decoder rescue)
4. **DEUX agents ont refait le fit explicit (Casini-Huerta n=2 ET refit_8points) et trouvé que -11/24 N'EST PAS DANS LA DATA**

Le coût de la sur-confiance : ~5 hours d'agents max-effort sur faux problème. Coût de la honnêteté : drop l'anchor spurious.

## What survives

Décodeur valide post-correction :

```
COUCHE 1 — Heat kernel coefficients
✅ κ_FP = 1/6 = a_2 SD (Kostant)
✅ b_0 = 11N/(48π²) = a_4 SD total (Vassilevich)
✅ c∞ = 1/4 = Bekenstein area-law

COUCHE 2 — Poles ζ_Δ_FP (d_s=7/3 conjecture)
🟡 ξ★ = 2/3 = pole s_1 (H62)
🟡 κ_FP = 1/6 = pole s_2 (H62)

COUCHE 3 — Turbulence
🟡 p_K41 = 5/3 or 1.81 (empirical)
🟡 F∞ = 9/10 (empirical)
🟡 β_K41_offset = +0.42 (Cartan hypothesis, unknown)

WAS — Now DROPPED
❌ β = -11/24 (was spurious — fit doesn't give this)
❌ β = -a_4/4 (was conjecture without empirical support)
```

## How to apply

Si futures sessions revisitent le décodeur :
1. **Ne PAS clamer β = -11/24** — c'est spurious
2. Le β empirique réel est **+0.4025** (K41 fit) ou **+0.455** (free p=1.81)
3. Le decoder reste valide pour 3 anchors EXACT + d_s=7/3 conjecture
4. P(structural complete) : **25-40% honest**
5. Vérifier TOUJOURS les claims numériques en refit explicit sur full data

## Anti-fab rule générale

**Plusieurs agents lisant le même paper et arrivant au même claim "structural" ne prouvent pas que le claim est vrai.** Il faut vérifier l'ancre EMPIRIQUE primaire en refit direct sur les données.

Trois agents (H51, Solodukhin uplift H61, decoder breakthrough) ont tous accepté "β = -11/24" comme empirical anchor. Le quatrième agent (Casini-Huerta n=2) a refait le fit et trouvé que c'était faux. **Refit explicit catches what literature parsing misses**.

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[correction_H51_anti_fab_vassilevich_2026-05-26]]
[[H61_renyi2_strict_BP2008b_FALSIFY_quarter_mechanism_2026-05-26]]
[[H62_dS_7over3_decoder_rescue_2026-05-26]]
[[project_decoder_breakthrough_quarter_dS_7over3_2026-05-26]]
[[SESSION_MASTER_FINAL_2026-05-26]]
