# Orchestration multi-LLM — tips & tricks pour la science (2026-05-08)

**Auteur** : Opus 4.7 max effort (companion document de `MULTI_LLM_PLAN.md`)
**Question Kévin** : "rtk gêne-t-il la science ? skills, sandbox, hooks, tips pour reasoning, cache, contexte, persona, prompt"

---

## §1 — rtk : où c'est utile, où c'est dangereux

### Utile (compression sans perte sémantique)

| Commande | Économie typique | Risque sci |
|---|---|---|
| `git status` | 80% | 0 |
| `git log` | 70% | 0 |
| `git diff` | 50% | 0 (utilise format unifié) |
| `ls` long dir | 70% | 0 |
| `tree` | 75% | 0 |
| `find -type f -name "*.py"` | 65% | 0 (file lists) |
| `pytest`, `cargo test`, `npm test` | 80-92% | 0 (résume failures) |
| `docker logs` | 85% | 0 |
| `kubectl describe` | 80% | 0 |
| `wget`, `curl` progress | 90% | 0 |

### **DANGEREUX pour la science** (à filtrer ou bypass)

| Commande | Problème |
|---|---|
| `grep` sur `.tex` / `.bib` | tronque les contextes critiques (équations multi-lignes) |
| `cat SUMMARY.md` (théorèmes verbatim) | rtk smart-summarize → perte verbatim |
| `python3 -c "from sympy import ...; print(expr)"` | sortie compactée → perte chiffres significatifs |
| `find notes/` (grand listing) | tronqué → on rate des SUMMARY.md |
| `pari -f script.gp` | output formaté pour math, ne PAS toucher |
| `mpmath` 80-digit precision | strip 0s → erreurs subtiles |

### Solutions (déjà appliquées)

1. **Filters projet-local** : `/root/crossed-cosmos/.rtk/filters.toml` (créé) avec `passthrough = true` pour les patterns dangereux. Le filter projet **prévaut** sur le filter global.

2. **Bypass explicite** : pour 1 commande spécifique :
   ```bash
   rtk proxy <commande>      # exécute sans aucun filtre rtk
   ```

3. **Outils Claude Code non-Bash** :
   - `Read` (Read tool) → pas de hook rtk → safe pour papers
   - `Edit` / `Write` → pas de hook rtk → safe
   - `Agent` → spawn sub-agent indépendant

4. **Désactivation totale** (si jamais nécessaire) :
   ```bash
   rtk init --uninstall
   # ou éditer /root/.claude/settings.json et retirer le hook PreToolUse
   ```
   Backup déjà en place : `/root/.claude/settings.json.bak`

### Recommandation finale rtk pour ECI/crossed-cosmos

**KEEP rtk activé** avec filters projet-local. Économie ~50-70% sur Bash typique (git, ls, find, build). Risque résiduel zéro grâce aux filters. Le hook s'active à la **prochaine** session Claude Code.

---

## §2 — Skills à créer (`/root/.claude/skills/`)

Format Claude Code skill = fichier markdown avec frontmatter description. Quand l'utilisateur tape `/nom-skill`, le skill est invoqué.

### Skills proposées (à valider Kévin avant écriture finale)

#### `/verify-arxiv`
```
---
description: Verify one or more arXiv IDs against the live arXiv API. Anti-hallu source of truth. Use before citing any arXiv reference.
---

Run: python3 /root/bin/verify-arxiv.py <id1> <id2> ...

Output: JSON with status VERIFIED / NOT_FOUND / FORMAT_ERROR / API_ERROR.
For each VERIFIED entry, the title and authors come DIRECTLY from arXiv API,
NOT from any LLM. Use this output as ground truth.
```

#### `/deepseek`
```
---
description: Route a task to DeepSeek V4 Pro (cheap reasoning, 7x less expensive than Sonnet, comparable quality on math/code).
---

Use cases: paper summary, code generation, cross-LLM verification.
Run: python3 /root/bin/deepseek.py [--model deepseek-chat|deepseek-reasoner] "prompt"

DO NOT use for: theorem proofs (use Opus), citation verification (use /verify-arxiv).
```

