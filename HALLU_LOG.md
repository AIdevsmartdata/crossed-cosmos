# HALLU_LOG.md — Cluster hallu (append-only, single source of truth)

Chaque ligne = 1 catch firm de fabrication ou attribution incorrecte. Format :
`YYYY-MM-DD | ID/claim | catcher | type | source`

**Total firm catches au 2026-05-16 : 391**

Historique consolidé jusqu'au 2026-05-11 : **368** (cf. `/root/.claude/projects/-root/memory/project_crossed_cosmos.md` pour la litanie complète : A34/A36/A37/A52/M40/M48/M53/M59/M79/M114/M142-M177/morn15/morn39/morn54/morn55/morn56/etc.)

## Catches 2026-05-12

(Aucun firm catch documenté ce jour. La cluster reste à 368.)

## Catches 2026-05-13

- `2026-05-13 | arXiv:2506.00284 | Gemini-search via Ξ Verifier | WITHDRAWN (nouveau type) | LHC piste G4 wave, 3/8 workers DS le citaient comme support` → **+1 = 369**
  - Auteur D.C. Jacobsen, "A Constructive Proof of Existence and Mass Gap for Pure SU(3) YM"
  - Soumis 2025-05-30, retiré 2025-06-13 par arXiv ("ne répond pas aux standards de qualité")
  - Profil yangmills.dev = crank-tier (41/41 lemmas, OCaml/Rust/ARM64 triple-verified, Arthur J. Miller Proof Engine)
  - Idées 5D orbifold + polymer Wilson potentiellement récupérables si réoutillées par école Balaban-Magnen-Sénéor sérieuse

## Format pour ajouts futurs

```
YYYY-MM-DD | <arxiv_id ou claim verbatim> | <catcher: nom outil/agent> | <type> | <contexte court>
```

Types valides :
- `FAB_ARXIV` : arXiv ID fabriqué ou mauvais paper
- `MIS_ATTRIBUTION` : arXiv réel mais authors/title/contenu mal-cités
- `WITHDRAWN` : arXiv réel mais retiré
- `FAB_FORMULA` : formule mathématique fabriquée
- `FAB_NUMERIC` : valeur numérique inventée (pas vérifiée PARI/sympy)
- `OVERCLAIM` : conjecture présentée comme théorème prouvé

## Discipline

1. **Avant tout commit ou propagation d'un arXiv ID** : `python3 /root/bin/verify-arxiv.py <id>` + check WITHDRAWN.
2. **Si le catch est nouveau** : append ici + commit.
3. **Si plusieurs sources convergent** : 1 entrée + note "propagé dans N docs".
4. **Ne JAMAIS gonfler le compteur sans entrée traçable.** Le "375+" précédent dans SOUL.md/AGENTS.md/INVARIANTS.md était une inflation non documentée → corrigée au 2026-05-13.

- `2026-05-13 | arXiv:1004.2667 | Ξ Verifier (audit wave G4) | FAB_ARXIV | Wave G4 microlocal — cited as "Mozgovoy-Schiffmann Hodge-Deligne moduli spaces" — actual: Raji Heyrovska "Bonding distances in nanomaterials" — DS V4 Pro fabrication. Missed by built-in wave audit (audit_claude.md marked "ID real")` → **+1 = 370**

- `2026-05-13 | Balaban CMP 122 (1989) 175-202 attribution | Opus 4.7 direct (G4_attack_2026_05_13_OPUS_direct.md) | MIS_ATTRIBUTION | Cité partout dans le projet (M54_01, M46_04, eci_context.txt, 15/15 workers wave G4) comme "Scattering Theory for Yang-Mills Fields on T⁴". Vrai titre via Project Euclid table of contents : "Large field renormalization. I. The basic step of the R operation". Réf existe et page numbers correctes, mais le topic exact est renormalisation par blocs, pas scattering. Convergent uncertainty héritée du contexte (CITE_NEEDED systematic sans vérification) — pas une fab DS, une mis-attribution propagée projet. eci_context.txt corrigé.` → **+1 = 371
- `2026-05-13 | Balaban CMP 122 (1989) 175-202 | Opus max-effort G4 attack | MIS_ATTRIBUTION | Actual title: "Large field renormalization. I. The basic step of the R operation" — NOT "Scattering theory" as assumed in M54_01, M46_04, eci_context.txt, 15/15 workers wave G4, diverses docs. Source: Project Euclid table of contents. Corrigé dans eci_context.txt` → **+1 = 371**

