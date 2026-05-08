# Plan multi-LLM économies sans dégrader la qualité (2026-05-08)

**Auteur** : Kévin Remondière + Opus 4.7
**Statut** : Phase 7 wave 10 setup, post-v6.0.53.120
**Inspiration** : `github.com/AIdevsmartdata/chimere-odo` (Engram + DVTS + intent classifier)

---

## §1 — Diagnostic coût actuel

| Modèle | Input $/M | Output $/M | Usage typique session ECI v9 |
|---|---|---|---|
| Claude Opus 4.7 max | $15 | $75 | tous les sub-agents M134-M181 (cher++) |
| Claude Sonnet 4.6 | $3 | $15 | sub-agents M168, R-3 verifications |
| Claude Haiku 4.5 | $1 | $5 | rare |
| **DeepSeek V4 Pro (75% off → 31 mai)** | **$0.435** | **$0.87** | NON UTILISÉ — opportunité |
| DeepSeek V4 Pro (cache hit) | $0.0036 | — | quasi-gratuit après 1ère requête |
| DeepSeek-Chat V3.2 | $0.28 | $0.42 | encore moins cher |
| Gemini Flash Lite | gratuit | gratuit | Kevin a 100% quota |
| **Mistral large-latest** | — | — | **STRICT-BANNED** (4+ fabrications) |

**Conclusion** : DeepSeek V4 Pro est **7× moins cher que Sonnet** en input, **17× moins cher en output**, qualité comparable sur math/code (HumanEval ~92%, MATH ~95% vs Sonnet ~93/96). Migration partielle Sonnet → DeepSeek = économie estimée **70-85%** sur les sous-agents de vérification.

---

## §2 — Architecture 3 tiers

### Tier 1 — Reconnaissance (Gemini Flash Lite, gratuit)

**Cas d'usage** :
- Vérification live arXiv ID via API officielle (`https://export.arxiv.org/api/query?id_list=XXXX.YYYYY`)
- Recherche d'adresse email institutionnelle (Google + university directory)
- Recherche papers récents 2025-2026 (Google Scholar via Gemini)
- Vérification DOI via CrossRef (`https://api.crossref.org/works/DOI`)

**Implémentation** : commande `gemini` CLI déjà installée à `/usr/local/bin/gemini`. Wrapper Python à écrire (`bin/gemini-verify.py`) pour exposer `verify_arxiv(ids)`, `find_email(name, institution)`, `find_recent_papers(topic, since)`.

**Anti-hallu** : confronter sortie Gemini à arXiv API directe. Si discordance → flag.

### Tier 2 — Cheap reasoning (DeepSeek V4 Pro)

**Cas d'usage** :
- Lire 1 paper arXiv et en extraire les claims clés (au lieu de Sonnet)
- Générer scripts Python de vérification (sympy/mpmath/PARI)
- Patches LaTeX en réponse à reviewer comments
- Cross-verification : "Opus a dit X, DeepSeek est-il d'accord ?" (détection hallu cross-modèle)
- Sub-agents ECI : remplacer Sonnet pour M168, M173 (CM stab classification, biquadratic check)

**Implémentation** : OpenAI-compatible endpoint `https://api.deepseek.com/v1`. Wrapper Python `bin/deepseek.py` avec prompt caching (98% off après 1ère requête identique → cumul cache hit 5min).

**Anti-hallu** :
- TOUJOURS demander citations exactes (DOI/arXiv ID + titre verbatim)
- Re-verify citations via Tier 1 Gemini AVANT acceptation
- Cross-check critique avec Opus si claim mathématique non trivial

### Tier 3 — Hard math (Claude Opus 4.7 max effort)

**Cas d'usage** (uniquement) :
- Preuves de théorèmes (M177-style 5-layer chain)
- Synthèse architecturale (ECI v9 → v10)
- Décisions stratégiques (dispatch, paper structure)
- Final critique sur output Tier 2 avant commit

**Économie** : limiter Opus aux sessions où *vraiment* nécessaire. Autres tâches → DeepSeek.

### Tier 4 — Compute (Vast.AI)

- Numérique mpmath dps > 60
- MCMC chains cosmologie
- LMFDB pull massif
- Indépendant de l'API LLM

---

## §3 — Pipeline science multi-modèles (style chimere-odo)

```
[USER QUERY]
    │
    ▼
[INTENT CLASSIFIER]  ── Gemini Flash Lite, 1-shot
    │
    ├── citation_check   → Tier 1 (Gemini live arXiv API)
    ├── code_gen         → Tier 2 (DeepSeek)
    ├── paper_summary    → Tier 2 (DeepSeek longue ctx)
    ├── theorem_prove    → Tier 3 (Opus max)
    ├── synthesis        → Tier 3 (Opus max)
    └── millennium       → Tier 3 (Opus + DeepSeek joint)
    │
    ▼
[QUALITY GATE]   ── DVTS-style cross-LLM verification
    │
    ├── claim a citation? → Tier 1 force re-verify
    ├── claim a derivation? → sympy/mpmath replay
    ├── claim a fact? → Tier 2 independent check
    │
    ▼
[COMMIT to git/Zenodo]
```

