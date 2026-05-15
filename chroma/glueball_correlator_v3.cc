// glueball_correlator_v3.cc — TRUE variational basis for SU(2) 0⁺⁺ glueball
//
// PROBLEM: v1 (single operator) → no plateau. v2 (multi-APE on same shape)
// → operators perfectly correlated → GEVP singular.
//
// SOLUTION (v3): 6 genuinely different geometric shapes × 2 APE levels = 12
// operators. This follows Morningstar-Peardon PRD 60 (1999) 034509.
//
// Operator shapes (all summed over spatial direction combos for A₁ rep):
//
//   Op 0,1  : PLAQ     — 1×1 spatial plaquette           (4-link)
//   Op 2,3  : RECT     — 2×1 rectangle (both orientations) (6-link)
//   Op 4,5  : SQUARE   — 2×2 square                        (8-link)
//   Op 6,7  : CHAIR    — 3D chair loop i,j,k,-i,-k,-j     (6-link)
//   Op 8,9  : PARA     — 2D parallelogram i,j,i,-j,-i,-j  (6-link)
//   Op 10,11: FATPLQ   — plaquette built from fat links    (4-link)
//
// Each shape at APE_ITER=10 and APE_ITER=25 (spatial-only smearing).
//
// OUTPUT FORMAT (per config):
//   <Op_t>
//     <Lt>16</Lt>
//     <n_ops>12</n_ops>
//     <O_op_0>val0 val1 ... val15</O_op_0>   <!-- PLAQ, APE10 -->
//     <O_op_1>val0 val1 ... val15</O_op_1>   <!-- PLAQ, APE25 -->
//     ...
//     <O_op_11>val0 val1 ... val15</O_op_11> <!-- FATPLQ, APE25 -->
//   </Op_t>
//
// The GEVP is solved OFFLINE in Python.
//
// BUILD: make -f Makefile.glueball_v3

#include "chroma.h"

using namespace Chroma;

// =========================================================================
//  Helper: compute spatial staple sum around link in direction mu
// =========================================================================
//   S_mu(x) = Σ_{ν≠mu, ν≠t_dir} [
//       U_ν(x) U_mu(x+ν) U_ν^†(x+mu)               (forward)
//     + U_ν^†(x-ν) U_mu(x-ν) U_ν(x-ν+mu)           (backward)
//   ]
LatticeColorMatrix spatial_staple(const multi1d<LatticeColorMatrix>& v,
                                   int mu, int t_dir)
{
  LatticeColorMatrix S;
  S = zero;
  for (int nu = 0; nu < Nd; ++nu) {
    if (nu == mu || nu == t_dir) continue;
    // Forward staple: U_nu(x) * U_mu(x+nu) * U_nu^†(x+mu)
    S += v[nu] * shift(v[mu], FORWARD, nu)
                * adj(shift(v[nu], FORWARD, mu));
    // Backward staple: U_nu^†(x-nu) * U_mu(x-nu) * U_nu(x-nu+mu)
    S += shift(adj(v[nu]) * v[mu] * shift(v[nu], FORWARD, mu),
               BACKWARD, nu);
  }
  return S;
}

// =========================================================================
//  Helper: APE smearing sweep (spatial only, preserves temporal links)
// =========================================================================
void ape_smear_spatial(multi1d<LatticeColorMatrix>& u_smear,
                       int t_dir, Real APE_alpha)
{
  const Real one_minus_alpha = Real(1) - APE_alpha;
  const Real norm = APE_alpha / Real(2 * (Nd - 2));

  auto staple = [&](const multi1d<LatticeColorMatrix>& v, int mu) {
    return spatial_staple(v, mu, t_dir);
  };

  multi1d<LatticeColorMatrix> u_new(Nd);
  for (int mu = 0; mu < Nd; ++mu) u_new[mu] = u_smear[mu];

  for (int mu = 0; mu < Nd; ++mu) {
    if (mu == t_dir) continue;  // preserve temporal gauge links
    LatticeColorMatrix S = staple(u_smear, mu);
    LatticeColorMatrix V = one_minus_alpha * u_smear[mu] + norm * S;
    reunit(V);
    u_new[mu] = V;
  }
  u_smear = u_new;
}

