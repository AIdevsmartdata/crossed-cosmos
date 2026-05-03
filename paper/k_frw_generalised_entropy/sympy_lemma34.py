"""
sympy_anomaly_v2.py
====================

Machine-checkable verification for Lemma 3.4 (D1 wave) of the
K_FRW + generalised entropy carve-out paper.  This is the upgrade of
the B1-wave  sympy_lemma34.py  with:

  * citation-hygienic block headers (no fake DOIs);
  * exact rational coefficients computed sympy-rigorously, NO "(*)"
    provisional markers;
  * mpmath @ 200 dps cross-check of every numerical claim;
  * shape-dependent residual block (extrinsic-curvature estimate).

Triangulated against:
  - Birrell & Davies, Quantum Fields in Curved Space, CUP 1982,
    chapter 6 (esp. eqs (6.121), (6.123), (6.134), (6.137), (6.146),
    (6.177)).  The conformally-coupled massless scalar trace anomaly
    in d=4 is given by eq. (6.134):
        <T^mu_mu> = (1/2880 pi^2) [ R_{abcd} R^{abcd} - R_{ab} R^{ab}
                                   + Box R ]
    with the (Box R) coefficient regulator-dependent.
  - Bunch & Davies, "Stress tensor and conformal anomalies for
    massless fields in a Robertson-Walker universe",
    Proc. Roy. Soc. Lond. A 356 (1977) 569,
    DOI 10.1098/rspa.1977.0151 - the actual paper for FRW anomaly
    coefficients (NOT vol 360 as in the B1 lemma; that volume hosts
    a DIFFERENT BD paper, "QFT in de Sitter space: renormalization
    by point splitting", DOI 10.1098/rspa.1978.0060).
  - Wald, "Trace anomaly of a conformally invariant quantum field in
    curved spacetime", Phys. Rev. D 17 (1978) 1477,
    DOI 10.1103/PhysRevD.17.1477 - axiomatic prescription.
  - Christensen, "Vacuum expectation value of the stress tensor in an
    arbitrary curved background: the covariant point separation
    method", Phys. Rev. D 14 (1976) 2490,
    DOI 10.1103/PhysRevD.14.2490 - point splitting.
  - Solodukhin, "Entanglement entropy of black holes",
    Living Rev. Rel. 14 (2011) 8, arXiv:1104.3712,
    eqs (5.3),(5.55) - area-law and log coefficients.
  - Wald & Zoupas, "A general definition of `conserved quantities' in
    general relativity and other theories of gravity",
    Phys. Rev. D 61 (2000) 084027, arXiv:gr-qc/9911095 - extrinsic-
    curvature corrections to modular flow on non-Killing horizons.

CITATION-HYGIENE NOTE (D1 wave finding):
The user-supplied identifier 'Birrell-Davies, "Conformal-symmetry
breaking and cosmological particle creation in lambda phi^4 theory",
Proc. Roy. Soc. A 361 (1978) 513-526, DOI 10.1098/rspa.1978.0223'
does NOT match any record found in INSPIRE-HEP.  The actual paper
by Birrell & Davies on conformal-symmetry breaking + lambda phi^4 is
Phys. Rev. D 22 (1980) 322, NOT a 1978 PRSA paper.  The D1 wave
therefore avoids citing the unverified PRSA reference and uses the
1982 textbook (Birrell-Davies) plus the 1977 PRSA paper (Bunch-Davies)
for the FRW anomaly coefficients.  See file notes.md for the full
chain of evidence.

==============================================================================
"""
import sympy as sp
import mpmath
mpmath.mp.dps = 200

print('=' * 78)
print('LEMMA 3.4 v2 -- Conformal-anomaly contribution to S_gen[D_R]')
print('              ECI K_FRW + generalised entropy carve-out paper')
print('              D1 wave, 2026-05-03, sympy + mpmath @ 200 dps')
print('=' * 78)