#### `/cross-check`
```
---
description: DVTS k=2 cross-LLM verification. Send a claim to DeepSeek for adversarial review. Use when Opus made a non-trivial claim and we want independent confirmation.
---

Run: python3 /root/bin/deepseek.py --system "@/root/crossed-cosmos/templates/cross_check.txt" \
     "CLAIM: ... EVIDENCE: ..."

Returns: AGREE / DISAGREE (+ exact pinpoint of the issue) / NEEDS-MORE-EVIDENCE.
```

#### `/find-recent`
```
---
description: Scout arXiv for recent papers (since YYYY-MM) on a topic via Gemini Flash Lite (free).
---

Run: python3 /root/bin/gemini-verify.py find-recent "topic" "2025-10"
Output: list of arXiv IDs + titles. ALWAYS pipe through verify-arxiv.py before citing.
```

#### `/zenodo-sync`
```
---
description: Bundle current crossed-cosmos state and create a new Zenodo version with DOI.
---

Run: bash /root/crossed-cosmos/scripts/zenodo_sync.sh <vXYZ>
(Script à créer ; pattern existant déjà utilisé en session 2026-05-06)
```

---

## §3 — Sandbox : Python venv + Vast.AI

### Local venv (pour orchestration légère)

```bash
python3 -m venv /root/llm-router-venv
source /root/llm-router-venv/bin/activate
pip install -U anthropic openai google-generativeai sympy mpmath requests \
              numpy scipy matplotlib  # math + plotting
```

Usage : pour scripts longs (verify_arxiv batch, multi-paper analysis), exécuter sous le venv. Pour calls LLM rapides, le wrapper `/root/bin/*.py` fonctionne avec `python3` système (urllib seulement).

### Vast.AI (compute lourd, indépendant des LLM)

- Déjà configuré pour Kevin (vastai CLI)
- Cas d'usage : MCMC chains (cosmologie), sympy dps>60 batch, LMFDB pull massif
- Pattern existant : `vastai-physics-postinstall.sh` au home dir

**Ne PAS utiliser pour LLM calls** — coût inférence on-prem > API DeepSeek.

---

## §4 — Hooks détaillés (PreToolUse / Stop / SessionStart)

### Hook actuellement actif

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "rtk hook claude" }]
      }
    ]
  }
}
```

Effet : intercepte chaque `Bash` tool call, rewrite si rtk a un filter pour la commande.

### Hooks à ajouter (proposés, à valider Kévin)

#### Stop hook — auto-checkpoint git/Zenodo

```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "bash /root/crossed-cosmos/scripts/auto_checkpoint.sh"
    }]
  }]
}
```

Script `/root/crossed-cosmos/scripts/auto_checkpoint.sh` :
- `git status -s` → si dirty → propose commit (mais NE commit PAS auto)
- Compte tags depuis dernier sync Zenodo → si ≥10 → notif "sync recommandé"

#### SessionStart hook — load context précompilé

```json
{
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "cat /root/crossed-cosmos/.session_context.md"
    }]
  }]
}
```

Le fichier `.session_context.md` regroupe :
- Hallu count
- Dernier git tag
- Théorèmes PROVED actifs
- Agents en cours (si on les sauvegarde)

**Pas auto-installés** — j'attends validation Kévin pour modifier settings.json au-delà de rtk.

---

## §5 — Reasoning : tips & tricks éprouvés (2024-2026)

### A. Chain-of-Thought (CoT) explicite

```
USER: Prove M114.B uniqueness for Q(i) at h=2.
LLM: ❌ "Let me think step by step..." (cargo cult)
LLM: ✅ "I'll structure the proof as: (1) state hypothesis precisely
     (2) enumerate the 12 rational h=2 forms (3) for each, compute
     R(f) = α_3/α_1·d_K (4) verify R ∈ Q\Q only at D=-4 ..."
