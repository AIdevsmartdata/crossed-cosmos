// glueball_correlator.cc
// SU(2) 0++ glueball operator: APE-smeared spatial plaquette per timeslice.
// Output: O(t) = sum_{i<j spatial} sum_{spatial sites} Re tr P_ij(x,t)
//   evaluated on N_smear APE-smeared spatial links (alpha=APE_alpha).
// The temporal correlator C(tau) = <O(0)O(tau)> is computed offline in Python.
//
// Input XML format:
//   <glueball>
//     <nrow>16 16 16 16</nrow>
//     <t_dir>3</t_dir>
//     <APE_alpha>0.5</APE_alpha>
//     <APE_iter>20</APE_iter>
//     <Cfg><cfg_type>SZINQIO</cfg_type><cfg_file>path</cfg_file></Cfg>
//   </glueball>
//
// Output: <Op>O(0) O(1) ... O(L_t-1)</Op>  inside an XML <glueball_output>.
//
// Build: see Makefile.glueball

#include "chroma.h"

using namespace Chroma;

int main(int argc, char *argv[])
{
  Chroma::initialize(&argc, &argv);

  XMLFileWriter& xml_out = Chroma::getXMLOutputInstance();
  push(xml_out, "glueball_correlator");

  // -----------------------------------------------------------------------
  // 1. Parse input
  // -----------------------------------------------------------------------
  if (argc < 3) {
    QDPIO::cerr << "Usage: glueball_correlator -i input.xml -o output.xml" << std::endl;
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
  int APE_iter;
  read(xml_in, "/glueball/APE_iter", APE_iter);
  std::string cfg_file;
  read(xml_in, "/glueball/Cfg/cfg_file", cfg_file);

  Layout::setLattSize(nrow);
  Layout::create();
  const int Lt = nrow[t_dir];

  write(xml_out, "nrow", nrow);
  write(xml_out, "t_dir", t_dir);
  write(xml_out, "APE_alpha", APE_alpha);
  write(xml_out, "APE_iter", APE_iter);
  write(xml_out, "cfg_file", cfg_file);

  // -----------------------------------------------------------------------
  // 2. Read gauge config (SZINQIO == SCIDAC LIME)
  // -----------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u(Nd);
  XMLReader gauge_xml;
  QDPIO::cout << "glueball: reading config " << cfg_file << std::endl;
  readSzinQio(gauge_xml, u, cfg_file);
  QDPIO::cout << "glueball: config read OK" << std::endl;

  // Plaquette sanity check on raw links
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
    QDPIO::cout << "glueball: raw plaquette = " << plaq << std::endl;
  }

  // -----------------------------------------------------------------------
  // 3. APE smearing on SPATIAL links only (preserve gauge invariance in time)
  //    U_mu(x) -> Proj_SU(2)[ (1-alpha) U_mu(x) + alpha/(2(d-1)) * staples ]
  //    where staples are spatial only.  We do APE_iter sweeps.
  // -----------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u_smear(Nd);
  for (int mu = 0; mu < Nd; ++mu) u_smear[mu] = u[mu];

  // helper: spatial staples sum for direction mu (mu != t_dir)
  auto spatial_staple = [&](const multi1d<LatticeColorMatrix>& v, int mu) {
    LatticeColorMatrix S; S = zero;
    for (int nu = 0; nu < Nd; ++nu) {
      if (nu == mu || nu == t_dir) continue;
      // Forward staple: U_nu(x) U_mu(x+nu) U_nu(x+mu)^dagger
      S += v[nu] * shift(v[mu], FORWARD, nu) * adj(shift(v[nu], FORWARD, mu));
      // Backward staple: U_nu(x-nu)^dagger U_mu(x-nu) U_nu(x-nu+mu)
      S += shift(adj(v[nu]) * v[mu] * shift(v[nu], FORWARD, mu), BACKWARD, nu);
    }
    return S;
  };

  const Real one_minus_alpha = Real(1) - APE_alpha;
  // Number of spatial neighbour directions excluding self & time: (Nd - 2) forward
  // staples + (Nd - 2) backward = 2 * (Nd - 2). For Nd=4, t_dir=3, that's 4 staples.
  const Real norm = APE_alpha / Real(2 * (Nd - 2));

  for (int it = 0; it < APE_iter; ++it) {
    multi1d<LatticeColorMatrix> u_new(Nd);
    for (int mu = 0; mu < Nd; ++mu) u_new[mu] = u_smear[mu];
    for (int mu = 0; mu < Nd; ++mu) {
      if (mu == t_dir) continue;  // do not smear temporal links
      LatticeColorMatrix S = spatial_staple(u_smear, mu);
      LatticeColorMatrix V = one_minus_alpha * u_smear[mu] + norm * S;
      // Project back onto SU(2) by polar decomposition: V -> V / sqrt(V^dag V)
      // For SU(2) gauge, this projection is exact via reunitarisation.
      reunit(V);
      u_new[mu] = V;
    }
    u_smear = u_new;
  }

  // Sanity: smeared spatial plaquette should be closer to 1 than raw
  {
    Double sp_pl = 0;
    int npl = 0;
    for (int mu = 0; mu < Nd; ++mu) {
      if (mu == t_dir) continue;
      for (int nu = mu + 1; nu < Nd; ++nu) {
        if (nu == t_dir) continue;
        LatticeColorMatrix P = u_smear[mu] * shift(u_smear[nu], FORWARD, mu)
                              * adj(shift(u_smear[mu], FORWARD, nu)) * adj(u_smear[nu]);
        sp_pl += sum(real(trace(P)));
        ++npl;
      }
    }
    if (npl > 0) {
      Double V = Real(Layout::vol());
      sp_pl /= (V * Real(Nc) * Real(npl));
      write(xml_out, "smeared_spatial_plaquette", sp_pl);
      QDPIO::cout << "glueball: smeared spatial plaq = " << sp_pl << std::endl;
    }
  }

  // -----------------------------------------------------------------------
  // 4. Build 0++ operator O(t) on smeared links: sum over spatial sites of
  //    Re tr P_ij(x,t) for i,j spatial, i<j.
  // -----------------------------------------------------------------------
  Set ts; ts.make(TimeSliceFunc(t_dir));
  multi1d<Double> Op(Lt);
  Op = zero;

  for (int mu = 0; mu < Nd; ++mu) {
    if (mu == t_dir) continue;
    for (int nu = mu + 1; nu < Nd; ++nu) {
      if (nu == t_dir) continue;
      LatticeColorMatrix P = u_smear[mu] * shift(u_smear[nu], FORWARD, mu)
                            * adj(shift(u_smear[mu], FORWARD, nu)) * adj(u_smear[nu]);
      LatticeDouble re_tr = real(trace(P));
      multi1d<Double> ts_sum = sumMulti(re_tr, ts);
      for (int t = 0; t < Lt; ++t) Op[t] += ts_sum[t];
    }
  }

  // -----------------------------------------------------------------------
  // 5. Output O(t)
  // -----------------------------------------------------------------------
  push(xml_out, "Op_t");
  write(xml_out, "Lt", Lt);
  multi1d<double> Op_out(Lt);
  for (int t = 0; t < Lt; ++t) Op_out[t] = toDouble(Op[t]);
  write(xml_out, "O", Op_out);
  pop(xml_out);  // Op_t

  pop(xml_out);  // glueball_correlator
  xml_out.flush();

  QDPIO::cout << "glueball: ran successfully" << std::endl;
  Chroma::finalize();
  return 0;
}