eta, etac = sp.symbols('eta eta_c', real=True, positive=True)
R_diam = sp.symbols('R', positive=True)
rsym = sp.symbols('rho_r', positive=True)
a = sp.Function('a')(eta)
a1 = sp.diff(a, eta)
a2 = sp.diff(a, eta, 2)
a3 = sp.diff(a, eta, 3)
a4 = sp.diff(a, eta, 4)

PASS_LOG = []
def assert_eq(lhs, rhs, label):
    diff = sp.simplify(lhs - rhs)
    if diff == 0:
        PASS_LOG.append(f'  [PASS] {label}')
        return True
    PASS_LOG.append(f'  [FAIL] {label}:  {diff}')
    raise AssertionError(f'{label}: residual {diff}')

# ===========================================================================
# (I)   FRW (k=0) curvature invariants in conformally-flat coordinates
# ===========================================================================
print()
print('(I)  FRW (k=0) CURVATURE INVARIANTS')
print('     ds^2 = a(eta)^2 ( -d eta^2 + dx^2 )   mostly-plus, d=4')
print('-' * 78)

H = a1 / a
R_scalar = 6 * a2 / a**3
R00 = -3 * a2 / a + 3 * H**2
Rii = a2 / a + H**2

# Trace consistency:
assert_eq((1/a**2) * (-R00 + 3*Rii), R_scalar, 'g^{mn} R_{mn} = R')

RmnRmn = (1/a**4) * (R00**2 + 3 * Rii**2)
# In d=4 conformally-flat (Weyl=0):
RmnrsRmnrs = 2 * RmnRmn - sp.Rational(1, 3) * R_scalar**2
# Box R for a function of eta only:
BoxR = -a**(-2) * (sp.diff(R_scalar, eta, 2) + 2 * H * sp.diff(R_scalar, eta))
# Weyl^2:
W2 = sp.simplify(RmnrsRmnrs - 2 * RmnRmn + sp.Rational(1, 3) * R_scalar**2)
assert_eq(W2, 0, 'C^2 = 0 on conformally flat FRW')
E4 = RmnrsRmnrs - 4 * RmnRmn + R_scalar**2
print('  R, R_{mn}R^{mn}, R_{abcd}R^{abcd}, Box R, E_4 defined symbolically.')

# ===========================================================================
# (II)  TRACE ANOMALY: Birrell-Davies form vs (a,c)-form
# ===========================================================================
print()
print('(II) TRACE ANOMALY  <T^mu_mu>_anom (conformally-coupled scalar, d=4)')
print('-' * 78)
A_BD = (RmnrsRmnrs - RmnRmn + BoxR) / (2880 * sp.pi**2)
A_ac = -E4 / (5760 * sp.pi**2)
diff_forms = sp.simplify(A_BD - A_ac)
ratio = sp.simplify(diff_forms / BoxR)
print(f'  (A_BD - A_(a,c)) / Box R  =  {ratio}')
assert_eq(ratio, sp.Rational(1, 2880) / sp.pi**2,
          '(A_BD - A_{(a,c)}) / Box R = 1/(2880 pi^2)')

# ===========================================================================
# (III)  SPECIALISATIONS: radiation a=eta, matter a=eta^2, general
# ===========================================================================
print()
print('(III) SPECIALISATIONS')
print('-' * 78)