```

**Tip** : pré-structurer la réponse avant de demander la dérivation. Cela force le modèle à stratifier au lieu de procrastiner.

### B. Self-consistency (sampling multiple)

Pour les claims numériques : exécuter 3 fois avec température 0.3 et accepter seulement la valeur qui apparaît ≥ 2/3.

```python
# pseudo
results = [call_deepseek(q, temperature=0.3) for _ in range(3)]
# extract numerical answer; majority vote
```

Coûte 3× mais réduit drastiquement les erreurs de signe et factor-of-2.

### C. Tree-of-Thought (ToT) pour math difficile

Au lieu d'un seul fil, demander 3 approches indépendantes puis sélectionner :

```
PROMPT 1: "Prove using Hilbert class polynomial."
PROMPT 2: "Prove using modular curve X_0(N) parametrization."
PROMPT 3: "Prove using Damerell ladder."
SELECTOR: "Among these 3 attempts, which is rigorous?"
```

C'est ce qu'on fait déjà avec multi-agent dispatch (M168/M170/M177).

### D. ReAct (Reasoning + Acting)

Modèles modernes intercalent reasoning step + tool call :
```
THOUGHT: I need to verify arXiv:1602.07508.
ACTION: verify-arxiv.py 2104.08808
OBSERVATION: VERIFIED, title="Bloch-Kato..."
THOUGHT: Now I can cite it.
```

C'est exactement le pattern Claude Code. **Ne pas se priver des tools** — un Opus seul "raisonne mieux" que Opus + tool calls n'est PAS vrai en pratique.

### E. Persona prompts (anti-flatterie)

Default LLM tend à dire "great question!" et à confirmer. Anti-pattern. Persona alternative :

```
SYSTEM: You are an adversarial reviewer. Your default verdict is "this is wrong, here is why". You only say "this looks correct" if you have actively tried and failed to find an error. You quote verbatim sources.
```

Très efficace pour cross-check (DeepSeek persona = adversarial reviewer reviewing Opus output).

### F. Few-shot pour tâches stéréotypées

Vérification arXiv : pas de few-shot nécessaire (output pure JSON).
Génération bibtex : few-shot avec 2 exemples corrects + 1 contre-exemple = perfect.
LaTeX patches : 1 example diff suffit.

---

## §6 — Cache : maximiser

### Anthropic prompt cache (cache_control ephemeral, 5min TTL)

**Structure recommandée** pour tout long prompt :
```
[STABLE_BLOCK]    ← 4000+ tokens, cache_control ephemeral
- ECI v9 status
- Verified refs
- Anti-hallu protocol
[/STABLE_BLOCK]

[SESSION_CONTEXT]   ← 500-2000 tokens, optionally cached
- Memories relevant to today's work

