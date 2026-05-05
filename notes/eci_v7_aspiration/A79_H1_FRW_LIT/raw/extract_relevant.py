#!/usr/bin/env python3
import json
data = json.load(open('/root/crossed-cosmos/notes/eci_v7_aspiration/A79_H1_FRW_LIT/raw/arxiv_recent.json'))
rel_keys = [
    '2406.02116',   # Chen-Penington 2024 'A clock is just a way to tell the time'
    '2406.01669',   # Kudler-Flam, Leutheusser, Satishchandran 2024 'Algebraic Observational Cosmology'
    '2504.07630',   # Speranza 2025 'An intrinsic cosmological observer'
    '2405.00847',   # Faulkner-Speranza 2024 GSL Killing horizons
    '2405.00114',   # De Vuyst-Eccles-Hoehn-Kirklin 2024 'Gravitational entropy is observer-dependent'
    '2412.15502',   # De Vuyst-Eccles-Hoehn-Kirklin 2024 'Crossed products and quantum reference frames'
    '2412.21185',   # Jensen-Raju-Speranza 2024 'Holographic observers for time-band algebras'
    '2411.19931',   # De Vuyst-Eccles-Hoehn-Kirklin 2024 'Linearization (in)stabilities and crossed products'
    '2407.20671',   # Gomez 2024 'Inflationary Cosmology as flow of integrable weights'
    '2603.25990',   # Seo 2026 'Implication of dressed form of relational observable on von Neumann algebra'
    '2510.24833',   # Giddings 2025 'Gravitational dressing: from the crossed product to more general structure'
    '2505.22708',   # Giddings 2025 'Quantum gravity observables: observation, algebras...'
    '2506.04311',   # Antonini-Chen-Maxfield-Penington 2025 'An apologia for islands'
    '2602.22153',   # Blommaert-Chen 2026 'Time in gravitational subregions and in closed universes'
    '2511.00622',   # Chen-Xu 2025 'An algebra for covariant observers in de Sitter space'
    '2507.01419',   # Requardt 2025 'Crossed product, modular dynamics, type III to II_infty'
    '2501.06009',   # Requardt 2025 'Type II_infty v.Neumann algebras and tensor structure quantum gravity'
    '2503.19957',   # Kudler-Flam-Prabhu-Satishchandran 2025 'Vacua and infrared radiation in de Sitter QFT'
    '2511.17382',   # Ribes-Metidieri-Agullo-Bonga 2025 'Entanglement and correlations in de Sitter spacetime'
    '2502.05135',   # D'Angelo-Ferrero-Frob 2025 'De Sitter quantum gravity ... asymptotic safety'
    '2404.12324',   # Cadamuro-Frob-Moreira-Ferrera 2024 'Sine-Gordon QFT in de Sitter spacetime'
    '2601.07915',   # Chandrasekaran-Flanagan 2026 'Subregion algebras in classical and quantum gravity'
    '2412.15549',   # Penington-Witten 2024 'Algebras and states in super-JT gravity'
]
for k in rel_keys:
    if k not in data:
        print('MISSING:', k); continue
    e = data[k]
    print(f"\n--- {k} | {e['published']} | {e['cat']} ---")
    print(f"TITLE: {e['title']}")
    print(f"AUTHORS: {', '.join(e['authors'])}")
    print(f"ABSTRACT: {e['summary'][:1800]}")
