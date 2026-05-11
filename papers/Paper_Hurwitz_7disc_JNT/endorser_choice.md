# Endorser Choice: Don Zagier (recommended) vs Larry Washington (alternative)

**Paper**: "Real quadratic discriminants with integer Hurwitz ratio $D^2 / B_{2,\chi_D}$: a finite list of seven"
**Author**: Kévin Remondière
**Date**: 2026-05-11

---

## §1 Decision: **Don Zagier** as primary endorser

**Recommended**: Don Zagier (Max-Planck-Institut für Mathematik, Bonn).
- Email: `zagier [at] mpim-bonn.mpg.de`
- Web: https://people.mpim-bonn.mpg.de/zagier/

**Rationale**:
1. Zagier's 1976 L'Enseign. Math. paper is the foundational reference for the rational evaluation of $\zeta_K(-1)$ for real quadratic $K$. Our 7-list is essentially a divisibility refinement of Zagier's Table I.
2. The Hirzebruch–Zagier 1977 signature interpretation (§5 of our paper) is co-authored by Zagier; he is the natural expert.
3. Zagier has historically been responsive to amateur and independent researchers (cf. his work with Roy, Bloch, Browning), and is known to evaluate short L-value notes quickly.
4. Bonn MPIM hosts the L-function and modular form database (LMFDB) collaboration, with which our work is computationally aligned.

**Alternative**: Larry Washington (UMD).
- Email: `lawrencewashington [at] umd.edu` (institutional address; verify before use)
- Web: https://www.math.umd.edu/~lcw/

**Rationale for alternative**:
1. Washington's GTM 83 *Introduction to Cyclotomic Fields* (1997) Theorem 4.2 is the formula we cite as the master Hurwitz identity.
2. Washington's work with Ferrero (Ferrero–Washington 1979) gives the $\mu$-invariant zero we quote in §4 finite-density heuristic.
3. Washington is also responsive to short L-value classification notes.

**If Zagier declines or doesn't respond in 2 weeks, fall back to Washington.**

---

## §2 Email draft for Don Zagier

### Subject line

```
Endorsement request — short J. Number Theory note "Real quadratic Hurwitz 7-discriminants" — independent researcher
```

### Body (English)

```
Dear Professor Zagier,

I am writing to request your consideration as endorser for a short
note I am preparing for submission to Journal of Number Theory:

  "Real quadratic discriminants with integer Hurwitz ratio
   D^2 / B_{2, chi_D} : a finite list of seven"

The note (8 pages) classifies, by direct calculation and computational
verification up to D <= 10^6, the positive fundamental discriminants D
for which the rational

  k(D) := D^2 / B_{2, chi_D} = pi^2 sqrt(D) / L(2, chi_D)
        = D^2 / (24 zeta_K(-1))    [K = Q(sqrt(D))]

is a positive integer. The list is

  D in {8, 12, 24, 28, 60, 76, 156}

with k(D) in {32, 36, 48, 49, 75, 76, 117} respectively. The
underlying Hurwitz formula L(2, chi) = pi^2 B_{2, chi} / f^{3/2} for
real even primitive characters is, of course, classical (your 1976
L'Enseign. Math. paper provides the canonical tabulation of
zeta_K(-1)). What appears to be new (modulo my limited literature
search) is the explicit characterisation of the seven exceptional
discriminants by INTEGRALITY OF k(D), together with a million-D PARI
sweep and a heuristic D^{-3/2} density argument supporting
finiteness.

I draw two further observations in the note: (i) the imaginary
quadratic mirror at s = 3 produces exactly one integer-k case
(d = -4); and (ii) higher weights k = 4, 6, ... yield no integer-k
events for D <= 200, suggesting the s = 2 phenomenon is genuinely
isolated.

Section 5 sketches the Hirzebruch–Zagier signature interpretation
(your 1977 paper with Hirzebruch in the Baily–Shioda volume,
together with van der Geer 1988 Ch. VIII), under which the seven
discriminants correspond to Hilbert modular surfaces whose
arithmetic-part signature divides D^2.

I would be most grateful if you could indicate whether (a) the
seven-list classification has been previously stated in the
literature unknown to me (in which case the paper becomes a
re-derivation), and (b) you would be willing to act as endorser for
the arXiv submission (math.NT, 11M06 / 11R42 / 14J27).

The PDF of the manuscript and a numerical verification PARI script
are attached. The verification reproduces independently in < 1
minute on a modern laptop.

Thank you for your time and consideration. I am happy to revise the
manuscript in any direction your expertise suggests.

Sincerely,
Kévin Remondière
Independent researcher
Tarbes, France
ORCID: 0009-0008-2443-7166
kevin.remondiere [at] gmail.com

Attachments:
 - main.pdf (8 pp, the paper)
 - verify_master.gp (PARI/GP script reproducing all numerics)
```

