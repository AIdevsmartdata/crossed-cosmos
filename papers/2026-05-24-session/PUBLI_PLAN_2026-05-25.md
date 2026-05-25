# Plan publication first paper — 2026-05-25

## Decision : viser JHEP (free, fast, prestigieux)

JHEP via SCOAP3 = free pour auteur + 1-3 mois peer review + accepte indép.
Mais NÉCESSITE arXiv ID au submit.

## Bottleneck : arXiv endorsement requis pour 1ère submit

**Plan séquentiel** :

### Étape 1 — Email Bauerschmidt aujourd'hui
- Draft : `EMAIL_BAUERSCHMIDT_arxiv_endorsement_2026-05-25.md`
- Attach : `PAPER_KR_FP3_AnnalsMath.pdf`
- Cible : endorsement hep-lat (ou math-ph)
- ETA réponse : 3-7 jours

### Étape 2 — Submit arXiv hep-lat (post-endorsement)
- Submit via https://arxiv.org/submit
- Catégorie : hep-lat (primary), math-ph (cross-list)
- Title : "Conditional Spectral Bound for the Faddeev-Popov Operator..."
- Author : Kévin Rémondière, ORCID 0009-0008-2443-7166
- Affiliation : Independent Researcher, Oloron-Sainte-Marie, France

### Étape 3 — Reformatter pour JHEP
- Template : `\documentclass{JHEP3}` (téléchargeable sur jhep.sissa.it)
- Ajouter section Acknowledgments avec LLM disclosure
- Cover letter optional

### Étape 4 — Submit JHEP avec arXiv ID
- Via : https://jhep.sissa.it/jhep/
- Register account (free)
- Submit paper + arXiv ID
- ETA review : 1-3 mois

## Backup endorsers si Bauerschmidt KO

1. Don Zagier (Max Planck Bonn) — math-ph
2. Francesc Castella (UCSD) — number theory
3. Roman Kotecký (Charles U) — cluster expansion

## Backup journals si JHEP reject

- Acta Physica Polonica B (free + indep OK)
- SIGMA (math-phys focus, diamond OA)
- Foundations of Physics (Springer, free hybrid)

## LLM disclosure (à inclure dans Acknowledgments)

```
The author acknowledges the use of AI-based tools (large language models)
to assist with code review, literature search, manuscript preparation,
and discussion of mathematical and physical concepts. All scientific
claims, derivations, lattice computations, and conclusions are the sole
responsibility of the author. The AI tools did not generate any of the
core mathematical results or numerical data presented herein.
```

## Anti-fab discipline

- Tous les arXiv IDs cités vérifiés WebFetch
- Cluster firm 731 STABLE
- ORCID 0009-0008-2443-7166 propagé partout
- Pas mention "LLM" ailleurs que Acknowledgments (COPE compliant)