// =========================================================================
//  Helper: sum over timeslices → O(t) array
// =========================================================================
void timeslice_sum(const LatticeDouble& lat_val, const Set& ts,
                   int Lt, multi1d<Double>& out)
{
  multi1d<Double> ts_sum = sumMulti(lat_val, ts);
  for (int t = 0; t < Lt; ++t) out[t] += ts_sum[t];
}

// =========================================================================
//  SHAPE BUILDERS — each returns LatticeDouble = Re Tr(loop)
// =========================================================================

// Shape 0: Plaquette 1×1  in plane (mu, nu)
//   path: +mu, +nu, -mu, -nu
LatticeDouble plaquette_trace(const multi1d<LatticeColorMatrix>& v,
                               int mu, int nu)
{
  LatticeColorMatrix P = v[mu] * shift(v[nu], FORWARD, mu)
                        * adj(shift(v[mu], FORWARD, nu)) * adj(v[nu]);
  return real(trace(P));
}

// Shape 1: Rectangle 2×1, long side along mu
//   path: +mu, +mu, +nu, -mu, -mu, -nu
LatticeDouble rect_2x1_mu_trace(const multi1d<LatticeColorMatrix>& v,
                                 int mu, int nu)
{
  LatticeColorMatrix R = v[mu]
    * shift(v[mu], FORWARD, mu)
    * shift(shift(v[nu], FORWARD, mu), FORWARD, mu)
    * adj(shift(shift(v[mu], FORWARD, nu), FORWARD, mu))
    * adj(shift(v[mu], FORWARD, nu))
    * adj(v[nu]);
  return real(trace(R));
}

// Shape 1 alt: Rectangle 1×2, long side along nu
//   path: +mu, +nu, +nu, -mu, -nu, -nu
LatticeDouble rect_1x2_nu_trace(const multi1d<LatticeColorMatrix>& v,
                                 int mu, int nu)
{
  LatticeColorMatrix R = v[mu]
    * shift(v[nu], FORWARD, mu)
    * shift(shift(v[nu], FORWARD, nu), FORWARD, mu)
    * adj(shift(shift(v[mu], FORWARD, nu), FORWARD, nu))
    * adj(shift(v[nu], FORWARD, nu))
    * adj(v[nu]);
  return real(trace(R));
}

// Shape 2: Square 2×2 in plane (mu, nu)
//   path: +mu, +mu, +nu, +nu, -mu, -mu, -nu, -nu
LatticeDouble square_2x2_trace(const multi1d<LatticeColorMatrix>& v,
                                int mu, int nu)
{
  LatticeColorMatrix S = v[mu]
    * shift(v[mu], FORWARD, mu)
    * shift(shift(v[nu], FORWARD, mu), FORWARD, mu)
    * shift(shift(shift(v[nu], FORWARD, nu), FORWARD, mu), FORWARD, mu)
    * adj(shift(shift(shift(v[mu], FORWARD, nu), FORWARD, nu), FORWARD, mu))
    * adj(shift(shift(v[mu], FORWARD, nu), FORWARD, nu))
    * adj(shift(v[nu], FORWARD, nu))
    * adj(v[nu]);
  return real(trace(S));
}

// Shape 3: Chair 3D  — path +mu, +nu, +rho, -mu, -rho, -nu
//   (mu, nu, rho are three distinct spatial directions)
LatticeDouble chair_3d_trace(const multi1d<LatticeColorMatrix>& v,
                              int mu, int nu, int rho)
{
  LatticeColorMatrix C = v[mu]
    * shift(v[nu], FORWARD, mu)
    * shift(shift(v[rho], FORWARD, nu), FORWARD, mu)
    * adj(shift(shift(v[mu], FORWARD, rho), FORWARD, nu))
    * adj(shift(v[rho], FORWARD, nu))
    * adj(v[nu]);
  return real(trace(C));
}