## Catches 2026-05-15

- `2026-05-15 | m_2⁺⁺/√σ = 5.505(70) claim for SU(2) in AT 2021 Table 34 | Ξ Verifier (audit Paper 6′ subagent) | FAB_NUMERIC | Claimed as AT 2021 Table 34 data for SU(2) 2⁺⁺ ground state. Actual value: 5.349(20). Verified via pdftotext extraction of arXiv:2106.00364v3, line-by-line table parsing. Value 5.505(70) does not appear anywhere in the 122-page paper. Propagated in Paper 6′ "connaissances fraîches" context and pattern A52 vigilence note.` → **+1 = 372**

## Catches 2026-05-16 — W40 4 digests (372→390)

Batch W40 T3 fondations — 8 firm A52 arXiv IDs caught (2026-05-16):
- `2026-05-16 | arXiv:1908.02302 | Opus W40 T3 digest | FAB_ARXIV | Cité comme CCHS 2D YM — vrais IDs 2006.04987/2201.03487 hard-injected eci_context LAYER 5` → **+1 = 373**
- `2026-05-16 | arXiv:2001.04894 | Opus W40 T3 digest | FAB_ARXIV | Mis-attribué constructive YM 4D` → **+1 = 374**
- `2026-05-16 | arXiv:2004.11488 | Opus W40 T3 digest | FAB_ARXIV | Mis-attribué constructive YM 4D` → **+1 = 375**
- `2026-05-16 | arXiv:1506.01497 | Opus W40 T3 digest | FAB_ARXIV | Mis-attribué constructive YM 4D` → **+1 = 376**
- `2026-05-16 | arXiv:2009.11378 | Opus W40 T3 digest | FAB_ARXIV | Cité comme Chatterjee YM-Higgs — vrai = 2401.10507` → **+1 = 377**
- `2026-05-16 | arXiv:2007.08294 | Opus W40 T3 digest | FAB_ARXIV | Cité comme Shen-Zhu-Zhu — vrai = 2204.12737` → **+1 = 378**
- `2026-05-16 | hep-lat/0207010 | Opus W40 T3 digest | FAB_ARXIV | Mis-attribué LTW 2004 — vrai = hep-lat/0404008` → **+1 = 379**
- `2026-05-16 | arXiv:2006.06694 | Opus W40 T3 digest | FAB_ARXIV | Cité comme AT 2021 — vrai = 2106.00364` → **+1 = 380**

W40 T1 lattice — catches:
- `2026-05-16 | arXiv:2011.07257 | Opus W40 T2 digest (Paper 3 rebuild) | FAB_ARXIV | Cité comme AT 2021 glueball — faux ID` → **+1 = 381**
- `2026-05-16 | P02 q-table contra-corpus M142 | Opus W40 T1 digest | FAB_NUMERIC | q(D) values conflit avec M142 10 PROVED theorems (Q(i)=1/12 etc.) — user-facing fab retractée` → **+1 = 382**
- `2026-05-16 | P05 L₅(67,1)=2.660 numerical fab | Opus W40 T1 digest | FAB_NUMERIC | DS V4 Pro fabricated L-value vs PARI direct=14.3575 (×5.4)` → **+1 = 383**
- `2026-05-16 | P01 F(N) data input fab | Opus W40 T1 digest | FAB_NUMERIC | Fitted faux ratios vs Table 34 AT 2021 — triggered RELAUNCH` → **+1 = 384**
- `2026-05-16 | arXiv:1006.4518 (Lüscher) | Opus W40 T2 digest (P25) | MIS_ATTRIBUTION | g²_GF↔Φ_univ 0.5% match = artefact échelle (Δ≈19% sur μ)` → **+1 = 385**

W40 worker-internal additional catches (T1+T2+T3 cumul, worker-internal = broader hygiene, NE PAS confondre avec firm propagation):
- `2026-05-16 | +5 worker-internal A52 catches T1+T2+T3 | W40 workers DS V4 Pro | FAB_ARXIV | Catches internes workers — non propagées au corpus. Broader hygiene = 390` → **cluster firm = 385, broader = 390**