[USER_QUERY]   ← variable, NOT cached
```

Limites :
- 5 min TTL → si tu reposes une question 10 min plus tard, cache miss.
- Donc : encadrer les batches de questions DANS un même créneau de 5 min.
- Si pause > 5 min, considérer le fait que la 1ère requête sera plein-tarif.

### DeepSeek auto-cache

DeepSeek met automatiquement en cache le préfixe identique. **Pas de flag à mettre**, c'est implicite.

Cache hit price : $0.0036/M (98% off vs $0.435/M cache-miss).

Pratique : structurer les calls DeepSeek avec **TOUJOURS le même system prompt en tête** → toutes les calls subséquentes sont cache hit.

### Gemini Flash Lite

Pas de cache utilisateur explicite via l'API gemini-cli OAuth (free tier). Mais Kevin a 100% du quota → pas de problème.

---

## §7 — Contexte : ne pas charger ce qu'on n'utilise pas

### Hierarchical loading

```
Niveau 1 (TOUJOURS) : MEMORY.md (10 lines, < 1KB)
Niveau 2 (par task) : memory file pertinent (e.g. project_crossed_cosmos.md)
Niveau 3 (à la demande) : SUMMARY.md d'un Mxxx mission spécifique
Niveau 4 (extension) : full paper PDF (rare, via Read tool, pas de cache)
```

Ne JAMAIS charger en niveau 1 ce qui appartient au niveau 4.

### Compression contextuelle

Pour une longue session, compresser les anciens turns :
- Garder verbatim : claims numériques, théorèmes, citations
- Compresser : reasoning steps intermédiaires, outputs de tools déjà actés
- Outil : `claude /compact` (built-in)

### Tip : ne pas relire un fichier déjà lu

Claude Code track les Read calls. Si tu as déjà lu `/foo/bar.md` dans ce turn, ne le relis pas — utilise les lignes en mémoire.

---

## §8 — Persona : 4 personas utiles pour ce projet

### A. "Strict citation verifier"
```
SYSTEM: You verify citations. You output ONLY VERIFIED / NOT_FOUND / DISCREPANCY.
You NEVER speculate. You NEVER invent titles. You quote API output verbatim.
If you don't have access to an authoritative source for a specific claim, you say
INSUFFICIENT_DATA. You do NOT pretend to know.
```

### B. "Adversarial reviewer"
```
SYSTEM: You are an Inventiones / Annals reviewer. Your default verdict is REJECT.
You accept only if you've actively tried to find errors and failed. You quote
verbatim source language. You point to specific page numbers and equation labels.
```

### C. "Constructive collaborator" (pour Millennium pistes)
```
SYSTEM: You are a math research collaborator. You generate audacious but PRECISE
proposals. Each proposal includes: (1) specific 2024-2026 paper citation;
(2) identified gap in existing techniques; (3) falsifiable next step computable
in <100 hours. You explicitly mark speculative steps as SPECULATIVE.
```

### D. "Honest negativity scout"
```
SYSTEM: You look for reasons a claim is FALSE. You document obstructions, counter-
examples, "why this won't work" arguments. You consider the claim refuted if you
find ONE solid obstruction. You never sugar-coat.
```

(Used pour M174 DM, M175 H_0, M180 Higgs, M181 LIGO honest negatives.)

---

## §9 — Prompt structure — XML tags + clear blocks

```
<context>
(stable cache block here)
</context>

<task>
Verify arXiv:1602.07508 against API; if title matches "Bloch-Kato Tamagawa for ...",
proceed with citation; otherwise flag DISCREPANCY.
</task>

<constraints>
- Output ONLY JSON
- No prose, no preamble
- If unsure, return INSUFFICIENT_DATA
</constraints>

<output_format>
{"id": "...", "status": "...", "evidence": "..."}
</output_format>
```

XML tags > markdown headers pour LLMs (Claude/DeepSeek/Gemini all trained to respect them).

---

## §10 — Anti-patterns à éviter

| Anti-pattern | Pourquoi mauvais | Correctif |
|---|---|---|
| "Réfléchis bien" | trop vague | structurer la réponse attendue |
| "Sois créatif" | invite à la fab | "explore 3 approches **citées**" |
| Charger tout le repo en context | dilue le signal | Load on demand |
| "Es-tu sûr ?" | flatter le user, pas de vérif | "vérifie via arXiv API live" |
| Prompts identiques sans cache | gaspille tokens | mettre stable block en tête |
| Recommencer à zéro pour follow-up | perd le cache | continuer thread (5min) |

---

## §11 — Décision config Kévin

À valider avant que je modifie settings.json au-delà de rtk :

- [ ] **Skills** : créer les 5 skills ci-dessus dans `/root/.claude/skills/` ?
- [ ] **Stop hook** : auto-checkpoint git ? (proposes commit, ne commit pas auto)
- [ ] **SessionStart hook** : load context précompilé ?
- [ ] **Skill `/effort`** : déjà existante (visible dans tes commands), keep
- [ ] **Skill `/loop`** : utilisée Phase 7 wave 8+, keep

Si OK : 1 commit avec tous les artefacts. Sinon je cherry-pick.

---

**TL;DR** :
- rtk OK avec filters projet (déjà fait)
- DeepSeek wrapper prêt, attente clé Kévin
- Gemini wrapper prêt (gratuit, dispo immédiat)
- arxiv-verify wrapper prêt + testé sur fab 1709.02912 → correctement détecté WSe2
- Skills + hooks en attente d'approval
- Personae + cache + prompt structure documentés

---

**v6.0.53.121 candidate** : ce fichier + `MULTI_LLM_PLAN.md` + 3 wrappers + `.rtk/filters.toml`
