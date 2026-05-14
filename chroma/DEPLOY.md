# CHROMA SU(2) GLUEBALL — Déploiement Vast

## Package
```
/root/crossed-cosmos/chroma/
├── run_chroma_su2.sh    (10KB) — Master script, 5 stages idempotent
├── analyze_gevp.py      (2.5KB) — GEVP analysis, m_0++/sqrt(σ) extraction
└── g2_scaling.py        (1.4KB) — g²(β) scaling from Langevin data
```

## Déploiement (1 commande)
```bash
# 1. Copier le package sur l'instance Vast
scp -r /root/crossed-cosmos/chroma root@<VAST_IP>:~

# 2. Lancer (tout est idempotent — peut être interrompu et relancé)
ssh -t root@<VAST_IP> 'cd chroma && bash run_chroma_su2.sh'
```

## Instance Vast recommandée
```
GPU: A40 48GB, A100 80GB, ou RTX 4090 24GB
OU CPU pur: 32+ cores, 64-128GB RAM (Chroma n'utilise PAS le GPU)
Budget: $0.30-0.70/h (GPU) ou $0.07-0.20/h (CPU pur)
Image: Ubuntu 22.04 LTS
Disk: 200GB+
```

## Étapes (idempotent — relançable)
```
0: apt install + build QMP → QDP++ → Chroma      (20-30 min)
1: HMC SU(2) Wilson, β=2.40/2.50/2.60             (2-3h/β)
2: Wilson loop measurement (string tension)        (30 min/β)
3: Wilson flow + glueball correlators              (3-4h/β)
4: GEVP analysis, m_0++/sqrt(σ) extraction         (5 min/β)
5: Falsification summary vs LT2010 (3.78)           (1 min)
```

## Décision post-Chroma
```
m_0++/√σ vs 3.78 (LT2010) ± Athenodorou-TePer 2021 (3.56)
├─ Δ < 5%  → MP1 VALIDATED → Phase 1 Go ($45-65 G4 microlocal)
├─ Δ 5-10% → MP1 marginal → recalibrer conf
└─ Δ > 10% → MP1 FALSIFIED → PIVOT (revoir base ECI v15)
```

## Références vérifiées
- Lucini-TePer JHEP 08(2010)119 — SU(N) glueball large-N (m_0++/√σ=3.78)
- Athenodorou-TePer JHEP 12(2021)082 (arXiv:2106.00364, withdrawn→published) — SU(N) 2→12 glueball spectrum ✓ verify-arxiv
- Glimm-Jaffe 1981 — constructive QFT, Springer
- Balaban 1989 CMP 122 — scattering theory YM
- Balaban 1996 CMP 175 — RG uniformity (conditionnel mass gap)
- ⚠️ arXiv:1004.3206 = Minimal Walking Technicolor, PAS glueball → NE PAS CITER (fab catch, cluster 369)

## Monitoring
```bash
# Depuis ce VPS:
watch -n 300 'ssh root@<VAST_IP> "tail -20 ~/chroma_work/logs/*.log 2>/dev/null"'
```