**DVTS k=2 minimum** : pour tout claim non trivial, exiger qu'au moins 2 modèles indépendants confirment OU qu'une vérification numérique (sympy/mpmath/PARI) cross-check. Anti-hallu fondamental.

---

## §4 — Cache strategy détaillée

### Anthropic (Opus session)

**Stable block au TOP de tout prompt long** (cache_control ephemeral, 5min TTL) :

```
[STABLE-CACHE-BLOCK]  ← cached
=============================================
ECI v9 STATUS (2026-05-08):
- 6 PROVED theorems: M142/M151.1/M162/M168.1/M170.1/M177.1
- 4 falsifiable predictions (M177.1)
- 8 honest orthogonalities documented
- Hallu 103 cumulative, 0 silent

ANTI-HALLU PROTOCOL (NON-NEGOTIABLE):
- Mistral STRICT-BANNED for citations (4+ fabrications)
- All arXiv IDs MUST be live-verified via API
- All DOIs MUST be verified via CrossRef
- "Verbatim" requires exact quote with page number

KEY REFERENCES (verified):
- arXiv:2012.01111 Kanno-Watari (F-theory K3xK3)
- arXiv:1602.07508 Büyükboduk-Lei (anticyclotomic IMC)
- arXiv:2104.08808 Kriz (Bloch-Kato Tamagawa)
- arXiv:1703.10521 Sagnier (NCG arithmetic site)
- LMFDB: 4.5.b.a (UNIQUE among 8 wt-5 dim-1 CM Q(i))
- LMFDB: 88.3.b.a (W^Q canonical M151.1)
=============================================
[/STABLE-CACHE-BLOCK]

[QUERY-SPECIFIC]  ← not cached
...
```

**Économie estimée** : sur Opus, si stable block = 4000 tokens et tu fais 30 requêtes en 5min → cache hit 29 fois → réduction $15 × 4000 × 30 / 1M = $1.80 → ~$0.18 (10% du prix sans cache, soit $1.62 économisés par session).

### DeepSeek

Cache hit à $0.0036/M (98% off vs $0.435/M). Stratégie identique : stable block + per-query body. Si tu fais 100 sub-agent calls dans une session → économie massive.

### Gemini Flash Lite

Pas de cache explicite, mais quotas généreux (Kevin "100%" disponible). À utiliser sans réserve pour Tier 1.

---

## §5 — Hooks Claude Code à installer

### `~/.claude/settings.json` :

1. **PreToolUse** sur `Agent` :
   - Si `description` contient {"verify", "check arxiv", "find email"} → suggérer route Tier 1 Gemini au lieu d'Opus.
   - Sinon → laisser passer.

2. **Stop** :
   - Auto-`git status` ; si dirty et stable depuis 3 min → propose commit + push GitHub.
   - Tous les 10 tags Phase 7 → suggère sync Zenodo.

3. **SessionStart** :
   - Charge `MEMORY.md` + `MULTI_LLM_PLAN.md` + état `git log --oneline -5` automatiquement.
   - Affiche : "Hallu count: 103 ; ECI v9 PROVED: 6 ; in flight: $(detect agents)"

(Hooks à valider avec skill `update-config` quand on les implémente, je ne les active pas sans ton OK.)

---

## §6 — Skills Claude Code à ajouter

| Skill | Raccourci | Cible | Coût |
|---|---|---|---|
| `/verify-arxiv` | id1,id2,... | Gemini live arXiv API | gratuit |
| `/verify-email` | "Name @ Institution" | Gemini Google search | gratuit |
| `/find-recent` | "topic since 2025-XX" | Gemini Scholar | gratuit |
| `/deepseek` | task description | DeepSeek V4 Pro | $0.4/M |
| `/cross-check` | claim X | DeepSeek + Opus joint | mixte |
| `/router` | "what to do with task T?" | classifier seul | quasi-gratuit |
| `/zenodo-sync` | tag vX.Y.Z | upload bundle + DOI | gratuit |

---

## §7 — Sandbox Python

`/root/llm-router-venv/` :
- `anthropic` (Opus calls direct si besoin hors Claude Code)
- `openai` (DeepSeek + GPT compat)
- `google-generativeai` (Gemini)
- `requests` (arXiv API + CrossRef)
- `sympy`, `mpmath` (math verification)
- `pari-python` ou shell-out (Damerell ladder)

`/root/bin/` :
- `verify-arxiv.py` (Tier 1)
- `deepseek.py` (Tier 2 wrapper)
- `llm-route.py` (orchestrateur intent → tier)
- `cross-check.py` (DVTS k=2)

---

## §8 — Prompts templates anti-hallu pour DeepSeek