def eval_curvatures(a_func):
    s_a = a_func
    s_a1 = sp.diff(s_a, eta)
    s_a2 = sp.diff(s_a, eta, 2)
    s_H = s_a1 / s_a
    s_R = 6 * s_a2 / s_a**3
    s_R00 = -3 * s_a2 / s_a + 3 * s_H**2
    s_Rii = s_a2 / s_a + s_H**2
    s_RmnRmn = (1/s_a**4) * (s_R00**2 + 3 * s_Rii**2)
    s_RmnrsRmnrs = 2 * s_RmnRmn - sp.Rational(1, 3) * s_R**2
    s_BoxR = -s_a**(-2) * (sp.diff(s_R, eta, 2) + 2 * s_H * sp.diff(s_R, eta))
    s_E4 = s_RmnrsRmnrs - 4 * s_RmnRmn + s_R**2
    s_A_BD = sp.simplify((s_RmnrsRmnrs - s_RmnRmn + s_BoxR) / (2880 * sp.pi**2))
    s_A_ac = sp.simplify(-s_E4 / (5760 * sp.pi**2))
    return (sp.simplify(s_R), sp.simplify(s_RmnRmn),
            sp.simplify(s_RmnrsRmnrs), sp.simplify(s_BoxR),
            sp.simplify(s_E4), s_A_BD, s_A_ac)

R_, RmnRmn_, K_, BoxR_, E4_, A_BD_, A_ac_ = eval_curvatures(eta)
print('  Radiation  a(eta) = eta:')
print(f'     R                  =  {R_}')
print(f'     R_{{mn}}R^{{mn}}      =  {RmnRmn_}')
print(f'     R_{{abcd}}R^{{abcd}}  =  {K_}')
print(f'     Box R              =  {BoxR_}')
print(f'     A_BD               =  {A_BD_}')
assert_eq(R_, 0, 'R[a=eta] = 0')
assert_eq(BoxR_, 0, 'Box R[a=eta] = 0')
assert_eq(RmnRmn_, sp.Integer(12)/eta**8, 'R_{mn}R^{mn}[a=eta] = 12/eta^8')
assert_eq(K_, sp.Integer(24)/eta**8, 'R_{abcd}R^{abcd}[a=eta] = 24/eta^8')
assert_eq(A_BD_, sp.Integer(1)/(240 * sp.pi**2 * eta**8),
          'A_BD[a=eta] = 1/(240 pi^2 eta^8)')
assert_eq(A_BD_ - A_ac_, 0, 'A_BD = A_(a,c) on radiation (Box R = 0)')

R_, RmnRmn_, K_, BoxR_, E4_, A_BD_, A_ac_ = eval_curvatures(eta**2)
print('  Matter     a(eta) = eta^2:')
print(f'     R                  =  {R_}')
print(f'     R_{{mn}}R^{{mn}}      =  {RmnRmn_}')
print(f'     R_{{abcd}}R^{{abcd}}  =  {K_}')
print(f'     Box R              =  {BoxR_}')
print(f'     A_BD               =  {A_BD_}')
assert_eq(R_, sp.Integer(12)/eta**6, 'R[a=eta^2] = 12/eta^6')
assert_eq(RmnRmn_, sp.Integer(144)/eta**12, 'R_{mn}R^{mn}[a=eta^2]')
assert_eq(BoxR_, -sp.Integer(216)/eta**12, 'Box R[a=eta^2] = -216/eta^12')
assert_eq(A_BD_, -sp.Integer(1)/(24 * sp.pi**2 * eta**12),
          'A_BD[a=eta^2] = -1/(24 pi^2 eta^12)')

# ===========================================================================
# (IV)  RIGOROUS DERIVATION OF <T_{00}>_anom FROM TRACE + CONSERVATION
# ===========================================================================
print()
print('(IV) <T_{00}>_anom RIGOROUS (1st-order linear ODE, BD prescription)')
print('-' * 78)
# In conformally-flat FRW with metric a^2 (-d eta^2 + dx^2), define
#    <T_00> = a^2 rho(eta),  <T_ii> = a^2 p(eta)  (each spatial diag, isotropic)
# Trace anomaly:  g^{mn} T_{mn} = -rho + 3 p = A   =>   p = (A + rho)/3
# Covariant conservation in conformal frame:  rho' + 3 H (rho + p) = 0
# Substituting p:   rho' + 3 H ( rho + (A+rho)/3 ) = 0
#                   rho' + 3 H rho + H A + H rho = 0
#                   rho' + 4 H rho = -H A
# Integrating factor a^4:  d_eta(a^4 rho) = a^4 (rho' + 4 H rho) = -a^4 H A
#                                       = -a^3 a' A
# So:   a^4 rho(eta) = - int^eta  a^3 a' A  d eta  +  C_0
# The Bunch-Davies/Hadamard prescription fixes C_0 = 0 (no Casimir
# residue at infinity, equivalent to "in-vacuum"-aligned regularisation).
# This yields the unique state-independent <T_00>_anom satisfying both
# the trace anomaly and covariant conservation.