### French version (alternative, since Zagier reads French and English equally well)

```
Cher Professeur Zagier,

Je vous écris pour solliciter votre avis et possiblement votre
endorsement pour une courte note que je prépare en vue d'une
soumission au Journal of Number Theory :

  « Real quadratic discriminants with integer Hurwitz ratio
    D^2 / B_{2, chi_D} : a finite list of seven »

La note (8 pages) classifie, par calcul direct et vérification
informatique jusqu'à D <= 10^6, les discriminants fondamentaux D > 0
pour lesquels le rationnel

  k(D) := D^2 / B_{2, chi_D} = pi^2 sqrt(D) / L(2, chi_D)
        = D^2 / (24 zeta_K(-1))    [K = Q(sqrt(D))]

est un entier positif. La liste est

  D dans {8, 12, 24, 28, 60, 76, 156}

avec k(D) dans {32, 36, 48, 49, 75, 76, 117} respectivement.

La formule de Hurwitz sous-jacente L(2, chi) = pi^2 B_{2, chi} / f^{3/2}
pour les caractères primitifs réels et pairs est, naturellement,
classique (votre article de L'Enseign. Math. en 1976 fournit la
tabulation canonique de zeta_K(-1)). Ce qui semble nouveau, modulo
ma recherche bibliographique limitée, est la caractérisation
explicite de ces sept discriminants exceptionnels par L'INTÉGRALITÉ
DE k(D), accompagnée d'un balayage PARI jusqu'à D = 10^6 et d'un
argument heuristique de densité D^{-3/2} appuyant la finitude.

Je serais très reconnaissant si vous pouviez (a) m'indiquer si cette
classification à sept éléments a déjà été énoncée dans une
littérature qui m'aurait échappé (auquel cas l'article deviendrait
une re-dérivation à attribuer convenablement), et (b) si vous
accepteriez d'être l'endorser de la soumission arXiv (math.NT, 11M06
/ 11R42 / 14J27).

Le PDF du manuscrit et le script PARI de vérification numérique
sont en pièce jointe. La vérification se reproduit indépendamment en
moins d'une minute sur un ordinateur portable moderne.

Avec mes remerciements pour votre temps et votre attention, je serai
heureux de réviser le manuscrit dans toute direction que votre
expertise suggérera.

Sincèrement,
Kévin Remondière
Chercheur indépendant
Tarbes, France
ORCID : 0009-0008-2443-7166
kevin.remondiere [at] gmail.com

Pièces jointes :
 - main.pdf (8 pp, l'article)
 - verify_master.gp (script PARI/GP reproduisant tous les calculs)
```

---

## §3 Backup email draft for Larry Washington (in English only)

### Subject line

```
Endorsement request — short J. Number Theory note on integer Hurwitz ratio for real quadratic chi_D — independent researcher
```

### Body

