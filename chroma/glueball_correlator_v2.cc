// glueball_correlator_v2.cc
// SU(2) 0++ glueball operator with MULTI-SMEARING basis for GEVP analysis.
//
// Differences from v1:
//   - APE_iter_list (XML) instead of scalar APE_iter — emits <O_smear_K> per level
//   - Cumulative smearing: do 40 sweeps total, snapshot O(t) at iters {10, 20, 40}
//   - Output basis: {O_K(t) : K in APE_iter_list} for 1×1 spatial plaquette
//
// Input XML format:
//   <glueball>
//     <nrow>16 16 16 16</nrow>
//     <t_dir>3</t_dir>
//     <APE_alpha>0.5</APE_alpha>
//     <APE_iter_list>10 20 40</APE_iter_list>   <-- changed
//     <Cfg><cfg_type>SZINQIO</cfg_type><cfg_file>path</cfg_file></Cfg>
//   </glueball>
//
// Output:  <Op_t><Lt>...</Lt><O_smear_10>...</O_smear_10><O_smear_20>...
//          <O_smear_40>...</Op_t>

#include "chroma.h"

using namespace Chroma;

namespace {

// Compute O_plaq(t) summed over spatial sites and i<j spatial pairs.
// Stored into the (level_idx, t) row of `Op` (multi2d-like via multi1d of multi1d).
void compute_O_plaq(const multi1d<LatticeColorMatrix>& u_smear,
                    int t_dir, const Set& ts, int Lt,
                    multi1d<Double>& Op_level)
{
  Op_level = zero;
  for (int mu = 0; mu < Nd; ++mu) {
    if (mu == t_dir) continue;
    for (int nu = mu + 1; nu < Nd; ++nu) {
      if (nu == t_dir) continue;
      LatticeColorMatrix P = u_smear[mu] * shift(u_smear[nu], FORWARD, mu)
                            * adj(shift(u_smear[mu], FORWARD, nu)) * adj(u_smear[nu]);
      LatticeDouble re_tr = real(trace(P));
      multi1d<Double> ts_sum = sumMulti(re_tr, ts);
      for (int t = 0; t < Lt; ++t) Op_level[t] += ts_sum[t];
    }
  }
}

}  // anon namespace


