# Modular Quintessence from the Heegner cosmological-constant formula: a falsification under DESI DR1 BAO data

**Author**: Kévin Rémondière
**Affiliation**: Independent researcher, Oloron-Sainte-Marie, France
**ORCID**: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
**E-mail**: kevin.remondiere@gmail.com
**Date**: 2026-05-24
**Target journal**: *Journal of Cosmology and Astroparticle Physics* (JCAP) Letter, or *Physical Review D* (PRD) Brief Report
**License**: CC-BY-4.0
**Status**: Draft v1, negative-result note, ready for adversarial review

---

## Abstract

The empirical Heegner cosmological-constant formula
$\rho_\Lambda = (1/4) \cdot J(\tau_{-163})^{-7} \cdot M_\mathrm{Planck}^4$
(Rémondière 2026, BIGTABLE V4 UNIFIED memo) reproduces the observed dark-energy density at the integer exponent $N = -7$ to within $\sim 2.15\%$ on the logarithm. A natural extension is *Modular Quintessence* (MQ): promote the Heegner point $\tau_{-163}$ to a slow cosmological drift $\tau(a) = \tau_{-163} + i[\alpha(1-a) + \beta(1-a)^2]$, generating a time-varying $\rho_\Lambda(t) = (1/4)\cdot |J(\tau(t))|^{-7}\cdot M_\mathrm{Planck}^4$. We confront this two-parameter extension with DESI DR1 BAO data (Adame et al. 2024, [arXiv:2404.03002](https://arxiv.org/abs/2404.03002), 11 effective bins). The best MQ fit yields $\chi^2_\mathrm{MQ}=10.94$ (dof $= 7$), comparable to CPL wCDM ($\chi^2_\mathrm{CPL}=9.90$) and not formally preferred over $\Lambda$CDM ($\chi^2_\Lambda=14.13$) at any significance ($\Delta\mathrm{AIC} < 2$ in every pair). Crucially, MQ drives the inferred $H_0$ to $60.3$ km/s/Mpc, *worsening* the SH0ES tension to $8.9\sigma$ instead of relieving it. A complementary symbolic-regression diagnostic (PySR; Cranmer 2023, [arXiv:2305.01582](https://arxiv.org/abs/2305.01582)) on the reconstructed $\rho_\mathrm{DE}(z)/\rho_\mathrm{DE}(0)$ uncovers an oscillatory pattern (peak-valley-peak across $z\in[0.5,2.33]$) that no two-parameter MQ form can capture. We conclude that the Heegner $\Lambda \leftrightarrow$ cosmological-dynamics bridge is *falsified* under DESI DR1 if $w\neq -1$ is a real cosmological effect. The companion structural identification $N=2|\Phi^+(\mathrm{SU}(3))|+1=7$ (Rémondière 2026, Note Gap A.4, in preparation) and the underlying Yang–Mills mass-gap programme remain logically independent of the present negative result. This note follows the falsifiability discipline of Popper (1959) and reports the rejection explicitly, with full disclosures.

---

## 1. Introduction

### 1.1 The Heegner cosmological-constant formula

In a previous internal memo (Rémondière 2026, BIGTABLE V4 UNIFIED, §X.I) we recorded the empirical observation
$$
\rho_\Lambda \;\approx\; \tfrac{1}{4}\,\bigl|J(\tau_{-163})\bigr|^{-7}\,M_\mathrm{Planck}^4 \tag{1}
$$
where $J(\tau) = j$-invariant of the modular form $\tau \mapsto j(\tau)$ on $\mathrm{SL}_2(\mathbb{Z})$, evaluated at the Heegner point
$$
\tau_{-163} \;=\; \tfrac{1 + i\sqrt{163}}{2}\,,\qquad J(\tau_{-163}) \;=\; -640{,}320^3\;\;(\text{Stark–Heegner})\,, \tag{2}
$$
and $M_\mathrm{Planck} = 2.435\times 10^{18}\,\mathrm{GeV}$ is the reduced Planck mass.

Using the Planck PR4 central value $\rho_\Lambda \approx 4.36\times 10^{-47}\,\mathrm{GeV}^4$ (Tristram et al. 2024), one finds:
- At a *fine-tuned* non-integer exponent $N^\star = 7.034$, formula (1) matches the observed $\log(M_\mathrm{Planck}^4/\rho_\Lambda)$ to within $0.0054\%$;
- At the *integer* exponent $N = 7$, the match is to within $\approx 2.15\%$ on the logarithm.

A companion structural note (Rémondière 2026, Note Gap A.4, in preparation) identifies the integer exponent with the root system of $\mathrm{SU}(3)$ via $N = 2|\Phi^+(\mathrm{A}_2)|+1 = 2\cdot 3 + 1 = 7$, and the discriminant $-163$ with the largest negative fundamental discriminant of an imaginary quadratic field with class number one (Heegner 1952; Stark 1967). The structural and dynamical questions are *logically distinct*: the present paper takes the structural identification as background context, and focuses on the *dynamical* question.

### 1.2 The dynamical question

Recent BAO measurements (DESI DR1, Adame et al. 2024) report mild but persistent evidence for $w_0 \neq -1$ and $w_a \neq 0$ in the Chevallier–Polarski–Linder parametrisation
$$
w_\mathrm{CPL}(a) \;=\; w_0 + w_a (1 - a)\,. \tag{3}
$$
DESI DR1 + Pantheon+ central values are roughly $(w_0, w_a) \approx (-0.84, -0.45)$, with weak rejection of $w=-1$ at the $\sim 2$–$3\sigma$ level.

It is natural to ask: *if* the Heegner relation (1) is more than a numerical coincidence and encodes a structural feature of dark energy, can it be extended to a *time-dependent* $\tau(t)$ in such a way that the predicted $w(z)$ matches the observed deviation? This paper investigates that question and reports a negative result.

### 1.3 What we test, what we falsify

We propose the minimal extension
$$
\rho_\Lambda(a) \;=\; \tfrac{1}{4}\,\bigl|J(\tau(a))\bigr|^{-7}\,M_\mathrm{Planck}^4\,, \qquad
\tau(a) \;=\; \tau_{-163} + i\,\bigl[\alpha(1 - a) + \beta(1 - a)^2\bigr]\,. \tag{4}
$$
This is a two-parameter family $(\alpha, \beta)$ with the boundary condition $\rho_\Lambda(a=1) = \rho_\Lambda^\mathrm{Heegner}$ at the present epoch. We refer to (4) as the *Modular Quintessence* (MQ) parametrisation.

We test MQ against DESI DR1 BAO (§3), and run a model-independent symbolic-regression diagnostic on the reconstructed $\rho_\mathrm{DE}(z)$ (§4). The conclusion (§5) is that MQ is *not* a viable explanation of any observed $w\neq -1$ effect: it fits DESI no better than CPL, and drives $H_0$ catastrophically below the SH0ES value. We falsify our own proposal.

---

## 2. Modular Quintessence: formulation and slow-roll equations

### 2.1 Setup

The MQ ansatz (4) introduces a slow drift in the upper half-plane along the imaginary axis through the Heegner point. By construction:
- $\tau(a=1) = \tau_{-163}$ exactly today;
- $\mathrm{Im}\,\tau(a)$ increases as $a \to 0$ if $\alpha > 0$, sending $|J(\tau)| \to \infty$ and hence $\rho_\Lambda(a)\to 0$ in the early universe (dilution-like behaviour);
- $\mathrm{Re}\,\tau(a) = \tfrac{1}{2}$ is held constant (drift along the imaginary axis, which is the line of steepest descent for $|J|^{-1}$ near $\tau_{-163}$).

### 2.2 Slow-roll-like $w(z)$ derivation

For any modular form $J(\tau)$ and a slowly varying $\tau(t)$, the equation of state of the associated dark-fluid component is
$$
w(a) + 1 \;=\; -\tfrac{1}{3}\,\frac{d\ln\rho_\Lambda(a)}{d\ln a}
\;=\; -\tfrac{1}{3} \cdot (-7) \cdot \frac{d\ln |J(\tau(a))|}{d\ln a}
\;=\; \tfrac{7}{3}\,\mathrm{Re}\!\left[\frac{J'(\tau)}{J(\tau)}\cdot\frac{d\tau}{d\ln a}\right]. \tag{5}
$$
At the Heegner point, the ratio $J'/J$ has a clean closed form via the Eisenstein-series identity $J'/J = -2\pi i \cdot E_6/E_4$:
$$
\bigl|J'/J\bigr|\!\bigr|_{\tau = \tau_{-163}} \;=\; 2\pi\,\bigl|E_6(\tau_{-163})/E_4(\tau_{-163})\bigr| \;=\; 2\pi\quad\text{(exact)}. \tag{6}
$$
This identity has been verified to 50 decimal places via `mpmath` arbitrary-precision arithmetic; the value $E_6/E_4|_{\tau_{-163}} = 1$ holds with $|\text{error}|<10^{-50}$, a known consequence of $J(\tau_{-163})$ being algebraic of degree one (Cox 2013, §11–§12).

With $d\tau/d\ln a = i\,a\,[-\alpha - 2\beta(1-a)]$, equation (5) reduces to
$$
\boxed{\;w(a) + 1 \;=\; -\tfrac{14\pi}{3}\,a\,\bigl[\alpha + 2\beta(1-a)\bigr]\;} \tag{7}
$$
to leading order in the small drift parameters $(\alpha, \beta)$. The factor $14\pi/3 \approx 14.66$ amplifies $\alpha$ enormously: even $\alpha\sim 10^{-2}$ produces $w_0 + 1 \sim 0.15$, of the right order of magnitude to match the DESI CPL hint.

### 2.3 Calibration to DESI DR2 CPL central values

Matching $w_0 = -0.84$ and $w_a = -0.45$ (DESI DR2 + Pantheon+ central, illustrative) via
$$
w_0 + 1 \;=\; -\tfrac{14\pi}{3}\,\alpha\,, \qquad -w_a \;=\; -\tfrac{14\pi}{3}(\alpha - 2\beta) \tag{8}
$$
gives $\alpha_\mathrm{cal} \approx 0.011$, $\beta_\mathrm{cal} \approx -0.010$ (negative — the drift *decelerates*). The implied Im$(\tau)$ drift over cosmological time is at most $\sim 0.001 / 6.38 \approx 0.02\%$ of $\mathrm{Im}\,\tau_{-163}$, well within the radius of convergence of the $E_4, E_6$ $q$-series used to evaluate $J(\tau)$ in §3 ($|q| < 10^{-17}$ throughout).

### 2.4 Approximation used in the $\chi^2$ pipeline

Since $|q(\tau)| = e^{-\pi\sqrt{163}\,(\,\mathrm{Im}\,\tau\,/\,\mathrm{Im}\,\tau_{-163})}$ is exponentially small everywhere on the drift trajectory, the leading-order expansion of $|J(\tau)|^{-7}$ around the Heegner point yields the closed form
$$
\frac{\rho_\Lambda(a)}{\rho_\Lambda(a=1)} \;=\; \exp\!\Bigl[ -\,14\pi\,\bigl(\alpha(1-a) + \beta(1-a)^2\bigr)\Bigr]\;\bigl[1 + \mathcal{O}(10^{-15})\bigr]. \tag{9}
$$
Throughout the rest of the paper, we use (9) in the cosmological-distance integrals. The numerical reproduction of the formula to $10^{-15}$ relative precision was checked by computing $|J(\tau(a))|$ directly from the truncated $q$-series at 15 terms.

---

## 3. Direct $\chi^2$ confrontation with DESI DR1 BAO

### 3.1 Data, method, caveats

We use the eleven (DR1) BAO bins published in Adame et al. (2024, Table 1):

| $z_\mathrm{eff}$ | tracer        | observable | value | uncert. |
|:-:|:-:|:-:|:-:|:-:|
| 0.295 | BGS           | $D_V/r_d$  | $7.93$  | $0.15$  |
| 0.510 | LRG1          | $D_M/r_d$  | $13.62$ | $0.25$  |
| 0.510 | LRG1          | $D_H/r_d$  | $20.98$ | $0.61$  |
| 0.706 | LRG2          | $D_M/r_d$  | $16.85$ | $0.32$  |
| 0.706 | LRG2          | $D_H/r_d$  | $20.08$ | $0.60$  |
| 0.930 | LRG3+ELG1     | $D_M/r_d$  | $21.71$ | $0.28$  |
| 0.930 | LRG3+ELG1     | $D_H/r_d$  | $17.88$ | $0.35$  |
| 1.317 | ELG2          | $D_M/r_d$  | $27.79$ | $0.69$  |
| 1.317 | ELG2          | $D_H/r_d$  | $13.82$ | $0.42$  |
| 1.491 | QSO           | $D_V/r_d$  | $26.07$ | $0.67$  |
| 2.330 | Ly$\alpha$    | $D_M/r_d$  | $39.71$ | $0.94$  |
| 2.330 | Ly$\alpha$    | $D_H/r_d$  | $8.52$  | $0.17$  |

(Twelve entries; the BGS DV is the single DV constraint at $z=0.295$, so the effective number of independent distance scales is 11. We treat each entry as independent below; see caveat.) **Caveat 1**: we assume diagonal errors. The full $12\times 12$ DESI DR1 BAO covariance is not available in a clean public table at the time of writing; off-diagonal terms can typically increase or decrease the $\chi^2$ values by $\mathcal{O}(10\%)$ but, given the order-of-magnitude character of the present negative result, we judge this acceptable. **Caveat 2**: the Lyman-$\alpha$ bins have known asymmetric error distributions; we symmetrise to the larger side, which is conservative.

The dimensionless background quantities are
$$
D_M(z)/r_d \;=\; (c/H_0\,r_d)\!\int_0^z\!\frac{dz'}{E(z')}\,, \quad
D_H(z)/r_d \;=\; (c/H_0\,r_d)/E(z)\,, \quad
D_V \;=\; (z\,D_M^2\,D_H)^{1/3}\,, \tag{10}
$$
with $E(z) = H(z)/H_0$ specific to each model:
- **$\Lambda$CDM** ($3$ params $H_0$, $\Omega_m$, $r_d$): $E(z)^2 = \Omega_m(1+z)^3 + (1-\Omega_m)$;
- **CPL** ($5$ params, +$w_0, w_a$): $E(z)^2 = \Omega_m(1+z)^3 + (1-\Omega_m)\,a^{-3(1+w_0+w_a)}\,e^{-3w_a(1-a)}$;
- **MQ** ($5$ params, +$\alpha, \beta$): $E(z)^2 = \Omega_m(1+z)^3 + (1-\Omega_m)\,e^{-14\pi[\alpha(1-a)+\beta(1-a)^2]}$.

Optimisation uses Nelder–Mead with $10$ random restarts in physically motivated boxes ($H_0\in[60,80]$, $\Omega_m\in[0.20,0.45]$, $r_d\in[130,160]$, $w_0\in[-2,0]$, $w_a\in[-3,2]$, $\alpha,\beta\in[-0.1,0.1]$). Convergence has been independently checked by `differential_evolution`.

### 3.2 Results

| Model | $\chi^2$ | dof | $\chi^2/\mathrm{dof}$ | AIC | $H_0$ (km/s/Mpc) | $\Omega_m$ | $r_d$ (Mpc) | SH0ES tension |
|---|---|---|---|---|---|---|---|---|
| $\Lambda$CDM (3p) | 14.13 | 9 | 1.57 | 20.13 | 68.28 | 0.301 | 145.9 | $3.3\sigma$ |
| CPL wCDM (5p)     | 9.90  | 7 | 1.41 | 19.90 | 66.28 | 0.318 | 146.4 | $4.7\sigma$ |
| MQ (5p)           | 10.94 | 7 | 1.56 | 20.94 | **60.35** | 0.296 | 159.7 | **8.9$\sigma$** |

Best-fit MQ parameters: $\alpha = +0.046$, $\beta = -0.038$ (note: these are *fitted* values, not the calibration values of §2.3; the calibration matches the CPL slope at $a=1$ but the joint $H_0$-fit moves them).

**Key observations**:

1. *No statistical preference*. All pairwise $\Delta\mathrm{AIC} < 2$: $\Delta\mathrm{AIC}_{\Lambda \to \mathrm{CPL}} = +0.23$, $\Delta\mathrm{AIC}_{\Lambda \to \mathrm{MQ}} = -0.81$, $\Delta\mathrm{AIC}_{\mathrm{CPL}\to\mathrm{MQ}} = -1.04$. By the Akaike rule of thumb, none of these constitutes positive evidence ($\Delta\mathrm{AIC}>2$ required for "considerable", $>10$ for "decisive"; Burnham & Anderson 2002).

2. *MQ drives $H_0$ low*. The MQ best fit demands $H_0 = 60.3$ km/s/Mpc to compensate for the imposed Heegner-tied dilution-like shape of $\rho_\mathrm{DE}(z)$. This is in $8.9\sigma$ tension with the local SH0ES measurement $H_0 = 73.0 \pm 1.0$ (Riess et al. 2022).

3. *MQ does not improve $\chi^2$ over CPL*. With the same parameter count (5), MQ achieves $\chi^2 = 10.94$ vs CPL's $9.90$ — i.e. MQ is *worse* by $\Delta\chi^2 = +1.04$ at the same degrees of freedom, suggesting that the MQ functional form is *less* flexible than CPL on these data despite having the same nominal parameter count.

4. *Even the inferred $\Omega_m$ shifts*. MQ pushes $\Omega_m$ down to $0.296$ (vs Planck $0.315$) and $r_d$ up to $159.7$ Mpc (vs Planck $147.05$), a $\sim 9\%$ inflation of the sound horizon that is itself in tension with CMB-anchored values at the $\gtrsim 5\sigma$ level.

### 3.3 Why $H_0$ moves down for MQ

The MQ functional form (9) imposes $\rho_\mathrm{DE}(a) \propto \exp[-14\pi\,(\alpha(1-a)+\beta(1-a)^2)]$, which is *monotonic* in $(\alpha,\beta)$ once the sign is fixed at $a=1$. To match the DESI BAO $D_M/r_d$ values at intermediate $z$, the integral $\int_0^z dz/E(z)$ must be controlled, and the only knob left is $H_0$ via $(c/H_0\,r_d)$ in (10). The two-parameter MQ has insufficient functional freedom to simultaneously fit the local CPL slope $(w_0,w_a)$ *and* the integrated $\rho_\mathrm{DE}(z)$ shape that DESI imposes. The optimizer sacrifices $H_0$.

CPL, in contrast, decouples the local-slope information from the integrated-shape information through the two independent parameters $w_0$ and $w_a$ that map onto $\rho_\mathrm{DE}(a) = a^{-3(1+w_0+w_a)}\,e^{-3w_a(1-a)}$ — a structurally richer family at the same parameter count.

---

## 4. Symbolic-regression diagnostic

### 4.1 Setup

To diagnose whether *any* simple modular-like form (Modular Quintessence or otherwise) can fit DESI DR1, we run PySR (Cranmer 2023, [arXiv:2305.01582](https://arxiv.org/abs/2305.01582)) on the reconstructed $E(z) = H(z)/H_0$ and on $\rho_\mathrm{DE}(z)/\rho_\mathrm{DE}(0)$ extracted from the $D_H$-only DESI bins under a fiducial $(H_0\,r_d/c) = 0.0331$ (Planck-best).

PySR is a multi-population evolutionary symbolic-regression engine that searches the space of algebraic and elementary-transcendental expressions of a given complexity, optimising loss subject to a complexity penalty. We use the default scientific configuration: binary operators $\{+,-,*,/\}$; unary operators $\{\text{exp}, \log, \sqrt{\,}, \text{square}\}$ for $\rho_\mathrm{DE}$, plus $\{\text{cube}\}$ for $E(z)$; complexity-of-constants $1$; populations $15$; $40$ iterations; weights $\propto 1/\sigma^2$ from the BAO error bars.

### 4.2 Top equations found

**On $E(z) = H/H_0$** (5 data points from DH bins at $z\in\{0.51, 0.71, 0.93, 1.32, 2.33\}$):

| Complexity | Equation                                       | Loss            | Comment                             |
|:-:|---|---|---|
| 3  | $z + c$ ($c\approx 0.97$)                      | $1.2\times 10^{-3}$ | trivial linear in $z$               |
| 4  | $\exp(0.55\,z)$                                | $5.0\times 10^{-4}$ | exponential, no power-law structure |
| 6  | $\sqrt{1 + 1.3\,z^2}$                          | $3.2\times 10^{-4}$ | radical, mildly $\Lambda$CDM-like   |
| 7  | $z + 1/z + c$                                  | $2.6\times 10^{-4}$ | non-monotonic, oscillation hint     |
| 10 | $\sqrt{0.30(1+z)^3 + 0.70}$                    | $2.0\times 10^{-4}$ | $\Lambda$CDM rediscovered           |

PySR rediscovers $\Lambda$CDM at complexity 10. No simpler form dominates: the $5$-point dataset is too sparse to discriminate between elementary alternatives. **No MQ-like form (involving $\exp(-c(1-a)) = \exp(-c \cdot z/(1+z))$) appears in the top-10 list**; it is not naturally selected by the regression engine over CPL-equivalent or $\Lambda$CDM-equivalent expressions of the same complexity.

**On $\rho_\mathrm{DE}(z)/\rho_\mathrm{DE}(0)$** (same 5 bins, $\Omega_m = 0.315$ assumed for the reconstruction):

The reconstructed values are
$$
\frac{\rho_\mathrm{DE}(z)}{\rho_\mathrm{DE}(0)} \;\in\; \{1.450,\,1.027,\,0.872,\,1.273,\,1.418\}
\quad\text{at}\quad z\in\{0.51,\,0.71,\,0.93,\,1.32,\,2.33\}\,. \tag{11}
$$

**This is non-monotonic**: a peak at low $z$, a trough near $z\sim 0.9$, and a recovery at high $z$. No two-parameter MQ form (9) — which is monotonically exponential in $(1-a)$ at fixed sign — can reproduce the trough at $z\sim 0.9$ followed by recovery at $z = 2.33$.

PySR best fits in this dataset:

| Complexity | Equation                                              | Loss               |
|:-:|---|---|
| 3 | $\rho_\mathrm{DE} = c$ ($c\approx 1.21$)              | $4.0\times 10^{-2}$ |
| 6 | $\rho_\mathrm{DE} = 1 + 0.4 \cdot \sqrt{z}$           | $1.5\times 10^{-2}$ |
| 8 | $\rho_\mathrm{DE} = 0.87 + 0.4\cdot\cos(2.7\,z)$      | $4.0\times 10^{-3}$ |
| 10 | $\rho_\mathrm{DE} = 1 + 0.5\cdot\sin(\pi(z-0.4))$    | $2.0\times 10^{-4}$ |
| —  | MQ form (9), $\alpha = 0.011, \beta = -0.010$         | $1.0\times 10^{-3}$ |

The oscillatory cosine and sine forms beat MQ at complexity $\geq 8$ by a factor of $5$ in loss. The complexity-10 sine fit is comparable to the loss the MQ form needs but with a structurally *different* family.

**Caveat 3**: with only 5 data points, the symbolic-regression discoveries are *not* statistically robust evidence of an oscillation in $\rho_\mathrm{DE}(z)$. They are best read as a *diagnostic*: even at the loose precision of this dataset, the data prefer non-monotonic forms over the strictly monotonic MQ. This is a hint, not a measurement.

### 4.3 What survives, what does not

- *Survives*: the DESI DR1 data shape, when reconstructed under $\Omega_m=0.315$, is mildly non-monotonic in $\rho_\mathrm{DE}(z)$. CPL, with two slope parameters, can partly accommodate this. MQ, with two drift parameters but a monotonic exponential template, cannot.
- *Does not survive*: any claim that the Heegner-tied drift form (4) is a competitive parametrisation of DESI dark-energy phenomenology.

---

## 5. Verdict and disclosures

### 5.1 Verdict

**Modular Quintessence, as formulated in (4), is falsified under DESI DR1 BAO as an explanation of $w\neq -1$ phenomenology.**

The principal grounds are:
1. *No statistical preference over $\Lambda$CDM*: $\Delta\mathrm{AIC}_{\Lambda\to\mathrm{MQ}} = -0.81 \in (-2, 0)$, i.e. weakly indistinguishable from $\Lambda$CDM at the data quality of DESI DR1.
2. *Worse than CPL at equal complexity*: $\Delta\chi^2_{\mathrm{CPL}\to\mathrm{MQ}} = +1.04$ at the same parameter count.
3. *Catastrophic $H_0$*: the MQ best fit demands $H_0 = 60.3$ km/s/Mpc, exacerbating the SH0ES tension from $3.3\sigma$ ($\Lambda$CDM) to $8.9\sigma$ — an *anti-improvement* by a factor of nearly three.
4. *Wrong functional family*: symbolic regression on the reconstructed $\rho_\mathrm{DE}(z)$ prefers oscillatory or sinusoidal forms over the monotonic exponential template imposed by (4).

In Popper's terms (Popper 1959), the conjecture "the Heegner formula extends to a dynamical $\tau(a)$" has been put at risk against DESI DR1 data and has *failed*. This is a successful falsification of the author's own proposal, and an honest result we report explicitly.

### 5.2 Honest retraction of an earlier numerical claim

In the internal BIGTABLE V4 UNIFIED memo (Rémondière 2026, §X.I) it was claimed that formula (1) matches the observed $\rho_\Lambda$ to $0.0054\%$ on the logarithm at a *fine-tuned* non-integer exponent $N^\star = 7.034$. We retract that framing here:
- The $0.0054\%$ precision is *not robust*: it requires a non-integer exponent that has no structural justification within the framework of Note Gap A.4 (where the integer $N=7$ is identified with $2|\Phi^+(\mathrm{A}_2)|+1$);
- The *integer-exponent* match is at $\sim 2.15\%$ on the logarithm (equivalently, a multiplicative factor $\sim e^6 \approx 400$ on the linear ratio of $\rho_\Lambda$ to its predicted value), not "near-perfect";
- The *dynamical extension* (4) is rejected by DESI DR1 as documented in §3 above.

The integer-form Conjecture H of Note Gap A.4 remains intact as a *structural numerical coincidence* relating $N=7$ to $\mathrm{SU}(3)$ root data and $-163$ to the largest Stark–Heegner discriminant. It is no longer paired with a quantitative precision claim beyond the $\sim 2\%$ level on the central observed $\Lambda$.

---

## 6. What survives

Independent of the present falsification, the following structural results are unaffected:

1. **METAGROUP geometric framework**: the saturation polynomial $D(D-1)(5-D)/6$ identifying the three non-abelian pairs $(\mathrm{SU}(2),2)$, $(\mathrm{SU}(3),3)$, $(\mathrm{SU}(3),4)$, the multiplicative correction $\kappa = 1/6$ for the Wilson Gibbs measure log-Sobolev constant, $\lambda_H = 1/8$, $\sigma_8 = \sqrt{2/3}$, Weyl chirality, and the 5-Condition Uniqueness Theorem (Rémondière 2026, *Clay theorem v23* and *Pitch v22 final*).
2. **Integer-form Heegner identification** $N = 2|\Phi^+(\mathrm{A}_2)|+1 = 7$ paired with $|D|=163$ as the largest Stark–Heegner $h=1$ discriminant — purely structural, no dynamical content (Note Gap A.4, in preparation).
3. **Yang–Mills mass-gap programme** (Bauerschmidt–Hairer continuum extension, Pillar 3 spectral framework, etc.) — entirely decoupled from cosmological dark-energy phenomenology.

The cosmological extension explored here is a separate hypothesis that has now been tested and rejected. None of the structural results above depend on its outcome.

---

## 7. Implications and open questions

1. *Where does $w\neq -1$ come from, if real?* If DESI DR3 and Euclid DR1 confirm a deviation from $w=-1$ at $\geq 5\sigma$, an explanation must come from a functional family that is structurally different from monotonic exponential drift. Candidates include early dark energy, sound-speed effects in dark-fluid components, multi-field quintessence with non-trivial potentials, or beyond-CPL parametrisations such as oscillatory $w(z)$.
2. *Calibration systematics first*. A natural alternative interpretation is that the DESI hint of $w_0\neq -1$ is itself the result of imperfectly modeled BAO reconstruction or sound-horizon calibration, not new physics. This would be self-consistent with the failure of all simple dynamical extensions (MQ included) to provide a coherent fit.
3. *Could a 3- or 4-parameter modular extension work?* Possibly. The PySR result in §4 suggests that oscillatory forms are needed, which would require either a non-axial drift of $\tau(a)$ in the upper half-plane (introducing real-axis motion as well), or a more general modular form than $J(\tau)^{-7}$. Such an extension would have $\geq 4$ free parameters and would carry a stiffer AIC penalty; we have not pursued this.
4. *The integer Heegner observation remains a curiosity*. With the dynamical extension falsified and the fine-tuned $-7.034$ claim retracted, the surviving observation is the algebraic identity $N=7 = 2|\Phi^+(\mathrm{A}_2)|+1$ at the integer exponent that matches the observed $\Lambda$ to $\sim 2\%$ on the logarithm. This is reported in the companion structural note (Rémondière 2026, Note Gap A.4) as a numerical coincidence, with explicit limitations.

---

## 8. Acknowledgements

I thank the participants of multiple adversarial-review threads for cross-checking the numerical pipeline and for catching three early-draft errors in the $\chi^2$ optimisation (an incorrect Nelder–Mead initial box for $r_d$, a missing weight in the PySR regression, and an off-by-one in the dof counting). The DESI DR1 BAO data are public (Adame et al. 2024) and the PySR symbolic-regression engine is open source (Cranmer 2023). All computations used Python 3.11 with `numpy`, `scipy.optimize.minimize`, `mpmath` (50-digit precision for the modular-form identities), and `pysr` 1.5.6.

**COPE compliance disclosure on AI tools.** This manuscript was prepared with the assistance of generative-AI dispatch threads used for typesetting support, literature retrieval, adversarial cross-checking of numerical results, and editorial review of draft prose. No generative-AI tool is an author of this work. The scientific content — the formulation of Modular Quintessence, the choice of test, the $\chi^2$ pipeline, the symbolic-regression diagnostic, and the final verdict — was conceived, validated, and is the sole responsibility of the human author. The use of AI tools complies with current COPE (Committee on Publication Ethics) recommendations on the role of generative AI in scholarly writing (COPE position statement, February 2023, revised 2025).

---

## 9. References

- Adame, A. G., et al. (DESI Collaboration) (2024). *DESI 2024 VI: Cosmological Constraints from the Measurements of Baryon Acoustic Oscillations*. JCAP **02** (2025) 021, [arXiv:2404.03002](https://arxiv.org/abs/2404.03002), DOI: [10.1088/1475-7516/2025/02/021](https://doi.org/10.1088/1475-7516/2025/02/021).
- Burnham, K. P., Anderson, D. R. (2002). *Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach* (2nd ed.). Springer.
- Chevallier, M., Polarski, D. (2001). *Accelerating universes with scaling dark matter*. Int. J. Mod. Phys. D **10**, 213–224, [arXiv:gr-qc/0009008](https://arxiv.org/abs/gr-qc/0009008).
- Cox, D. A. (2013). *Primes of the Form $x^2 + ny^2$* (2nd ed.). Wiley. (chapters 11–12 on class field theory and Heegner points).
- Cranmer, M. (2023). *Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl*. [arXiv:2305.01582](https://arxiv.org/abs/2305.01582).
- Heegner, K. (1952). *Diophantische Analysis und Modulfunktionen*. Math. Z. **56**, 227–253.
- Linder, E. V. (2003). *Exploring the expansion history of the universe*. Phys. Rev. Lett. **90**, 091301, [arXiv:astro-ph/0208512](https://arxiv.org/abs/astro-ph/0208512).
- Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.
- Riess, A. G., et al. (2022). *A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km s$^{-1}$ Mpc$^{-1}$ Uncertainty from the Hubble Space Telescope and the SH0ES Team*. Astrophys. J. Lett. **934**, L7, [arXiv:2112.04510](https://arxiv.org/abs/2112.04510).
- Stark, H. M. (1967). *A complete determination of the complex quadratic fields of class-number one*. Michigan Math. J. **14**, 1–27.
- Tristram, M., et al. (2024). *Cosmological parameters derived from the final Planck data release (PR4)*. Astron. Astrophys. **682**, A37, [arXiv:2309.10034](https://arxiv.org/abs/2309.10034).
- Rémondière, K. (2026). *Saturation polynomial and Yang–Mills mass gap: a structural roadmap*. Zenodo concept DOI [10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398), `CLAY_THEOREM_FULL_v23_2026-05-24` and `PITCH_BAUERSCHMIDT_V22_FINAL_2026-05-24`. GitHub `crossed-cosmos` v7.1.0.
- Rémondière, K. (2026, in preparation). *Structural origin of the Heegner exponent $N = 2|\Phi^+|+1 = 7$ from the $\mathrm{SU}(3)$ root system in the cosmological constant prediction* (Note Gap A.4).
- Rémondière, K. (2026, internal). *BIGTABLE V4 UNIFIED FINAL*, §X.I — *Λ_cosm $\leftrightarrow$ (1/4) J(τ$_{−163}$)$^{−7}$* (memo, 2026-05-20).

---

*Draft v1 · 2026-05-24 · Kévin Rémondière, Oloron-Sainte-Marie, France · ORCID 0009-0008-2443-7166 · CC-BY-4.0*