### Template A — Citation check
```
SYSTEM: You are a citation verification agent. You MUST output ONLY:
- arXiv ID (verbatim format YYYY.NNNNN)
- Exact title (no paraphrase)
- Authors verbatim
- Verification status: VERIFIED-via-arxiv-API / NOT-FOUND / DISCREPANCY
You MUST NOT speculate or invent. If unsure: "INSUFFICIENT-DATA".

USER: Verify the following arXiv references:
{ids}
```

### Template B — Cross-LLM math check
```
SYSTEM: You are checking another LLM's mathematical claim. Your job is
to find errors, NOT to agree. Look specifically for:
- Sign errors, off-by-one, factor-of-2, factor-of-π
- Wrong attribution (which paper? which equation?)
- Misapplied theorem (assumptions not satisfied?)
- Numerical errors (verify with sympy if applicable)

CLAIM TO CHECK: {claim}
EVIDENCE PROVIDED: {evidence}

Respond with: AGREE / DISAGREE / NEEDS-MORE-EVIDENCE
If DISAGREE: explain exactly what is wrong with verbatim quote of source.
```

### Template C — Paper summary
```
SYSTEM: You are a math/physics paper summarizer. Output exactly:
1. Main theorem (verbatim if stated)
2. Key assumptions (numbered list)
3. Proof technique (1-2 sentences)
4. Numerical/empirical claims (verbatim values)
5. What this paper does NOT prove (limitations)
NEVER paraphrase a theorem statement; quote it.

PAPER: {arxiv_id}
USER FOCUS: {focus_question}
```

### Template D — Brainstorm Millennium
```
SYSTEM: You are exploring open mathematical problems. Be audacious but
PRECISE. Each suggestion must:
- Cite ≥1 specific 2024-2026 working paper or preprint
- Identify a specific gap in existing techniques
- Propose a falsifiable next step (computable in <100 hours of compute)

PROBLEM: {millennium_problem}
PRIOR CONTEXT (from Kevin's GPT/DeepSeek session): {kevin_context}
ECI v9 RELEVANT FACTS: {eci_facts}

Generate 5 concrete pistes. Each: title + technique + expected obstacle + falsifiability test.
```

---

## §9 — Anti-hallu cross-LLM (CRITIQUE)

L'approche "DVTS k=2" ne suffit PAS si les 2 modèles partagent les mêmes biais d'entraînement. Ajouter :

1. **Live verification au moment T** (arXiv API, CrossRef, MathSciNet, LMFDB) — source de vérité indépendante.
2. **Sympy / mpmath / PARI replay** pour toute identité numérique.
3. **Mistral REMAINS BANNED** (4+ fabrications confirmées 2026-05-05).
4. **Si DeepSeek + Opus + Gemini confirment mais sont en contradiction avec arXiv API live** → trust API, flag les 3 modèles.

Catalogue 12 catches sur 5 jours = 0 silent fabs. Discipline à maintenir cross-tier.

---

## §10 — Plan d'exécution séquentiel

| Étape | Tier | Bloqué par | Coût estimé |
|---|---|---|---|
| 1. Sauvegarder ce plan + commit | Tier 3 | — | $0 |
| 2. Setup DeepSeek (clé + venv + wrapper) | Tier 3 | clé Kévin | $0 |
| 3. Skills + hooks (quand validés) | Tier 3 | (2) | $0 |
| 4. Verify 12 emails (arXiv + adresses + content) | Tier 1+2 | (3) | < $0.50 |
| 5. Finir expériences gating emails | Tier 2+3 | (4) | $5-10 |
| 6. ECI v9 → v10 cosmologie + particles | Tier 3 + Tier 2 sub | (3) | $20-40 |
| 7. Millennium problems (par batch) | Tier 3 + Tier 2 joint | input Kévin | $5-15 par problème |

**Total estimé** : $50-100 pour TOUTE la session étendue, vs $200-500 sans optimisation.

---

## §11 — Décisions à prendre par Kévin (gating)

- [ ] **Clé DeepSeek** : Kévin doit fournir sa clé V4 Pro. Méthode sécurisée recommandée :
  - `echo "$DEEPSEEK_KEY" > /root/.config/deepseek/key && chmod 600` (hors chat)
  - Ou `! echo $DEEPSEEK_KEY > /root/.config/deepseek/key` (dans Claude Code, le `!` exécute en shell — la clé n'est pas mémorisée par moi)
- [ ] **Approve hooks settings.json** : je proposerai un diff exact avant d'écrire.
- [ ] **Millennium problems** : Kévin colle le content DeepSeek/GPT free pour chaque problème quand prêt.

---

## §12 — Métriques de succès

- Hallu count reste à 103 ou augmente seulement par catches (jamais silent).
- ECI v9 → v10 publication-ready avec cosmology+particle integrations.
- Au moins 1 nouveau (A) PROVED ou (B+) reduction sur Millennium.
- Coût total session ≤ $100.
- Tous les 12 emails verified + send-ready.

---

**Last updated** : 2026-05-08 par Opus 4.7 (1M ctx) max effort