// Shape 4: Parallelogram 2D — path +mu, +nu, +mu, -nu, -mu, -nu
//   Summed over all ordered pairs (mu,nu) of distinct spatial directions
LatticeDouble para_2d_trace(const multi1d<LatticeColorMatrix>& v,
                             int mu, int nu)
{
  LatticeColorMatrix P = v[mu]
    * shift(v[nu], FORWARD, mu)
    * shift(shift(v[mu], FORWARD, nu), FORWARD, mu)
    * adj(shift(shift(v[nu], FORWARD, mu), FORWARD, mu))
    * adj(shift(v[mu], FORWARD, mu))
    * adj(v[nu]);
  return real(trace(P));
}

// Shape 5: Fat-link plaquette
//   Build fat link F_mu = U_mu + c * spatial_staple(U_mu), project to SU(2),
//   then compute plaquette trace with F.
//   This probes different UV scales than smearing (local fattening vs iterative).
LatticeDouble fatplaq_trace(const multi1d<LatticeColorMatrix>& v,
                             int mu, int nu, int t_dir,
                             Real fat_coeff = Real(0.5))
{
  // Fatten mu-link only
  LatticeColorMatrix S_mu = spatial_staple(v, mu, t_dir);
  LatticeColorMatrix F_mu = v[mu] + fat_coeff * S_mu;
  reunit(F_mu);

  // Fatten nu-link only
  LatticeColorMatrix S_nu = spatial_staple(v, nu, t_dir);
  LatticeColorMatrix F_nu = v[nu] + fat_coeff * S_nu;
  reunit(F_nu);

  // Plaquette from fat links in this plane
  LatticeColorMatrix P = F_mu * shift(F_nu, FORWARD, mu)
                        * adj(shift(F_mu, FORWARD, nu)) * adj(F_nu);
  return real(trace(P));
}

// =========================================================================
//  OPERATOR LEVEL: compute O(t) for given shape and link-set
// =========================================================================
enum ShapeType { SHAPE_PLAQ=0, SHAPE_RECT=1, SHAPE_SQUARE=2,
                 SHAPE_CHAIR=3, SHAPE_PARA=4, SHAPE_FATPLQ=5,
                 N_SHAPES=6 };

void compute_operator(const multi1d<LatticeColorMatrix>& v,
                      int t_dir, const Set& ts, int Lt,
                      ShapeType shape, multi1d<Double>& Op)
{
  Op.resize(Lt);
  Op = zero;

  for (int mu = 0; mu < Nd; ++mu) {
    if (mu == t_dir) continue;

    switch (shape) {

    case SHAPE_PLAQ:
      // Sum over i<j spatial
      for (int nu = mu + 1; nu < Nd; ++nu) {
        if (nu == t_dir) continue;
        LatticeDouble tr = plaquette_trace(v, mu, nu);
        timeslice_sum(tr, ts, Lt, Op);
      }
      break;

    case SHAPE_RECT:
      // Sum over all ordered pairs (mu,nu) of distinct spatial dirs
      // Include BOTH orientations: 2×1 (long mu) and 1×2 (long nu)
      for (int nu = 0; nu < Nd; ++nu) {
        if (nu == mu || nu == t_dir) continue;
        LatticeDouble tr1 = rect_2x1_mu_trace(v, mu, nu);
        timeslice_sum(tr1, ts, Lt, Op);
        LatticeDouble tr2 = rect_1x2_nu_trace(v, mu, nu);
        timeslice_sum(tr2, ts, Lt, Op);
      }
      break;

    case SHAPE_SQUARE:
      // Sum over i<j spatial
      for (int nu = mu + 1; nu < Nd; ++nu) {
        if (nu == t_dir) continue;
        LatticeDouble tr = square_2x2_trace(v, mu, nu);
        timeslice_sum(tr, ts, Lt, Op);
      }
      break;

    case SHAPE_CHAIR:
      // Sum over all triples (mu,nu,rho) of distinct spatial directions
      for (int nu = 0; nu < Nd; ++nu) {
        if (nu == mu || nu == t_dir) continue;
        for (int rho = 0; rho < Nd; ++rho) {
          if (rho == mu || rho == nu || rho == t_dir) continue;
          LatticeDouble tr = chair_3d_trace(v, mu, nu, rho);
          timeslice_sum(tr, ts, Lt, Op);
        }
      }
      break;

    case SHAPE_PARA:
      // Sum over all ordered pairs (mu,nu) of distinct spatial directions
      for (int nu = 0; nu < Nd; ++nu) {
        if (nu == mu || nu == t_dir) continue;
        LatticeDouble tr = para_2d_trace(v, mu, nu);
        timeslice_sum(tr, ts, Lt, Op);
      }
      break;

    case SHAPE_FATPLQ:
      // Fat-link plaquette summed over i<j spatial
      for (int nu = mu + 1; nu < Nd; ++nu) {
        if (nu == t_dir) continue;
        LatticeDouble tr = fatplaq_trace(v, mu, nu, t_dir);
        timeslice_sum(tr, ts, Lt, Op);
      }
      break;

    default:
      break;
    }
  }
}

