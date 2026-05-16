# Endorser email: Don Zagier (MPIM Bonn) for HSH v3 letter (JNT)

**Paper**: "The number of Q-rational weight-5 CM newforms attached to an imaginary quadratic field: a theorem (Gauss 1801) and a conjecture (Rubin 1991)"
**Target**: Journal of Number Theory (short note, ~7 pp)
**Author**: Kevin Remondiere (ORCID 0009-0008-2443-7166)
**Recipient**: Prof.\ Don Zagier, Max-Planck-Institut fur Mathematik, Bonn.
Email: `zagier [at] mpim-bonn.mpg.de`
Web: https://people.mpim-bonn.mpg.de/zagier/

**Etiquette reminders** (post Dumontet-incident, cf.\ Paper_Hurwitz_7disc endorser_choice.md):
- Single email, no follow-up within 2 weeks.
- Attach `main.pdf` and `D5460_theta_direct.gp` directly.
- Plain text, no HTML, no signature image.
- Send at ~9:00 AM Bonn time (08:00 UTC).
- Do NOT cc other mathematicians.

---

## Subject line

```
Endorsement request -- JNT short note: weight-5 CM newforms Q-rational count via Gauss 1801 genus theory -- independent researcher
```

## Body (English, 315 words)

```
Dear Professor Zagier,

I am writing to request your consideration as endorser for a short
note (7 pp) I am preparing for submission to Journal of Number Theory:

   "The number of Q-rational weight-5 CM newforms attached to an
    imaginary quadratic field: a theorem (Gauss 1801) and a
    conjecture (Rubin 1991)."

Let K = Q(sqrt(D)) be an imaginary quadratic field of fundamental
discriminant D < 0 and class group Cl(K). Let r(D) be the number of
weight-5 Hecke newforms of level |D| with complex multiplication
by K, Nebentypus chi_K, whose Fourier coefficients are all rational.
The note proves, in three pages of elementary harmonic analysis on
the finite abelian group Cl(K), that when Cl(K) is a 2-group

   r(D) = |Cl(K)[2]| = 2^{rk_2 Cl(K)} = 2^{t-1},

with t the number of distinct prime divisors of |D|; the last
equality is your familiar genus theorem of Gauss, Disquisitiones
Sectio V Sections 225-237 (cf. Cox 1989 Theorem 3.15). A precise
conjecture for the case where Cl(K) admits odd torsion -- consistent
with, but not derived from, Rubin's 1991 main conjecture for
imaginary quadratic fields -- complements the theorem.

The result is verified on seven discriminants spanning rk_2 in
{0, 2, 3, 4}, including the first known fundamental discriminant
of pure 2-rank 4, D = -5460 = -4*3*5*7*13, where the prediction
r(-5460) = 16 is confirmed by two independent PARI/GP methods
against two earlier circulated guesses predicting 32 and 1024.

I would be grateful if you could indicate whether (a) the 2-group
formula has been previously stated in the literature unknown to me,
and (b) you would be willing to endorse the arXiv submission (math.NT
primary 11F11; secondary 11R29, 11F30, 11G15). The PDF and a PARI/GP
verification script are attached; the script reproduces in under a
minute on a laptop. I am happy to revise in any direction.

Sincerely,
Kevin Remondiere
Independent researcher
Tarbes, France
ORCID: 0009-0008-2443-7166
kevin.remondiere [at] gmail.com

Attachments:
 - main.pdf (7 pp, the paper)
 - D5460_theta_direct.gp (PARI/GP script for the pure rank-4 anchor)
```

## Why Zagier (Tier_HONNETE rationale)

1. **Genus theory anchor**: the theorem identifies r(D) with Gauss's
   1801 invariant 2^{t-1}. Zagier's 1976 Enseign. Math. paper on
   zeta_K(-1) is the canonical modern arithmetic exposition of how
   classical genus-theoretic invariants combine with L-values in real
   and imaginary quadratic settings; his perspective on
   |Cl(K)[2]| = 2^{t-1} as an L-theoretic identity is unmatched.
2. **Theta-series-by-class expertise**: the theta-direct method used
   for D=-5460 (16 reduced forms paired with Hecke characters) is in
   the lineage of Zagier's work on theta liftings and class-number
   formulae (Hirzebruch-Zagier 1976, Zagier 1975 on Eisenstein series
   of weight 3/2 attached to class groups).
3. **Track record with short L-value notes**: historically responsive
   to amateur and independent researchers on short rigorous notes.
4. **No overlap with Heath-Brown / Mazur-Rubin literature**: the present
   paper deliberately does NOT route through 2-Selmer parity
   conjectures or twist families of a single CM elliptic curve; it is
   a clean elementary statement about CM newform spaces, well-suited to
   Zagier's classical-arithmetic taste.

**Honesty caveat to maintain**: I am NOT to claim that the 2-group
formula is "completely new in the literature" -- the underlying
identity |Cl(K)[2]| = 2^{t-1} is 1801 and the rationality criterion
psi^2 = 1 is standard for CM newforms. The novelty is in the
explicit identification "r(D) = the Gauss invariant" at weight 5
combined with the rk_2=4 numerical anchor D=-5460. Zagier may very
well point to a folklore reference; if so, the paper pivots to an
explicit-verification framing (cf. Paper_Hurwitz_7disc protocol).

## Fallback path (if Zagier declines or no answer in 2 weeks)

1. **Henri Cohen** (Bordeaux) -- PARI/GP, class groups of imaginary
   quadratic fields, GTM 138/239 expositor. Email via the PARI list.
2. **Larry Washington** (UMD) -- author of GTM 83 "Introduction to
   Cyclotomic Fields"; expert on |Cl[2]| via genus theory.
3. **Karl Rubin** (UCI) -- author of the 1991 Invent. Math. main
   conjecture paper directly relevant to Conjecture 3.

If all three decline, fall back to the arXiv account's prior endorser
chain (used for previous submissions in math.NT).

## Timeline

| Date         | Action                                                  |
|--------------|---------------------------------------------------------|
| 2026-05-16   | Send Zagier email (English version above)              |
| 2026-05-17 to 2026-05-30 | Wait 2 weeks                                |
| 2026-05-30   | If no answer: send to Henri Cohen                       |
| 2026-06-06   | If no answer from Cohen: Washington / Rubin             |
| 2026-06-13   | arXiv submission (with or without endorsement)          |
| 2026-06-14   | JNT submission via Elsevier Editorial Manager           |

---

## Closing notes

- Word count of email body: **315 words** (target 280-320, within bracket).
- Tone: deferential, factual, Tier_HONNETE. No "discovered" / "novel"
  / "breakthrough" language.
- Anti-fab discipline: all references in the paper (Cox 1989, Gauss
  1801, Miyake 2006, Rubin 1991, Shimura 1971, PARI 2024) are
  bibliographic monographs / journal articles with no arXiv IDs, so
  verify-arxiv does not apply. The journal reference Rubin 1991
  Invent. Math. 103 pp. 25-68 has been spot-checked at MathSciNet
  MR1079839 (manual operator verification recommended pre-send).
- The earlier "Mazur-Rubin parity" and "Heath-Brown 1994 congruent
  number" digressions have been intentionally REMOVED from the
  manuscript v2 per corpus-corrections-2026-05-15.md sections 2-3
  (the former was a mis-attribution, the latter mis-applied to a
  varying-D CM family that does not occur in our setting).