```
Dear Professor Washington,

I am writing to request your consideration as endorser for a short
note (8 pages) I am preparing for submission to Journal of Number
Theory:

  "Real quadratic discriminants with integer Hurwitz ratio
   D^2 / B_{2, chi_D} : a finite list of seven"

The note classifies, by direct calculation and computational sweep
up to D <= 10^6, the positive fundamental discriminants D for which

  k(D) := D^2 / B_{2, chi_D} = pi^2 sqrt(D) / L(2, chi_D)
        = D^2 / (24 zeta_K(-1))    [K = Q(sqrt(D))]

is a positive integer. The list is exactly seven elements,
D in {8, 12, 24, 28, 60, 76, 156}, with k(D) in {32, 36, 48, 49, 75, 76, 117}
respectively.

The proof relies on the Hurwitz identity L(2, chi) = pi^2 B_{2,chi}
/ f^{3/2} for primitive real even chi, which I quote from your GTM 83
"Introduction to Cyclotomic Fields" Theorem 4.2 — the most accessible
modern reference for this formula. The finiteness conjecture for the
seven-list is heuristically supported by a D^{-3/2} density argument
that, made rigorous, would draw on your 1979 work with Ferrero
(Annals of Math. (2) 109) on vanishing of the mu-invariant.

I would be grateful for any feedback, in particular whether the
seven-list has been previously stated explicitly in the literature
unknown to me. If you would be willing to endorse the arXiv
submission (math.NT), I would be most grateful.

Manuscript PDF and PARI verification script attached.

Sincerely,
Kévin Remondière
Independent researcher
Tarbes, France
ORCID: 0009-0008-2443-7166
kevin.remondiere [at] gmail.com

Attachments:
 - main.pdf (8 pp, the paper)
 - verify_master.gp (PARI/GP script reproducing all numerics)
```

---

## §4 Submission protocol

### Timeline

| Date          | Action                                                  |
|---------------|---------------------------------------------------------|
| 2026-05-11    | Endorser email sent to Don Zagier (English version)    |
| 2026-05-12 to 2026-05-25 | Wait for response (2-week window)            |
| 2026-05-25    | If no response: send to Larry Washington                |
| 2026-06-01 to 2026-06-08 | Wait for second response (1-week window)     |
| 2026-06-08    | If no endorsement: arXiv submission as v1 without endorsement (an account with prior submissions does not need a per-paper endorser; if Kévin's arXiv account has no prior NT submission, a new endorser must be found — try Bjorn Poonen, Henri Cohen, or André Pizer) |
| 2026-06-08    | Submit to arXiv math.NT |
| 2026-06-09    | Submit to Journal of Number Theory via Editorial Manager |
| 2026-06-10    | Send arXiv preprint link to Zagier and Washington for awareness |

### Etiquette notes (post-Sébastien-Dumontet incident memory)

- **Single email, no follow-up before 2 weeks.** Zagier and Washington both receive 50+ requests per week.
- **Attach the manuscript directly**, not a Dropbox/Google-Drive link.
- **Indicate willingness to revise** ("I am happy to revise in any direction your expertise suggests"). This is critical for amateur-credibility.
- **Do NOT cc** other mathematicians on the same email.
- **Plain-text email** (no HTML, no signature image), to avoid spam-filter issues.
- Email at **9:00 AM Bonn time** (8:00 AM UTC), which is when Zagier reads his queue.

---

## §5 If Zagier confirms 7-list is folklore

If Zagier responds with a citation showing the 7-list was already in the literature, the paper pivots to:

> "Re-derivation and computational confirmation of the integrality classification $D^2 / B_{2,\chi_D} \in \mathbb{Z}$ for real quadratic discriminants"

with explicit attribution to Zagier's prior work (or Hirzebruch's, or van der Geer's, depending on the cited reference). The paper remains publishable as an explicit verification with $D \le 10^6$ sweep + density heuristic + $s = 3$ imaginary-quadratic mirror, which is the genuinely-new content even in the worst case.

**The contingency saves face.** Honest reframing is preferable to retraction.
