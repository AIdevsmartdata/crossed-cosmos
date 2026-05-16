// glueball_correlator_GEVP_T2g.cc — T₂g/Eg spin-projected operators for 2⁺⁺ glueball
//
// PURPOSE: Extract m_2++ via GEVP using T₂g and Eg cubic-rep operators built
// from the clover field-strength tensor F_{μν}.  This is P11 design from
// DIGEST_W40_T1_2026-05-16 (bridge Conj E-1 : m_2++²/m_0++² ?= 2).
//
// OPERATORS (3 smearing levels per irrep, GEVP 3×3 per channel):
//   T₂g channel:  OpT2[0..2] = Re T_{xy}   at APE iters {0, 10, 25}
//   Eg  channel:  OpE[0..2]  = Re (T_{xx}-T_{yy}) at APE iters {0, 10, 25}
//
// FIELD STRENGTH CONSTRUCTION:
//   plaq(μ,ν)(x) = U_μ(x) U_ν(x+μ) U_μ†(x+ν) U_ν†(x)
//
//   BUGFIX (P11 line 65): the invalid QDP++ expression
//     Fmunu = (plaq - adj(plaq)) / (2.0 * Real(1.0) * cmplx(Real(0), Real(1)))
//   is replaced with the standard QDP++ idiom:
//     Fmunu = timesMinusI(plaq - adj(plaq)) * Real(0.5)
//   Rationale: dividing by 2i ≡ multiplying by -i/2 = timesMinusI(...) * 0.5.
//   QDP++ does not support operator/(LatticeColorMatrix, Complex) — only Real.
//
// TENSOR:
//   T_{ij}   = Σ_k Tr( F_{ik} F_{kj} )           (full, per colour trace)
//   T_tl{ij} = T_{ij} - (1/3) δ_{ij} Σ_k T_{kk}  (traceless)
//
// PROJECTION:
//   T₂g: T_tl_{xy}  (and cyclic: yz, zx — averaged for statistics)
//   Eg : T_tl_{xx} - T_tl_{yy}
//
// OUTPUT XML (per config):
//   <Op_spin2>
//     <Lt>16</Lt>
//     <n_ops_T2g>3</n_ops_T2g>  <!-- APE levels 0,1,2 -->
//     <n_ops_Eg>3</n_ops_Eg>
//     <OT2_0>val0 ... val15</OT2_0>   <!-- T₂g APE_iter=0  (raw) -->
//     <OT2_1>val0 ... val15</OT2_1>   <!-- T₂g APE_iter=10 -->
//     <OT2_2>val0 ... val15</OT2_2>   <!-- T₂g APE_iter=25 -->
//     <OE_0>val0 ... val15</OE_0>
//     <OE_1>val0 ... val15</OE_1>
//     <OE_2>val0 ... val15</OE_2>
//   </Op_spin2>
//
// BUILD: make -f Makefile.glueball_T2g
// (copy Makefile.glueball_v3, replace SRC target name)

#include "chroma.h"
#include <sstream>
#include <vector>

using namespace Chroma;

// =========================================================================
//  Helper: spatial staple (reuse pattern from glueball_correlator_v3.cc)
// =========================================================================
LatticeColorMatrix spatial_staple_T2g(const multi1d<LatticeColorMatrix>& v,
                                       int mu, int t_dir)
{
  LatticeColorMatrix S;
  S = zero;
  for (int nu = 0; nu < Nd; ++nu) {
    if (nu == mu || nu == t_dir) continue;
    S += v[nu] * shift(v[mu], FORWARD, nu)
               * adj(shift(v[nu], FORWARD, mu));
    S += shift(adj(v[nu]) * v[mu] * shift(v[nu], FORWARD, mu),
               BACKWARD, nu);
  }
  return S;
}

// =========================================================================
//  Helper: APE smearing (spatial only)
// =========================================================================
void ape_smear_T2g(multi1d<LatticeColorMatrix>& u_smear,
                   int t_dir, Real APE_alpha)
{
  const Real one_minus_alpha = Real(1) - APE_alpha;
  const Real norm = APE_alpha / Real(2 * (Nd - 2));

  multi1d<LatticeColorMatrix> u_new(Nd);
  for (int mu = 0; mu < Nd; ++mu) u_new[mu] = u_smear[mu];

  for (int mu = 0; mu < Nd; ++mu) {
    if (mu == t_dir) continue;
    LatticeColorMatrix S = spatial_staple_T2g(u_smear, mu, t_dir);
    LatticeColorMatrix V = one_minus_alpha * u_smear[mu] + norm * S;
    reunit(V);
    u_new[mu] = V;
  }
  u_smear = u_new;
}

