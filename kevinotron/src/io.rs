// kevinotron/src/io.rs
// NPY config dump and loading.
//
// Writes gauge field configurations in NumPy .npy format (v1.0).
// Layout: (4, Ls, Ls, Ls, Lt, d, d) for real groups
//         (4, Ls, Ls, Ls, Lt, d, d) complex128 for SU(N)
//
// This allows direct loading in JAX/numpy:
//   links = jnp.load("config_g2_L8.npy")
//   assert links.shape == (4, 8, 8, 8, 16, 7, 7)

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;
use byteorder::{LittleEndian, WriteBytesExt};
use std::io::Write;

/// Write a lattice configuration as .npy file.
///
/// For real groups (G2): dtype '<f8', shape (4, L, L, L, T, d, d)
/// For complex groups (SU(N)): dtype '<c16', shape (4, L, L, L, T, d, d)
///   where the flat f64 pairs (re,im) map to complex128.
pub fn dump_config_npy(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    path: &str,
) -> std::io::Result<()> {
    let ls = lat.ls;
    let lt = lat.lt;
    let d = group.dim_fund();
    let is_complex = group.is_complex();

    // Build the .npy header
    let dtype = if is_complex { "<c16" } else { "<f8" };
    let shape_str = format!("({}, {}, {}, {}, {}, {}, {})", 4, ls, ls, ls, lt, d, d);
    let descr = format!(
        "{{'descr': '{}', 'fortran_order': False, 'shape': {}, }}",
        dtype, shape_str
    );

    // Header: magic (6) + version (2) + header_len (2) + header + padding to 64-byte boundary
    let magic = b"\x93NUMPY";
    let version: [u8; 2] = [1, 0];
    // Total header length (after magic+version+header_len) must be multiple of 64
    let base_len = magic.len() + version.len() + 2; // 10
    let header_bytes = descr.as_bytes();
    let total_needed = base_len + header_bytes.len() + 1; // +1 for newline
    let padding = (64 - (total_needed % 64)) % 64;
    let header_len = (header_bytes.len() + padding + 1) as u16;

    let mut file = std::fs::File::create(path)?;
    file.write_all(magic)?;
    file.write_all(&version)?;
    file.write_u16::<LittleEndian>(header_len)?;
    file.write_all(header_bytes)?;
    for _ in 0..padding {
        file.write_all(b" ")?;
    }
    file.write_all(b"\n")?;

    // Write data in C order: mu, x0, x1, x2, x3, i, j
    // This matches the flat layout if we iterate in this order.
    //
    // The lattice stores links as:
    //   flat_idx = ((x0*ls + x1)*ls + x2)*lt + x3 then *4 + mu then *link_size
    // We need to output in (mu, x0, x1, x2, x3, i, j) order.
    let link_size = group.link_size();

    for mu in 0..4 {
        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        let site = [x0, x1, x2, x3];
                        let data = lat.get(site, mu);

                        if is_complex {
                            // data is 2*d*d f64: (re00,im00,re01,im01,...)
                            // numpy complex128 is (f64_re, f64_im) per entry, row-major
                            // Our storage is already (re,im) interleaved row-major
                            for val in data.iter() {
                                file.write_f64::<LittleEndian>(*val)?;
                            }
                        } else {
                            // data is d*d f64, row-major
                            for val in data.iter() {
                                file.write_f64::<LittleEndian>(*val)?;
                            }
                        }
                    }
                }
            }
        }
    }

    Ok(())
}

/// Write raw dS/dalpha measurements to a .dat file.
pub fn write_measurements_dat(
    path: &str,
    group_name: &str,
    ls: usize,
    lt: usize,
    beta: f64,
    alpha_idx: usize,
    alpha: f64,
    measurements: &[f64],
) -> std::io::Result<()> {
    use std::io::BufWriter;
    let file = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(path)?;
    let mut writer = BufWriter::new(file);
    if alpha_idx == 0 {
        writeln!(writer, "# {} EE raw measurements", group_name)?;
        writeln!(writer, "# Ls={} Lt={} beta={}", ls, lt, beta)?;
        writeln!(writer, "# Columns: alpha_idx config_idx dS_dalpha")?;
    }
    for (m, val) in measurements.iter().enumerate() {
        writeln!(writer, "{} {} {:.10}", alpha_idx, m, val)?;
    }
    Ok(())
}