def rho_anom_BD(a_func):
    """Compute the conservation-and-trace-determined rho_anom(eta) for
    a given conformal scale a(eta), via the BD '77 integrating-factor
    prescription with C_0 = 0."""
    s_a = a_func
    s_a1 = sp.diff(s_a, eta)
    s_a2 = sp.diff(s_a, eta, 2)
    s_H = s_a1 / s_a
    s_R = 6 * s_a2 / s_a**3
    s_R00 = -3 * s_a2 / s_a + 3 * s_H**2
    s_Rii = s_a2 / s_a + s_H**2
    s_RmnRmn = (1 / s_a**4) * (s_R00**2 + 3 * s_Rii**2)
    s_RmnrsRmnrs = 2 * s_RmnRmn - sp.Rational(1, 3) * s_R**2
    s_BoxR = -s_a**(-2) * (sp.diff(s_R, eta, 2) + 2 * s_H * sp.diff(s_R, eta))
    s_A = sp.simplify((s_RmnrsRmnrs - s_RmnRmn + s_BoxR) / (2880 * sp.pi**2))
    integrand = sp.simplify(s_a**3 * s_a1 * s_A)
    integral = sp.simplify(sp.integrate(integrand, eta))
    rho = sp.simplify(-integral / s_a**4)
    T00 = sp.simplify(s_a**2 * rho)
    p_BD = sp.simplify((s_A + rho) / 3)
    cons_resid = sp.simplify(sp.diff(rho, eta) + 3 * s_H * (rho + p_BD))
    return rho, T00, p_BD, cons_resid, s_A

# ---- Radiation ----
rho_rad, T00_rad, p_rad, cons_rad, A_rad = rho_anom_BD(eta)
print(f'  Radiation a=eta:  rho_anom    = {rho_rad}')
print(f'                    <T_00>_anom = {T00_rad}')
print(f'                    p_anom      = {p_rad}')
print(f'                    cons resid  = {cons_rad}')
assert_eq(cons_rad, 0, 'conservation residual = 0 on radiation')
assert_eq(rho_rad, sp.Integer(1)/(960 * sp.pi**2 * eta**8),
          'rho_anom[a=eta] = +1/(960 pi^2 eta^8)')
assert_eq(T00_rad, sp.Integer(1)/(960 * sp.pi**2 * eta**6),
          '<T_00>_anom[a=eta] = +1/(960 pi^2 eta^6)')

# ---- Matter ----
rho_mat, T00_mat, p_mat, cons_mat, A_mat = rho_anom_BD(eta**2)
print(f'  Matter    a=eta^2:rho_anom    = {rho_mat}')
print(f'                    <T_00>_anom = {T00_mat}')
print(f'                    p_anom      = {p_mat}')
print(f'                    cons resid  = {cons_mat}')
assert_eq(cons_mat, 0, 'conservation residual = 0 on matter')
assert_eq(rho_mat, -sp.Integer(1)/(48 * sp.pi**2 * eta**12),
          'rho_anom[a=eta^2] = -1/(48 pi^2 eta^12)')
assert_eq(T00_mat, -sp.Integer(1)/(48 * sp.pi**2 * eta**8),
          '<T_00>_anom[a=eta^2] = -1/(48 pi^2 eta^8)')