// =========================================================================
//  MAIN
// =========================================================================
int main(int argc, char *argv[])
{
  Chroma::initialize(&argc, &argv);

  XMLFileWriter& xml_out = Chroma::getXMLOutputInstance();
  push(xml_out, "glueball_correlator_v3");

  // -------------------------------------------------------------------
  // 1. Parse input XML
  // -------------------------------------------------------------------
  if (argc < 3) {
    QDPIO::cerr << "Usage: glueball_correlator_v3 -i input.xml -o output.xml"
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
  multi1d<int> APE_iters;      // e.g. 10 25
  read(xml_in, "/glueball/APE_iters", APE_iters);
  Cfg_t cfg;
  read(xml_in, "/glueball/Cfg", cfg);

  // Validate
  if (APE_iters.size() < 2) {
    QDPIO::cerr << "Need at least 2 APE iterations, got "
                << APE_iters.size() << std::endl;
    Chroma::finalize();
    return 1;
  }
  for (int s = 1; s < APE_iters.size(); ++s) {
    if (APE_iters[s] <= APE_iters[s-1]) {
      QDPIO::cerr << "APE_iters must be strictly ascending" << std::endl;
      Chroma::finalize();
      return 1;
    }
  }

  Layout::setLattSize(nrow);
  Layout::create();
  const int Lt = nrow[t_dir];
  const int n_ape_levels = APE_iters.size();     // 2
  const int max_ape = APE_iters[n_ape_levels - 1];

  // Total operators = N_SHAPES × n_ape_levels
  const int n_ops_total = N_SHAPES * n_ape_levels;  // 12

  write(xml_out, "nrow", nrow);
  write(xml_out, "t_dir", t_dir);
  write(xml_out, "APE_alpha", APE_alpha);
  write(xml_out, "APE_iters", APE_iters);
  write(xml_out, "n_shapes", N_SHAPES);
  write(xml_out, "n_ape_levels", n_ape_levels);
  write(xml_out, "cfg_file", cfg.cfg_file);

  // -------------------------------------------------------------------
  // 2. Read gauge config
  // -------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u(Nd);
  XMLReader gauge_file_xml, gauge_xml;
  QDPIO::cout << "glueball_v3: reading config " << cfg.cfg_file << std::endl;
  gaugeStartup(gauge_file_xml, gauge_xml, u, cfg);
  QDPIO::cout << "glueball_v3: config read OK" << std::endl;

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
    QDPIO::cout << "glueball_v3: raw plaquette = " << plaq << std::endl;
  }

  // -------------------------------------------------------------------
  // 4. Prepare timeslice set
  // -------------------------------------------------------------------
  Set ts;
  ts.make(TimeSliceFunc(t_dir));

  // -------------------------------------------------------------------
  // 5. Storage for all operators: Op[op_idx][t]
  //    Layout: Op[shape * n_ape_levels + ape_idx]
  //    shape 0..5, ape_idx 0..1 → 0..11
  // -------------------------------------------------------------------
  multi1d< multi1d<Double> > Op_all(n_ops_total);
  for (int i = 0; i < n_ops_total; ++i) {
    Op_all[i].resize(Lt);
    Op_all[i] = zero;
  }

  // -------------------------------------------------------------------
  // 6. Progressive APE smearing + operator snapshots
  // -------------------------------------------------------------------
  multi1d<LatticeColorMatrix> u_smear(Nd);
  for (int mu = 0; mu < Nd; ++mu) u_smear[mu] = u[mu];

  // Compute operators at APE=0 AND at each APE_iters level
  // Strategy: we snapshot at iter=0 (raw links) plus each target iter.
  // But the task specifies APE=10 and APE=25 only, not raw. So we only
  // snapshot at the target iters.
  //
  // However, we need operators on DIFFERENT smearing levels.
  // We do cumulative smearing and snapshot at each APE_iters[s].

  int next_ape_idx = 0;
  for (int it = 1; it <= max_ape; ++it) {
    // One APE sweep on spatial links
    ape_smear_spatial(u_smear, t_dir, APE_alpha);

    // Snapshot if this is a target iteration
    if (next_ape_idx < n_ape_levels && it == APE_iters[next_ape_idx]) {
      QDPIO::cout << "glueball_v3: snapshot at APE iter " << it << std::endl;

      // Spatial plaquette sanity at this smearing level
      {
        Double sp_pl = 0; int npl = 0;
        for (int mu = 0; mu < Nd; ++mu) {
          if (mu == t_dir) continue;
          for (int nu = mu + 1; nu < Nd; ++nu) {
            if (nu == t_dir) continue;
            LatticeColorMatrix P =
              u_smear[mu] * shift(u_smear[nu], FORWARD, mu)
              * adj(shift(u_smear[mu], FORWARD, nu)) * adj(u_smear[nu]);
            sp_pl += sum(real(trace(P))); ++npl;
          }
        }
        if (npl > 0) {
          Double V = Real(Layout::vol());
          sp_pl /= (V * Real(Nc) * Real(npl));
          QDPIO::cout << "glueball_v3: smeared spatial plaq @ iter " << it
                      << " = " << sp_pl << std::endl;
        }
      }

      // Compute all 6 shape operators on these smeared links
      for (int shape = 0; shape < N_SHAPES; ++shape) {
        int op_idx = shape * n_ape_levels + next_ape_idx;
        QDPIO::cout << "glueball_v3:   shape=" << shape
                    << " op_idx=" << op_idx << std::endl;
        compute_operator(u_smear, t_dir, ts, Lt,
                         static_cast<ShapeType>(shape), Op_all[op_idx]);
      }
      ++next_ape_idx;
    }
  }

  // -------------------------------------------------------------------
  // 7. Output: XML with O_op_0 .. O_op_{n_ops_total-1}
  // -------------------------------------------------------------------
  push(xml_out, "Op_t");
  write(xml_out, "Lt", Lt);
  write(xml_out, "n_ops", n_ops_total);

  // Shape names for metadata
  const char* shape_names[N_SHAPES] = {
    "PLAQ", "RECT", "SQUARE", "CHAIR", "PARA", "FATPLQ"
  };

  for (int shape = 0; shape < N_SHAPES; ++shape) {
    for (int a = 0; a < n_ape_levels; ++a) {
      int op_idx = shape * n_ape_levels + a;

      multi1d<double> Op_out(Lt);
      for (int t = 0; t < Lt; ++t) Op_out[t] = toDouble(Op_all[op_idx][t]);

      std::stringstream tag;
      tag << "O_op_" << op_idx;
      write(xml_out, tag.str(), Op_out);

      // Also write metadata attribute
      std::stringstream comment;
      comment << "shape=" << shape_names[shape]
              << " APE=" << APE_iters[a];
    }
  }
  pop(xml_out);  // Op_t

  // -------------------------------------------------------------------
  // 8. Write operator metadata for offline analysis
  // -------------------------------------------------------------------
  push(xml_out, "Op_metadata");
  write(xml_out, "n_ops", n_ops_total);
  write(xml_out, "n_shapes", N_SHAPES);
  write(xml_out, "n_ape_levels", n_ape_levels);
  for (int shape = 0; shape < N_SHAPES; ++shape) {
    push(xml_out, "shape");
    write(xml_out, "shape_id", shape);
    write(xml_out, "shape_name", std::string(shape_names[shape]));
    write(xml_out, "ape_iters", APE_iters);
    pop(xml_out);
  }
  pop(xml_out);  // Op_metadata

  pop(xml_out);  // glueball_correlator_v3
  xml_out.flush();

  QDPIO::cout << "glueball_v3: ran successfully" << std::endl;
  Chroma::finalize();
  return 0;
}