// =========================================================================
//  Core: compute T₂g and Eg operators from smeared links
//
//  Returns two timeslice arrays: Op_T2[Lt] and Op_E[Lt].
//
//  F_{μν} is built from the 1×1 clover (plaquette) as:
//    F_{μν} = timesMinusI(P_{μν} - P_{μν}^†) * 0.5
//  This is the standard anti-hermitian projection: (A - A†)/(2i) = -i(A-A†)/2.
//  QDP++ provides timesMinusI(X) = -i * X for LatticeColorMatrix X,
//  which avoids the invalid / cmplx(...) division caught in P11 line 65.
// =========================================================================
void compute_T2g_Eg_operators(const multi1d<LatticeColorMatrix>& u_smear,
                               int t_dir,
                               const Set& ts,
                               int Lt,
                               multi1d<Double>& Op_T2,
                               multi1d<Double>& Op_E)
{
  Op_T2.resize(Lt); Op_T2 = zero;
  Op_E.resize(Lt);  Op_E  = zero;

  // Spatial directions only
  std::vector<int> sdirs;
  for (int d = 0; d < Nd; ++d)
    if (d != t_dir) sdirs.push_back(d);
  const int ns = sdirs.size();  // = 3 for 4D lattice

  // Build F[i][j] for all spatial pairs (i < j), then antisymmetrise
  // Using multi2d indexed by spatial-direction indices 0,1,2 (mapped from sdirs[])
  multi2d<LatticeColorMatrix> F(ns, ns);
  for (int si = 0; si < ns; ++si)
  for (int sj = 0; sj < ns; ++sj)
    F[si][sj] = zero;

  for (int si = 0; si < ns; ++si) {
    int mu = sdirs[si];
    for (int sj = si + 1; sj < ns; ++sj) {
      int nu = sdirs[sj];

      // 1×1 plaquette in plane (mu, nu)
      LatticeColorMatrix plaq =
        u_smear[mu] * shift(u_smear[nu], FORWARD, mu)
        * adj(shift(u_smear[mu], FORWARD, nu)) * adj(u_smear[nu]);

      // ---------------------------------------------------------------
      // FIX for P11 line 65:
      //   BUGGY (QDP++ invalid): (plaq - adj(plaq)) / (2.0 * Real(1.0) * cmplx(Real(0), Real(1)))
      //   FIXED (QDP++ standard): timesMinusI(plaq - adj(plaq)) * Real(0.5)
      //   timesMinusI(X) = -iX, so -i*(P-P†)/2 = (P-P†)/(2i) = F_{μν}
      // ---------------------------------------------------------------
      LatticeColorMatrix Fmunu = timesMinusI(plaq - adj(plaq)) * Real(0.5);

      F[si][sj] =  Fmunu;
      F[sj][si] = -Fmunu;   // antisymmetry F_{νμ} = -F_{μν}
    }
  }

  // Build traceless tensor T_tl_{ij} = Σ_k Tr(F_{ik} F_{kj}) - (1/3)δ_{ij} Σ_kl Tr(F_{kl}²)
  // Using LatticeDouble (real part) since T is Hermitian and we only need Re
  multi2d<LatticeDouble> T_tl(ns, ns);
  for (int i = 0; i < ns; ++i)
  for (int j = 0; j < ns; ++j)
    T_tl[i][j] = zero;

  // Compute T_{ij} = Σ_k Re Tr(F_{ik} F_{kj})
  multi2d<LatticeDouble> T(ns, ns);
  for (int i = 0; i < ns; ++i)
  for (int j = 0; j < ns; ++j) {
    LatticeDouble tij = zero;
    for (int k = 0; k < ns; ++k)
      tij += real(trace(F[i][k] * F[k][j]));
    T[i][j] = tij;
  }

  // Trace: tr_T = T_{00} + T_{11} + T_{22}
  LatticeDouble tr_T = T[0][0] + T[1][1] + T[2][2];

  // Traceless part: T_tl_{ij} = T_{ij} - (1/3) δ_{ij} tr_T
  for (int i = 0; i < ns; ++i)
  for (int j = 0; j < ns; ++j) {
    T_tl[i][j] = T[i][j];
    if (i == j) T_tl[i][j] -= (Real(1) / Real(3)) * tr_T;
  }

  // -----------------------------------------------------------------------
  //  T₂g channel: average of T_tl_{xy}, T_tl_{yz}, T_tl_{zx}
  //  (Cartesian indices: x=sdirs[0], y=sdirs[1], z=sdirs[2])
  // -----------------------------------------------------------------------
  LatticeDouble Op_T2_lat =
    T_tl[0][1] + T_tl[1][2] + T_tl[0][2];  // xy + yz + xz
  // Timeslice sum
  {
    multi1d<Double> ts_sum = sumMulti(Op_T2_lat, ts);
    for (int t = 0; t < Lt; ++t) Op_T2[t] += ts_sum[t];
  }

  // -----------------------------------------------------------------------
  //  Eg channel: T_tl_{xx} - T_tl_{yy}
  //  (Second Eg component 2T_zz - T_xx - T_yy also valid; using first here)
  // -----------------------------------------------------------------------
  LatticeDouble Op_E_lat = T_tl[0][0] - T_tl[1][1];
  {
    multi1d<Double> ts_sum = sumMulti(Op_E_lat, ts);
    for (int t = 0; t < Lt; ++t) Op_E[t] += ts_sum[t];
  }
}