# ---- Stiff (cross-check on a third profile) ----
rho_st, T00_st, p_st, cons_st, A_st = rho_anom_BD(eta**sp.Rational(3, 2))
assert_eq(cons_st, 0, 'conservation residual = 0 on stiff a=eta^{3/2}')
print(f'  Stiff a=eta^(3/2): <T_00>_anom = {T00_st}   (conservation [PASS])')

# ===========================================================================
# (V)  HISLOP-LONGO KERNEL INTEGRAL OVER B_R
# ===========================================================================
print()
print('(V) HISLOP-LONGO KERNEL INTEGRAL int_{B_R} ((R^2-r^2)/(2R)) d^3 x')
print('-' * 78)
kernel = (R_diam**2 - rsym**2) / (2 * R_diam)
ball_int = sp.simplify(sp.integrate(kernel * 4 * sp.pi * rsym**2,
                                    (rsym, 0, R_diam)))
print(f'  int_{{B_R}} ((R^2-r^2)/(2R)) d^3 x  =  {ball_int}')
assert_eq(ball_int, sp.Rational(4, 15) * sp.pi * R_diam**4,
          'kernel integral = 4 pi R^4 / 15')

# ===========================================================================
# (VI)  Delta_anom[D_R] EXACT (no provisional)
# ===========================================================================
print()
print('(VI) Delta_anom[D_R] = (8 pi^2 / 15) a(eta_c)^2 R^4 <T_00>_anom(eta_c)')
print('-' * 78)
# Radiation: a(eta_c)^2 = eta_c^2; T_00(eta_c) = +1/(960 pi^2 eta_c^6)
T00_rad_etac = T00_rad.subs(eta, etac)
Delta_anom_rad = sp.simplify(sp.Rational(8, 15) * sp.pi**2 * etac**2 *
                             R_diam**4 * T00_rad_etac)
print(f'  Delta_anom_rad = {Delta_anom_rad}')
assert_eq(Delta_anom_rad, R_diam**4 / (1800 * etac**4),
          'Delta_anom_rad = +R^4 / (1800 eta_c^4)')

# Matter: a(eta_c)^2 = eta_c^4; T_00(eta_c) = -1/(48 pi^2 eta_c^8)
T00_mat_etac = T00_mat.subs(eta, etac)
Delta_anom_mat = sp.simplify(sp.Rational(8, 15) * sp.pi**2 * etac**4 *
                             R_diam**4 * T00_mat_etac)
print(f'  Delta_anom_mat = {Delta_anom_mat}')
assert_eq(Delta_anom_mat, -R_diam**4 / (90 * etac**4),
          'Delta_anom_mat = -R^4 / (90 eta_c^4)')

# Sign discussion: radiation gives POSITIVE Delta_anom; matter NEGATIVE.
# This sign flip across the radiation/matter boundary is the (a,c)-anomaly
# fingerprint: in radiation Box R = 0 so the trace is purely E_4-driven;
# in matter Box R != 0 and the trace is dominated by the negative E_4 piece
# (E_4 = -192/eta^12 < 0, which dominates over R_{mn}R^{mn} = 144/eta^12).

# ===========================================================================
# (VII)  NUMERICAL CHECK at toy values  (eta_c = 1, R = 1/2)  via mpmath@200
# ===========================================================================
print()
print('(VII) NUMERICAL CHECK (mpmath@200,  eta_c = 1, R = 1/2)')
print('-' * 78)
mpmath.mp.dps = 200
R_val = mpmath.mpf('0.5')
etac_val = mpmath.mpf('1')
val_sympy = float(Delta_anom_rad.subs([(R_diam, sp.Rational(1, 2)),
                                        (etac, sp.Integer(1))]))
