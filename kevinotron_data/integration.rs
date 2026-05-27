use std::process::Command;

fn kev(args: &[&str]) -> (String, String, bool) {
    let o = Command::new("./target/release/kevinotron").args(args).output().expect("run failed");
    (String::from_utf8_lossy(&o.stdout).to_string(), String::from_utf8_lossy(&o.stderr).to_string(), o.status.success())
}

#[test]
fn cold_start_all_groups() {
    for g in &["su2","su3","su4","g2","sp4","so7","f4","e6"] {
        let (_,se,ok) = kev(&["--group",g,"--ls","4","--beta","10.0","--n-therm","1","--n-meas","1","--n-skip","1","--epsilon","0.1","--alpha","0.0"]);
        assert!(ok, "{} failed", g);
        assert!(se.contains("P=1.000000 OK"), "{} cold start fail", g);
    }
}

#[test]
fn ee_output_format() {
    let (so,_,ok) = kev(&["--group","su2","--ls","4","--beta","2.5","--n-therm","50","--n-meas","5","--n-skip","1","--full-ee","--n-alpha","3","--no-parallel","--no-validate"]);
    assert!(ok);
    assert!(so.contains("ALPHA 0.000:"));
    assert!(so.contains("RESULT: S2/area="));
}

#[test]
fn hmc_su2_runs() {
    let (_,se,ok) = kev(&["--group","su2","--ls","4","--beta","2.3","--hmc-run","--hmc-traj","10","--hmc-steps","20","--hmc-dt","0.02","--no-validate"]);
    assert!(ok);
    assert!(se.contains("HMC done"));
}

#[test]
fn thermal_scan_runs() {
    let (so,se,ok) = kev(&["--group","su2","--ls","4","--beta","2.3","--thermal","--n-therm","20","--n-meas","5","--n-skip","1","--epsilon","0.2","--no-validate"]);
    assert!(ok);
    assert!(so.contains("Lt"));
}
