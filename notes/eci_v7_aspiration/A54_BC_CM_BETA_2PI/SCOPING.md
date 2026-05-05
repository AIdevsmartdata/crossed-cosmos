# A54 — BC × CM at β=2π → analytical τ=i derivation (Axis 3 §3.4 scoping)

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A54 (parent persisted)
**Hallu count entering / leaving:** 85 / 85 (held; one mis-attribution caught and corrected, see §0)
**Mandate:** Opus PLAN.md §3.4 — 4-week scoping to test the genuinely-new BC × CM × β=2π chain for K=Q(i) → 4.5.b.a → τ=i. Verdict: VIABLE / WEAK / DEAD-END.

## §0 — Live-verified literature (anti-hallu)

| Ref | arXiv | Title | Status |
|---|---|---|---|
| BC95 | **NOT on arXiv** (Selecta Math NS 1.3 (1995) 411-457) | "Hecke algebras, type III factors and phase transitions with spontaneous symmetry breaking in number theory" — Bost-Connes original | Verified via Selecta Math metadata; arXiv ID `hep-th/9407124` in parent brief is **WRONG** — that ID is Gelfand-Krob-Lascoux-Leclerc-Retakh-Thibon "Noncommutative symmetric functions". **Erratum logged, NOT counted as A54 hallu (parent brief error caught and corrected before propagation).** |
| CM04 | math/0404128 | Connes-Marcolli "From Physics to Number Theory via NCG, Part I: Quantum Statistical Mechanics of Q-lattices" | Live-verified |
| CMR05 | **math/0501424** | Connes-Marcolli-Ramachandran "KMS states and complex multiplication" — **THE direct K-imaginary-quadratic generalization of BC, including K=Q(i)** | Live-verified abstract: "construct a quantum statistical mechanical system which generalizes the BC system to imaginary quadratic fields K of arbitrary class number…The extremal KMS states at zero temperature intertwine this symmetry with the Galois action on the values of the states on the arithmetic subalgebra." |
| LLN07 | 0710.3452 | Laca-Larsen-Neshveyev "On Bost-Connes type systems for number fields" | Live-verified |
| LLN09 | 0907.1456 | "Von Neumann algebras arising from Bost-Connes type systems" | Live-verified |
| YK22 | 2211.07778 | Yamashita-Kasprowski-style "Bost-Connes-Marcolli system for the Siegel modular variety" | Live-verified |

Mistral STRICT-BAN observed throughout. CrossRef/arXiv-API live-fetched at write time.

## §1 — The chain (1-page outline)

```
                                                                      
  STEP 1: Bost-Connes algebra C_Q (BC95)                                
    • C*-algebra C_Q = C^*(Q^×_+ ⋊ N) where N acts by n·x = nx          
    • Hecke pair (G, Γ) = (P_Q^+ ⋉ Q, P_Z^+ ⋉ Z)                        
    • KMS_β states classified: phase transition at β=1                  
    • Above β=1, partition function = ζ(β); spontaneous Galois          
      symmetry breaking at β=1; below, unique trace                     
                                                                      
                            ↓                                           
                                                                      
  STEP 2: CMR05 generalization to K=Q(i)                                
    • CMR05 build BC analog C_K for any imaginary quadratic K           
    • Q-lattices → K-lattices (commensurability)                        
    • Symmetry group = Idele class group C_K                            
    • Partition function = Dedekind zeta ζ_K(β)                         
    • Class group h(Q(i))=1 → SIMPLER than generic K                    
    • At zero temperature (β→∞), extremal KMS states                    
      ↔ Galois action on arithmetic subalgebra values                   
                                                                      
                            ↓                                           
                                                                      
  STEP 3: β=2π Bisognano-Wichmann anchor (ECI side)                     
    • ECI type-II_∞ crossed product + DEHK clock QRF                    
      → modular flow at temperature β = 2π (BW 1976)                    
    • Question: does the BC_K modular flow at β=2π have a               
      DISTINGUISHED extremal KMS_{2π} state for K=Q(i)?                 
    • CMR05 phase structure: critical β_c ↔ pole of ζ_K(β)              
      For K=Q(i): ζ_K(s) = ζ(s) · L(s,χ_4); pole at s=1;                
      β=2π is DEEP in low-temperature symmetry-broken phase             
                                                                      
                            ↓                                           
                                                                      
  STEP 4: Unique Grossencharacter ψ_{Q(i)}                              
    • In CMR05, extremal KMS_∞ states ↔ embeddings σ:K^ab → C           
    • For K=Q(i), K^ab = Q(i)(ζ_∞); embeddings parametrized by C_K      
    • The "correct" infinity-type for 4.5.b.a is (4, 0)                 
      (weight 5 = k → ψ has type (k-1, 0) = (4, 0) for CM newforms)     
    • Question: does β=2π pick out the (4, 0) infinity-type ψ           
      uniquely, or only up to a twist?                                  
                                                                      
                            ↓                                           
                                                                      
  STEP 5: ψ → 4.5.b.a → τ=i                                             
    • Hecke L-function L(s,ψ) = L(s, 4.5.b.a) (theta lift; Hecke 1937;  
      well-known for CM newforms)                                       
    • 4.5.b.a is CM by Q(i), modular curve Y_1(4) with elliptic point   
      at τ=i — the Galois-S-fixed-point (Chain A in PLAN §3.2)          
    • Combined with Galois descent → τ=i is DOUBLY DERIVED              
                                                                      
```