- `2026-05-16 | Bennett-Holligan-Hill 2024 PRD 109 | Opus P50 Sp(2N) agent (Session 11 agents) | FAB_ARXIV | Cité comme "Bennett-Holligan-Hill 2024 PRD 109" dans briefs Session 11. Vrai = Bennett et al. 2021 PRD 103 054509 arXiv:2010.15781. Propagé dans briefs utilisateur (moi) vers sous-agents — firm propagation.` → **+1 = 386**

- `2026-05-16 | arXiv:1101.4057 (Gemini hallu) | Ξ Research (deepsearch Gemini) | FAB_ARXIV | Gemini-search retourna 1101.4057 comme "Wrochna Calderón projector gauge theory" — vrai = half-metallicity Co/Ni AlN (cond-mat). Vrai Wrochna = 1403.7153, 1706.08942.` → **+1 = 387**

- `2026-05-16 | "Caraiani-Bhatt 2024 prismatic Shimura" | Opus deep-dive #70 | FAB_ARXIV | N'existe pas — flaggé par agent.` → **+1 = 388**
- `2026-05-16 | "Caraiani-Hevesi-Tamiozzo eigenvarieties" | Opus deep-dive #70 (brief utilisateur) | MIS_ATTRIBUTION | NON CONFIRMÉ — CITE_NEEDED flag` → **+1 = 389**
- `2026-05-16 | Hodge-Tate period map attribution Caraiani-Scholze | Opus deep-dive #70 | MIS_ATTRIBUTION | Vrai = Faltings 1988` → **+1 = 390**
- `2026-05-16 | Igusa varieties attribution Caraiani-Scholze | Opus deep-dive #70 | MIS_ATTRIBUTION | Vrai = Mantovan 2005` → **+1 = 391**

## Catches 2026-05-16 — Build dependency chain (cluster firm 391, unchanged)

> **Note discipline** : les 3 entrées ci-dessous sont de type BUILD_DEP / AUDIT_MISS — pas des fabrications mathématiques. Le cluster firm 391 reste **inchangé**. Ces entrées documentent des erreurs d'ingénierie logicielle interceptées par exécution SSH réelle.

- `2026-05-16 | deploy v3 QMP "optional for parscalar" claim | SSH execution Instance #36879858 | BUILD_DEP | deploy_gevp_t2g_vast_v3.sh:152 — Opus deploy v3 annotait QMP comme étape facultative "REQUIRED by qdpxx configure even for parscalar" ajouté après coup dans v3 (commentaire ligne 152). Réalité : qdpxx configure échoue sans QMP présent, même en mode single-rank parscalar. QMP doit être installé en premier avec --with-qmp-comms-type=SINGLE. Corrigé dans v4.`
- `2026-05-16 | deploy v3 qdpxx tarball "wget includes all deps" claim | SSH execution Instance #36879858 + #36884254 | BUILD_DEP | qdpxx-qdp1-46-0/other_libs/qio empty — Le tarball wget de qdpxx (tag qdp1-46-0) n'inclut PAS le sous-module QIO (other_libs/qio/ vide). Deux tentatives d'exécution SSH ont échoué à cause de ce sous-répertoire vide. Fix canonique : git clone --recursive https://github.com/usqcd-software/qdpxx.git OU installer QIO en externe d'abord (méthode adoptée dans v4). Corrigé dans v4.`
- `2026-05-16 | G audit "19/19 issues fixed" miss runtime deps | SSH execution Instance #36884254 failure | AUDIT_MISS | G_deploy_v2_audit_2026-05-16.md §3a-3b — L'agent G (Opus code audit) a validé 19/19 issues corrigées dans deploy_gevp_t2g_vast_v3.sh mais n'a PAS détecté les deux dépendances runtime manquantes (QMP requis / QIO sous-module vide). L'audit était purement statique (lecture de code). La vérification SSH réelle sur instance Vast a révélé les deux blocages. Méta-leçon : code audit statique ≠ smoke test d'exécution. Discipline future : run build smoke sur instance bon marché AVANT déploiement production.`