// =========================================================================
//  MAIN
// =========================================================================
int main(int argc, char *argv[])
{
  Chroma::initialize(&argc, &argv);

  XMLFileWriter& xml_out = Chroma::getXMLOutputInstance();
  push(xml_out, "glueball_GEVP_T2g");

  // -------------------------------------------------------------------
  // 1. Parse input XML
  // -------------------------------------------------------------------
  if (argc < 3) {
    QDPIO::cerr << "Usage: glueball_GEVP_T2g -i input.xml -o output.xml"
                << std::endl;
    Chroma::finalize();
    return 1;
  }
  std::string in_file, out_file;
  for (int i = 1; i + 1 < argc; ++i) {
    if (std::string(argv[i]) == "-i") in_file  = argv[i+1];
    if (std::string(argv[i]) == "-o") out_file = argv[i+1];
  }
  XMLReader xml_in(in_file);

  multi1d<int> nrow;
  read(xml_in, "/glueball/nrow", nrow);
  int t_dir;
  read(xml_in, "/glueball/t_dir", t_dir);
  Real APE_alpha;
  read(xml_in, "/glueball/APE_alpha", APE_alpha);
  multi1d<int> APE_iters;     // e.g. {0, 10, 25}
  read(xml_in, "/glueball/APE_iters", APE_iters);
  Cfg_t cfg;
  read(xml_in, "/glueball/Cfg", cfg);

  // Validate
  if (APE_iters.size() < 1) {
    QDPIO::cerr << "Need at least 1 APE iteration level" << std::endl;
    Chroma::finalize();
    return 1;
  }
  const int n_ape_levels = APE_iters.size();   // typically 3: {0, 10, 25}
  int max_ape = 0;
  for (int s = 0; s < n_ape_levels; ++s)
    if (APE_iters[s] > max_ape) max_ape = APE_iters[s];

  Layout::setLattSize(nrow);
  Layout::create();
  const int Lt = nrow[t_dir];

  write(xml_out, "nrow", nrow);
  write(xml_out, "t_dir", t_dir);
  write(xml_out, "APE_alpha", APE_alpha);
  write(xml_out, "APE_iters", APE_iters);
  write(xml_out, "n_ape_levels", n_ape_levels);
  write(xml_out, "cfg_file", cfg.cfg_file);

  // -------------------------------------------------------------------
  // 2. Read gauge config
  // -------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u(Nd);
  XMLReader gauge_file_xml, gauge_xml;
  QDPIO::cout << "GEVP_T2g: reading config " << cfg.cfg_file << std::endl;
  gaugeStartup(gauge_file_xml, gauge_xml, u, cfg);
  QDPIO::cout << "GEVP_T2g: config read OK" << std::endl;

  // -------------------------------------------------------------------
  // 3. Sanity: raw plaquette
  // -------------------------------------------------------------------
  {
    Double plaq = 0;
    int npl = 0;
    for (int mu = 0; mu < Nd; ++mu) {
      for (int nu = mu + 1; nu < Nd; ++nu) {
        LatticeColorMatrix P = u[mu] * shift(u[nu], FORWARD, mu)
                              * adj(shift(u[mu], FORWARD, nu)) * adj(u[nu]);
        plaq += sum(real(trace(P)));
        ++npl;
      }
    }
    Double V = Real(Layout::vol());
    plaq /= (V * Real(Nc) * Real(npl));
    write(xml_out, "raw_plaquette", plaq);
    QDPIO::cout << "GEVP_T2g: raw plaquette = " << plaq << std::endl;
  }

  // -------------------------------------------------------------------
  // 4. Timeslice set
  // -------------------------------------------------------------------
  Set ts;
  ts.make(TimeSliceFunc(t_dir));

  // -------------------------------------------------------------------
  // 5. Storage for T₂g and Eg operators at each APE level
  // -------------------------------------------------------------------
  multi1d< multi1d<Double> > Op_T2_levels(n_ape_levels);
  multi1d< multi1d<Double> > Op_E_levels(n_ape_levels);
  for (int a = 0; a < n_ape_levels; ++a) {
    Op_T2_levels[a].resize(Lt); Op_T2_levels[a] = zero;
    Op_E_levels[a].resize(Lt);  Op_E_levels[a]  = zero;
  }

  // -------------------------------------------------------------------
  // 6. Progressive APE smearing + snapshot at each APE_iters level
  // -------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u_smear(Nd);
  for (int mu = 0; mu < Nd; ++mu) u_smear[mu] = u[mu];

  int next_ape_idx = 0;
  // Handle APE_iters[0] == 0 (raw links, no smearing)
  if (next_ape_idx < n_ape_levels && APE_iters[next_ape_idx] == 0) {
    QDPIO::cout << "GEVP_T2g: snapshot at APE iter 0 (raw)" << std::endl;
    compute_T2g_Eg_operators(u_smear, t_dir, ts, Lt,
                             Op_T2_levels[next_ape_idx],
                             Op_E_levels[next_ape_idx]);
    ++next_ape_idx;
  }

  for (int it = 1; it <= max_ape; ++it) {
    ape_smear_T2g(u_smear, t_dir, APE_alpha);

    if (next_ape_idx < n_ape_levels && it == APE_iters[next_ape_idx]) {
      QDPIO::cout << "GEVP_T2g: snapshot at APE iter " << it << std::endl;
      compute_T2g_Eg_operators(u_smear, t_dir, ts, Lt,
                               Op_T2_levels[next_ape_idx],
                               Op_E_levels[next_ape_idx]);
      ++next_ape_idx;
    }
  }

  // -------------------------------------------------------------------
  // 7. Output XML
  // -------------------------------------------------------------------
  push(xml_out, "Op_spin2");
  write(xml_out, "Lt", Lt);
  write(xml_out, "n_ops_T2g", n_ape_levels);
  write(xml_out, "n_ops_Eg",  n_ape_levels);

  for (int a = 0; a < n_ape_levels; ++a) {
    multi1d<double> T2_out(Lt);
    multi1d<double> E_out(Lt);
    for (int t = 0; t < Lt; ++t) {
      T2_out[t] = toDouble(Op_T2_levels[a][t]);
      E_out[t]  = toDouble(Op_E_levels[a][t]);
    }
    std::stringstream tag_T2, tag_E;
    tag_T2 << "OT2_" << a;
    tag_E  << "OE_"  << a;
    write(xml_out, tag_T2.str(), T2_out);
    write(xml_out, tag_E.str(),  E_out);
  }
  pop(xml_out);  // Op_spin2

  // -------------------------------------------------------------------
  // 8. Metadata
  // -------------------------------------------------------------------
  push(xml_out, "Op_spin2_metadata");
  write(xml_out, "irreps", std::string("T2g Eg"));
  write(xml_out, "field_strength_conv",
        std::string("Fmunu = timesMinusI(plaq - adj(plaq)) * 0.5"));
  write(xml_out, "T2g_component", std::string("T_tl[xy] + T_tl[yz] + T_tl[xz] (cyclic avg)"));
  write(xml_out, "Eg_component",  std::string("T_tl[xx] - T_tl[yy]"));
  write(xml_out, "APE_iters", APE_iters);
  pop(xml_out);  // Op_spin2_metadata

  pop(xml_out);  // glueball_GEVP_T2g
  xml_out.flush();

  QDPIO::cout << "GEVP_T2g: completed successfully" << std::endl;
  Chroma::finalize();
  return 0;
}