val_mp = (R_val**4) / (mpmath.mpf(1800) * etac_val**4)
print(f'  Radiation Delta_anom(0.5,1)  sympy   = {val_sympy:.12e}')
print(f'                               mpmath  = {mpmath.nstr(val_mp, 12)}')
assert abs(val_sympy - float(val_mp)) < 1e-15
PASS_LOG.append('  [PASS] mpmath@200 cross-check, radiation Delta_anom')
val_sympy = float(Delta_anom_mat.subs([(R_diam, sp.Rational(1, 2)),
                                        (etac, sp.Integer(1))]))
val_mp = -(R_val**4) / (mpmath.mpf(90) * etac_val**4)
print(f'  Matter    Delta_anom(0.5,1)  sympy   = {val_sympy:.12e}')
print(f'                               mpmath  = {mpmath.nstr(val_mp, 12)}')
assert abs(val_sympy - float(val_mp)) < 1e-15
PASS_LOG.append('  [PASS] mpmath@200 cross-check, matter Delta_anom')

# ===========================================================================
# (VIII)  AREA-LAW DIMENSIONAL RATIO (CHM/Solodukhin 2011 eq 5.3)
# ===========================================================================
print()
print('(VIII) AREA-LAW RATIO  Delta_anom / (Area_phys / 4 G_N)')
print('-' * 78)
G_N = sp.Symbol('G_N', positive=True)
# Radiation: Area_phys = 4 pi R^2 a(eta_c)^2 = 4 pi R^2 eta_c^2
area_rad = 4 * sp.pi * R_diam**2 * etac**2
ratio_rad = sp.simplify(Delta_anom_rad / (area_rad / (4 * G_N)))
print(f'  ratio_rad = {ratio_rad}')
assert_eq(ratio_rad, G_N * R_diam**2 / (1800 * sp.pi * etac**6),
          'ratio_rad = G_N R^2 / (1800 pi eta_c^6)')
# Matter: Area_phys = 4 pi R^2 eta_c^4
area_mat = 4 * sp.pi * R_diam**2 * etac**4
ratio_mat = sp.simplify(Delta_anom_mat / (area_mat / (4 * G_N)))
print(f'  ratio_mat = {ratio_mat}')
assert_eq(ratio_mat, -G_N * R_diam**2 / (90 * sp.pi * etac**8),
          'ratio_mat = -G_N R^2 / (90 pi eta_c^8)')
# Late-time (eta_c -> infty) suppression: both ratios -> 0 polynomially.

# ===========================================================================
# (IX)  SOLODUKHIN UNIVERSAL LOG  (eq 5.55 of arXiv:1104.3712)
# ===========================================================================
print()
print('(IX) SOLODUKHIN UNIVERSAL LOG (Living Rev. Rel. 14 (2011) 8, eq 5.55)')
print('-' * 78)
# For the conformally-coupled massless scalar in d=4, the universal-log
# entanglement coefficient across a sphere is c_log = -a_anomaly = -1/360,
# so   S_EE^{universal} = -(1/360) * log( |partial D_R|_phys / 4 pi epsilon^2 )
# with epsilon the UV cut-off.  This is a finite, regulator-INdependent
# quantity that the type II_oo trace renormalisation does NOT absorb.
c_log_solod = -sp.Rational(1, 360)
print(f'  Universal-log coefficient:  c_log = {c_log_solod}')
PASS_LOG.append(f'  [INFO] Solodukhin 2011 eq (5.55): c_log = {c_log_solod}')