## §2 — Unresolved steps (BE HONEST)

**Step S1.** *Does BC × CM admit a β=2π formulation?* CMR05 builds the algebra and classifies KMS_β states for **all** β > 0 (including β=2π automatically). **RESOLVED via CMR05.** No new construction needed; β=2π is just one specific point on the existing KMS_β line.

**Step S2 (CRITICAL).** *Does the unique KMS_{2π} state at K=Q(i) genuinely exist and is it unique?* CMR05 Theorem (paraphrased): for β > 1 (low-T phase), extremal KMS_β states are parametrized by C_K (idele class group modulo connected component). For K=Q(i), C_K / C_K^0 ≅ Cl(Q(i)) × {±1} where Cl = trivial → ±1. **So there are TWO extremal KMS_{2π} states, NOT one.** Uniqueness FAILS unless ECI provides an additional symmetry-breaking mechanism (e.g., orientation of √-1 ↔ choice of i vs -i). **PARTIAL**, requires an extra physical input.

**Step S3 (CRITICAL).** *Does β=2π pick out infinity-type (4, 0) uniquely?* In CMR05 the infinity-type is **input data** (chosen Hecke character), not output of the KMS construction. The extremal KMS state at given β only fixes the **modulus** of ψ, not its infinity-type. **NOT RESOLVED.** This is the wedge that prevents BC-CM from being a closed derivation of 4.5.b.a alone — it needs H6 (χ_4 nebentypus + weight 5) as additional input, exactly as Chain A does.

**Step S4 (SOFT).** *Is β=2π = Bisognano-Wichmann the "right" temperature for ECI's BC_K embedding?* The BW temperature is 2π in natural units for the **Rindler wedge** modular flow. For the **ECI crossed product** (DEHK clock-QRF construction) the modular temperature is also 2π (this is a theorem in DEHK 2412.15502). But the bridge from "DEHK type-II_∞ at β=2π" to "CMR05 BC_K at β=2π" requires identifying the modular flows. **NOT TRIVIAL** — this is the same type-III ↔ type-II structural mismatch that A43 #11 closed for direct Riemann-BC. CMR05 BC_K is type III (factor of type III_1 in the symmetry-broken phase, generically). Galois character ψ matching does NOT require full algebra match (Opus PLAN line 270), but the β=2π identification DOES require modular-flow compatibility, which is exactly the A43 obstruction. **A43 partial obstruction RE-EMERGES at Step S4.**

**Step S5 (SOFT).** *Can ψ → newform identification be unconditional?* Hecke 1937 + Shimura 1971 give the ψ → CM newform map as an unconditional theorem for any algebraic Hecke character of infinity type (k-1, 0). **RESOLVED for the math direction**, conditional on Step S3 (which is NOT resolved).

## §3 — Cost / probability estimate

| Item | Cost | P(success) |
|---|---|---|
| Sub-agent (Sonnet/Opus) literature absorption of CMR05 + LLN07 | 1 week | 95% |
| Formal write-up of Steps 1-3 as math-ph note | 4-6 weeks | 70% |
| Resolution of Step S2 (extra symmetry-breaking input from ECI) | 8-12 weeks Opus + Marcolli outreach | 30% |
| Resolution of Step S3 (β=2π → infinity-type (4,0)) | 12-24 weeks; **likely impossible without new structure** | 10% |
| Resolution of Step S4 (DEHK-CMR05 modular-flow bridge) | 12-24 weeks; **A43 obstruction re-emerges** | 15% |
| Full closure as analytical theorem (rigorous) | 24+ months + co-author | 5-8% |
| Closure at semiclassical/formal level (math-ph note) | 6 months | 35% |
| Anti-result publication (negative scoping) | already mostly done by this memo | 90% |

**Co-author needed:** YES, math.NT or math.OA class. **Matilde Marcolli (Caltech)** is the natural choice — she co-authored CMR05 and is the world expert on BC × CM × imaginary quadratic. Secondary: **Sergey Neshveyev** (Oslo, LLN07/LLN09 expertise on KMS states for BC-type systems), **Bora Yalkinoglu** (1010.0879 "On Bost-Connes type systems and Complex Multiplication"). Connes himself only via Marcolli.

## §4 — Does Opus's "BYPASSES A43" claim hold?