int main(int argc, char *argv[])
{
  Chroma::initialize(&argc, &argv);

  XMLFileWriter& xml_out = Chroma::getXMLOutputInstance();
  push(xml_out, "glueball_correlator_v2");

  // -----------------------------------------------------------------------
  // 1. Parse input
  // -----------------------------------------------------------------------
  if (argc < 3) {
    QDPIO::cerr << "Usage: glueball_correlator_v2 -i input.xml -o output.xml" << std::endl;
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
  multi1d<int> APE_iter_list;
  read(xml_in, "/glueball/APE_iter_list", APE_iter_list);
  Cfg_t cfg;
  read(xml_in, "/glueball/Cfg", cfg);

  Layout::setLattSize(nrow);
  Layout::create();
  const int Lt = nrow[t_dir];

  // Smearing schedule must be sorted ascending
  for (int s = 1; s < APE_iter_list.size(); ++s) {
    if (APE_iter_list[s] <= APE_iter_list[s-1]) {
      QDPIO::cerr << "APE_iter_list must be strictly ascending" << std::endl;
      Chroma::finalize();
      return 1;
    }
  }
  const int n_levels = APE_iter_list.size();
  const int max_iter = APE_iter_list[n_levels - 1];

  write(xml_out, "nrow", nrow);
  write(xml_out, "t_dir", t_dir);
  write(xml_out, "APE_alpha", APE_alpha);
  write(xml_out, "APE_iter_list", APE_iter_list);
  write(xml_out, "cfg_file", cfg.cfg_file);

  // -----------------------------------------------------------------------
  // 2. Read gauge config via unified gaugeStartup
  // -----------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u(Nd);
  XMLReader gauge_file_xml, gauge_xml;
  QDPIO::cout << "glueball_v2: reading config " << cfg.cfg_file << std::endl;
  gaugeStartup(gauge_file_xml, gauge_xml, u, cfg);
  QDPIO::cout << "glueball_v2: config read OK" << std::endl;

  // Plaquette sanity on raw links
  {
    Double plaq = 0; int npl = 0;
    for (int mu = 0; mu < Nd; ++mu)
      for (int nu = mu + 1; nu < Nd; ++nu) {
        LatticeColorMatrix P = u[mu] * shift(u[nu], FORWARD, mu)
                              * adj(shift(u[mu], FORWARD, nu)) * adj(u[nu]);
        plaq += sum(real(trace(P))); ++npl;
      }
    Double V = Real(Layout::vol());
    plaq /= (V * Real(Nc) * Real(npl));
    write(xml_out, "raw_plaquette", plaq);
    QDPIO::cout << "glueball_v2: raw plaquette = " << plaq << std::endl;
  }

  // -----------------------------------------------------------------------
  // 3. APE smearing on SPATIAL links with snapshots at smear_iters
  // -----------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u_smear(Nd);
  for (int mu = 0; mu < Nd; ++mu) u_smear[mu] = u[mu];

  auto spatial_staple = [&](const multi1d<LatticeColorMatrix>& v, int mu) {
    LatticeColorMatrix S; S = zero;
    for (int nu = 0; nu < Nd; ++nu) {
      if (nu == mu || nu == t_dir) continue;
      S += v[nu] * shift(v[mu], FORWARD, nu) * adj(shift(v[nu], FORWARD, mu));
      S += shift(adj(v[nu]) * v[mu] * shift(v[nu], FORWARD, mu), BACKWARD, nu);
    }
    return S;
  };

  const Real one_minus_alpha = Real(1) - APE_alpha;
  const Real norm = APE_alpha / Real(2 * (Nd - 2));

  Set ts; ts.make(TimeSliceFunc(t_dir));

  // Storage: Op[level][t]
  multi1d< multi1d<Double> > Op(n_levels);
  for (int s = 0; s < n_levels; ++s) {
    Op[s].resize(Lt);
    Op[s] = zero;
  }

  int next_idx = 0;
  for (int it = 1; it <= max_iter; ++it) {
    multi1d<LatticeColorMatrix> u_new(Nd);
    for (int mu = 0; mu < Nd; ++mu) u_new[mu] = u_smear[mu];
    for (int mu = 0; mu < Nd; ++mu) {
      if (mu == t_dir) continue;
      LatticeColorMatrix S = spatial_staple(u_smear, mu);
      LatticeColorMatrix V = one_minus_alpha * u_smear[mu] + norm * S;
      reunit(V);
      u_new[mu] = V;
    }
    u_smear = u_new;

    // Snapshot
    if (next_idx < n_levels && it == APE_iter_list[next_idx]) {
      compute_O_plaq(u_smear, t_dir, ts, Lt, Op[next_idx]);
      // Sanity: smeared spatial plaquette at this level
      Double sp_pl = 0; int npl = 0;
      for (int mu = 0; mu < Nd; ++mu) {
        if (mu == t_dir) continue;
        for (int nu = mu + 1; nu < Nd; ++nu) {
          if (nu == t_dir) continue;
          LatticeColorMatrix P = u_smear[mu] * shift(u_smear[nu], FORWARD, mu)
                                * adj(shift(u_smear[mu], FORWARD, nu)) * adj(u_smear[nu]);
          sp_pl += sum(real(trace(P))); ++npl;
        }
      }
      if (npl > 0) {
        Double V = Real(Layout::vol());
        sp_pl /= (V * Real(Nc) * Real(npl));
        QDPIO::cout << "glueball_v2: smeared spatial plaq @ iter " << it
                    << " = " << sp_pl << std::endl;
      }
      ++next_idx;
    }
  }

  // -----------------------------------------------------------------------
  // 4. Output: one <O_smear_K> array per smearing level
  // -----------------------------------------------------------------------
  push(xml_out, "Op_t");
  write(xml_out, "Lt", Lt);
  write(xml_out, "n_smear", n_levels);
  for (int s = 0; s < n_levels; ++s) {
    multi1d<double> Op_out(Lt);
    for (int t = 0; t < Lt; ++t) Op_out[t] = toDouble(Op[s][t]);
    std::stringstream tag;
    tag << "O_smear_" << APE_iter_list[s];
    write(xml_out, tag.str(), Op_out);
  }
  pop(xml_out);

  pop(xml_out);  // glueball_correlator_v2
  xml_out.flush();

  QDPIO::cout << "glueball_v2: ran successfully" << std::endl;
  Chroma::finalize();
  return 0;
}