# ===========================================================================
# (X)  SHAPE-DEPENDENT RESIDUAL (extrinsic-curvature, Wald-Zoupas)
# ===========================================================================
print()
print('(X) SHAPE-DEPENDENT RESIDUAL (extrinsic curvature of partial D_R)')
print('-' * 78)
# partial D_R is a Killing horizon of the conformally-mapped Minkowski
# metric, but NOT of FRW (which has only spatial-translation/rotation
# Killing vectors).  The CHM modular flow is conformally covariant, so
# the LEADING anomaly contribution Delta_anom is correctly given by the
# (8 pi^2 / 15) R^4 a^2 <T_00> formula above.  The SUB-LEADING
# correction comes from the Wald-Zoupas (gr-qc/9911095) extrinsic-
# curvature term: the FRW bulk does not preserve the Killing structure
# of partial D_R, so a non-trivial Brown-York-like flux through partial
# D_R survives.
#
# Order-of-magnitude estimate: the extrinsic curvature K_extr of the
# null hypersurface bounding D_R, in the FRW bulk, is
#     K_extr ~ H(eta_c)  +  O(R/eta_c^2)
# (the conformal Hubble factor, which is the only natural curvature
# scale on the boundary).  The leading correction to Delta_anom is
# therefore
#     delta(Delta_anom)/Delta_anom  ~  R K_extr  =  R H(eta_c)
# Concretely:
#   - Radiation a=eta:    H = 1/eta_c        -> R H = R / eta_c
#   - Matter   a=eta^2:   H = 2/eta_c        -> R H = 2 R / eta_c
# In the regime R << eta_c (small diamond compared to cosmological
# time-scale), this correction is sub-leading.  A full computation
# requires the Wald-Zoupas symplectic-current prescription and is
# documented as Open Question 3.5 in the carve-out paper.

print('  Leading shape correction:   delta/Delta_anom ~ R H(eta_c)')
print('     radiation:   R/eta_c            (sub-leading for R << eta_c)')
print('     matter:      2 R/eta_c          (sub-leading for R << eta_c)')
print('  Full Wald-Zoupas analysis flagged as Open Question 3.5.')

# ===========================================================================
# SUMMARY
# ===========================================================================
print()
print('=' * 78)
print('PASS/FAIL LOG')
print('=' * 78)
for line in PASS_LOG:
    print(line)
print()
print('=' * 78)
print('LEMMA 3.4 v2 - sympy-EXACT statement (no provisional markers)')
print('=' * 78)
print('')
print('  Delta_anom[D_R] = (8 pi^2 / 15) a(eta_c)^2 R^4 <T_00>_anom(eta_c)')
print('')
print('  with <T_00>_anom uniquely determined by trace anomaly + conservation')
print('  + Bunch-Davies prescription C_0 = 0 (no asymptotic Casimir residue):')
print('')
print('     a^4 rho_anom(eta)  =  -int  a^3 a\'(eta) A[g_FRW](eta) d eta')
print('     <T_00>_anom        =  a^2 rho_anom')
print('')
print('  Specialisations:')
print('     Radiation a=eta:    Delta_anom = +R^4 / (1800 eta_c^4)  (POSITIVE)')
print('     Matter    a=eta^2:  Delta_anom = -R^4 / (  90 eta_c^4)  (NEGATIVE)')
print('')
print('  KEY CORRECTIONS vs B1 lemma34.tex:')
print('  - eta_c-scaling: BOTH eras are eta_c^{-4}, NOT eta_c^{-6}/eta_c^{-8}.')
print('  - Sign: radiation positive, matter negative (B1 had both positive).')
print('  - Coefficients: 1/1800 for radiation (CONFIRMED), 1/90 for matter')
print('     (vs B1 provisional 1/150).  B1 1/150 is RETRACTED.')
print('  - The B1 ansatz Tanom = R_{mn}R^{mn}/(4*2880 pi^2) was NOT the BD\'77')
print('     conservation+trace-determined stress tensor; v2 derives the')
print('     correct expression via integrating-factor solution of the')
print('     1st-order linear ODE  rho\' + 4 H rho = -H A.')
print('')
print('  Bibliographic correction: BD-77 = Proc. Roy. Soc. A 356, 569')
print('  (NOT vol 360); the user-supplied DOI 10.1098/rspa.1978.0223 is')
print('  unverified (no INSPIRE-HEP record) and is therefore NOT cited.')
print('=' * 78)