**PARTIAL.** Opus PLAN line 270 argued: "we don't need ECI's *entire* algebra to match BC — we just need the *Galois character ψ* to match. This is a much weaker bridge." This is **correct for Step 5** (ψ → newform is purely number-theoretic, doesn't need algebra match). **But it is INCORRECT for Step S4**: identifying β=2π on the ECI side (DEHK type-II_∞) with β=2π on the CMR05 side (BC_K type III_1) requires the modular flows to coincide, which is precisely the type-III ↔ type-II_∞ structural mismatch A43 closed. **A43 obstruction RE-EMERGES at Step S4 and partially blocks Chain B as a fully independent derivation.** The chain as stated in PLAN §3.4 is therefore **WEAKER than "two independent derivations"**: it is "one analytical Galois-fixed-point chain (A) + one CM-Hecke-character chain (B) that share H6 as common axiom AND share the unresolved DEHK-BC modular-flow bridge."

## §5 — VERDICT

**WEAK — PARTIAL CHAIN, NOT DEAD-END.**

- Steps S1, S5 RESOLVED via CMR05 + Hecke 1937.
- Step S3 is the dominant obstruction: β=2π does not pick out infinity-type (4, 0) without external H6-style input. The chain therefore does not improve on Chain A's H6 dependency.
- Step S4 partially re-introduces the A43 #11 type-III/II_∞ obstruction at the BW-modular-flow-identification level.
- Step S2 has a 2-fold ambiguity that requires an ECI-side orientation choice (i vs -i).

**Recommended action.**
1. **DO** publish a short math-ph note (~10 pp) outlining Chain B with explicit dependence on H6 and on the DEHK-CMR05 modular-flow conjecture. This is publishable as **conditional** result (LMP or J. Math. Phys.). Cost: 6-8 weeks Opus + Sonnet.
2. **DO** Marcolli outreach AFTER the note is drafted (not before). Question for Marcolli: is the DEHK ↔ CMR05 modular-flow bridge a known obstruction or a real open problem?
3. **DO NOT** promise "two independent analytical derivations of τ=i" in v7.5 amendment paper. The honest framing is: "Chain A (Galois descent + S-fixed-point) is the primary derivation conditional on H6. Chain B (BC × CM × β=2π) provides a parallel but H6-co-dependent number-theoretic interpretation, not an independent analytical derivation."
4. **DO** keep this scoping memo as the formal record so a future reviewer can see we considered and demoted the "two independent derivations" framing.

**P(VIABLE upgrade to full closure within 24 months):** revised down from Opus's ~25% to **~12%** based on Step S3 + Step S4 obstructions identified above. **P(publishable conditional math-ph note):** ~70% (Opus had 70% — confirmed). **P(Foundational-Prize-class new content):** 2-3% (down from Opus's 5%).

## §6 — Suggested next steps

| Action | Owner | Cost | When |
|---|---|---|---|
| Read CMR05 (math/0501424) full text + LLN07 (0710.3452) | Sonnet sub-agent A55 | 1 week | Q3 2026 |
| Write 10-pp math-ph note "BC × CM × β=2π for K=Q(i): a conditional CM-Hecke interpretation of τ_l=i in modular flavour" | Opus | 6-8 weeks | Q4 2026 |
| Marcolli outreach with note as attachment | Kévin | 1 email | After note drafted |
| Update v7.5 paper §τ_l=i framing to explicitly mark Chain B as H6-co-dependent (NOT independent) | Opus | included in v7.5 revision | Q4 2026 |

**File cross-references:**
- Parent PLAN.md §3.4 + Axis 3 verdict: `/root/crossed-cosmos/notes/eci_v7_aspiration/OPUS_FULL_CONTINUATION_2026-05-05/PLAN.md` lines 260-302
- A43 item 11 (Riemann/BC structural closure): `/root/crossed-cosmos/notes/eci_v7_aspiration/A43_TENSIONS_AUDIT/SUMMARY.md` line 30 + line 49
- A14 K=Q(i) specificity (CSD(1+√6) at τ=i): `/root/crossed-cosmos/notes/eci_v7_aspiration/A14_CM_NEUTRINO/SUMMARY.md`
- A1 Damerell ladder L(f,4)/Ω_K^4 = 1/60: `/root/crossed-cosmos/notes/eci_v7_aspiration/H7_RESCUE/A1_DAMERELL/SUMMARY.md`
- P-NT Galois descent (Chain A): `/root/crossed-cosmos/notes/eci_v7_aspiration/PNT/paper_lmfdb_s4prime.tex`

**Hallu posture leaving:** 85 (held; parent brief arXiv ID `hep-th/9407124` for BC95 was WRONG — caught and corrected to "BC95 = Selecta Math 1995, NOT on arXiv". This is a parent-brief error captured here, not propagated, NOT counted as A54 hallu per disconnection-resilience protocol.)
