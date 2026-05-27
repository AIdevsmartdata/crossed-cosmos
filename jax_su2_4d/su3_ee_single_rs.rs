use nalgebra::SMatrix;
use rand::Rng;
use rand_distr::StandardNormal;
use clap::Parser;
use std::time::Instant;

type Mat3 = SMatrix<f64, 3, 3>;
// SU(3) in real 3×3 — NO. SU(3) needs COMPLEX 3×3.
// Use real embedding: SU(3) ⊂ SO(6) via 6-dim real rep... too complex.
// Simpler: work with complex matrices using nalgebra Complex.
// SIMPLEST: use f64 pairs (re,im) manually for 3×3 complex.

// Actually the cleanest approach for comparison with G_2:
// Use the ADJOINT representation (8-dim real matrices, 8×8).
// Then S₂/Area is directly comparable between G_2 (14-dim adj = 14×14... no)

// WAIT — the G_2 code uses the FUNDAMENTAL 7-dim real rep.
// For SU(3), the fundamental is 3-dim COMPLEX.
// To compare fairly, we need to use the same observable definition.

// The standard lattice approach: SU(3) links are 3×3 UNITARY matrices.
// Plaquette = (1/3) Re Tr(U_plaq) where U is complex 3×3.

// For a fair comparison with G_2 (7×7 real), we should use the SAME
// normalization: (1/d_rep) Re Tr(U_plaq) where d_rep = dim of fundamental.

// Implementation: complex 3×3 matrices using [f64; 18] = 3×3×2 (re,im)

const N: usize = 3;
const N2: usize = N * N; // 9 complex = 18 real

#[derive(Clone, Copy)]
struct CMat {
    re: SMatrix<f64, 3, 3>,
    im: SMatrix<f64, 3, 3>,
}

impl CMat {
    fn identity() -> Self {
        CMat { re: SMatrix::identity(), im: SMatrix::zeros() }
    }
    fn mul(&self, other: &CMat) -> CMat {
        CMat {
            re: &self.re * &other.re - &self.im * &other.im,
            im: &self.re * &other.im + &self.im * &other.re,
        }
    }
    fn dagger(&self) -> CMat {
        CMat { re: self.re.transpose(), im: -self.im.transpose() }
    }
    fn trace_re(&self) -> f64 {
        self.re.trace()
    }
}

fn su3_generators() -> Vec<(SMatrix<f64,3,3>, SMatrix<f64,3,3>)> {
    // Gell-Mann matrices λ_1..λ_8 (hermitian, traceless)
    // T_a = i λ_a / 2 (anti-hermitian generators)
    let mut gens = Vec::new();
    let z = SMatrix::<f64,3,3>::zeros();

    // λ_1
    let mut r = z; let mut i = z;
    r[(0,1)] = 0.5; r[(1,0)] = 0.5;
    gens.push((i, r)); // T_1 = i*λ_1/2 → re=0, im=λ_1/2

    // λ_2
    let mut r = z; let mut i = z;
    i[(0,1)] = 0.5; i[(1,0)] = -0.5; // actually λ_2 has -i,+i
    r[(0,1)] = 0.5; r[(1,0)] = -0.5; // T_2 = i*λ_2/2
    // λ_2 = [[0,-i,0],[i,0,0],[0,0,0]]
    // i*λ_2/2 = [[0,1/2,0],[-1/2,0,0],[0,0,0]] (real part)
    let mut r = z;
    r[(0,1)] = 0.5; r[(1,0)] = -0.5;
    gens.push((r, z));

    // λ_3
    let mut r = z;
    r[(0,0)] = 0.5; r[(1,1)] = -0.5; // i*λ_3/2 is imaginary: [[i/2,0],[0,-i/2],[0,0,0]]
    let mut i = z;
    i[(0,0)] = 0.5; i[(1,1)] = -0.5;
    gens.push((z, i));

    // λ_4
    let mut r = z;
    r[(0,2)] = 0.5; r[(2,0)] = 0.5;
    gens.push((z, r));

    // λ_5
    let mut r = z;
    r[(0,2)] = 0.5; r[(2,0)] = -0.5;
    gens.push((r, z));

    // λ_6
    let mut r = z;
    r[(1,2)] = 0.5; r[(2,1)] = 0.5;
    gens.push((z, r));

    // λ_7
    let mut r = z;
    r[(1,2)] = 0.5; r[(2,1)] = -0.5;
    gens.push((r, z));

    // λ_8
    let s = 0.5 / (3.0f64).sqrt();
    let mut i = z;
    i[(0,0)] = s; i[(1,1)] = s; i[(2,2)] = -2.0*s;
    gens.push((z, i));

    gens // each is (re, im) of T_a = i*λ_a/2
}

fn expm_su3(re: &SMatrix<f64,3,3>, im: &SMatrix<f64,3,3>) -> CMat {
    // exp(A) for anti-hermitian 3×3 via Taylor order 12
    // A = re + i*im where re is anti-symmetric, im is symmetric traceless
    let mut r_sum = SMatrix::<f64,3,3>::identity();
    let mut i_sum = SMatrix::<f64,3,3>::zeros();
    let mut r_pow = SMatrix::<f64,3,3>::identity();
    let mut i_pow = SMatrix::<f64,3,3>::zeros();
    for n in 1..=12 {
        let f = 1.0 / (n as f64);
        let nr = (&r_pow * re - &i_pow * im) * f;
        let ni = (&r_pow * im + &i_pow * re) * f;
        r_pow = nr; i_pow = ni;
        r_sum += &r_pow;
        i_sum += &i_pow;
    }
    CMat { re: r_sum, im: i_sum }
}

fn random_su3(gens: &[(SMatrix<f64,3,3>,SMatrix<f64,3,3>)], eps: f64, rng: &mut impl Rng) -> CMat {
    let mut re = SMatrix::<f64,3,3>::zeros();
    let mut im = SMatrix::<f64,3,3>::zeros();
    for (gr, gi) in gens {
        let c: f64 = rng.sample::<f64,_>(StandardNormal) * eps;
        re += gr * c;
        im += gi * c;
    }
    expm_su3(&re, &im)
}

struct Lat {
    ls: usize, lt: usize, beta: f64,
    gens: Vec<(SMatrix<f64,3,3>,SMatrix<f64,3,3>)>,
    links: Vec<CMat>,
}

impl Lat {
    fn new(ls: usize, lt: usize, beta: f64) -> Self {
        let g = su3_generators();
        let n = ls*ls*ls*lt*4;
        Lat { ls, lt, beta, gens: g, links: vec![CMat::identity(); n] }
    }
    fn sz(&self,d:usize)->usize{if d<3{self.ls}else{self.lt}}
    fn idx(&self,s:[usize;4],mu:usize)->usize{
        ((s[0]*self.ls+s[1])*self.ls+s[2])*self.lt*4+s[3]*4+mu
    }
    fn shift(&self,s:[usize;4],mu:usize,d:i32)->[usize;4]{
        let mut r=s;r[mu]=((r[mu]as i32+d).rem_euclid(self.sz(mu)as i32))as usize;r
    }
    fn get(&self,s:[usize;4],mu:usize)->&CMat{&self.links[self.idx(s,mu)]}
    fn set(&mut self,s:[usize;4],mu:usize,u:CMat){let i=self.idx(s,mu);self.links[i]=u;}

    fn staple(&self,s:[usize;4],mu:usize)->CMat{
        let mut st = CMat{re:SMatrix::zeros(),im:SMatrix::zeros()};
        for nu in 0..4{if nu==mu{continue;}
            let xm=self.shift(s,mu,1);let xn=self.shift(s,nu,1);
            let fwd = self.get(xm,nu).mul(&self.get(xn,mu).dagger()).mul(&self.get(s,nu).dagger());
            st.re += &fwd.re; st.im += &fwd.im;
            let xmn=self.shift(xm,nu,-1);let xn2=self.shift(s,nu,-1);
            let bwd = self.get(xmn,nu).dagger().mul(&self.get(xn2,mu).dagger()).mul(self.get(xn2,nu));
            st.re += &bwd.re; st.im += &bwd.im;
        }
        st
    }
    fn is_bdy(&self,s:[usize;4],mu:usize)->bool{mu==0&&s[0]==self.ls/2-1}

    fn sweep_a(&mut self,alpha:f64,eps:f64,rng:&mut impl Rng)->f64{
        let(ls,lt)=(self.ls,self.lt);
        let(mut a,mut t)=(0u64,0u64);
        for x0 in 0..ls{for x1 in 0..ls{for x2 in 0..ls{for x3 in 0..lt{
            let s=[x0,x1,x2,x3];
            for mu in 0..4{
                let uo=*self.get(s,mu);
                let k=self.staple(s,mu);
                let uk=uo.mul(&k);
                let base=-(self.beta/3.0)*uk.trace_re();
                let so=if self.is_bdy(s,mu){(1.-alpha)*base}else{base};
                let r=random_su3(&self.gens,eps,rng);
                let un=r.mul(&uo);
                let unk=un.mul(&k);
                let base2=-(self.beta/3.0)*unk.trace_re();
                let sn=if self.is_bdy(s,mu){(1.-alpha)*base2}else{base2};
                if sn-so<0.||rng.gen::<f64>()<(-(sn-so)).exp(){self.set(s,mu,un);a+=1;}
                t+=1;
            }
        }}}}
        a as f64/t as f64
    }
    fn measure_ds(&self)->f64{
        let(ls,lt)=(self.ls,self.lt);
        let mut ds=0.0;
        for x1 in 0..ls{for x2 in 0..ls{for x3 in 0..lt{
            let s=[ls/2-1,x1,x2,x3];
            let u=self.get(s,0);
            let k=self.staple(s,0);
            let uk=u.mul(&k);
            ds+=-(self.beta/3.0)*uk.trace_re();
        }}}
        -ds
    }
    fn plaq(&self)->f64{
        let(ls,lt)=(self.ls,self.lt);
        let(mut p,mut c)=(0.0,0u64);
        for x0 in 0..ls{for x1 in 0..ls{for x2 in 0..ls{for x3 in 0..lt{
            let s=[x0,x1,x2,x3];
            for mu in 0..4{for nu in(mu+1)..4{
                let xm=self.shift(s,mu,1);let xn=self.shift(s,nu,1);
                let pl=self.get(s,mu).mul(self.get(xm,nu)).mul(&self.get(xn,mu).dagger()).mul(&self.get(s,nu).dagger());
                p+=pl.trace_re()/3.;c+=1;
            }}
        }}}}
        p/c as f64
    }
}

#[derive(Parser)]
struct Args{
    #[arg(long)] ls:usize,
    #[arg(long,default_value="6.06")] beta:f64,
    #[arg(long)] alpha:f64,
    #[arg(long,default_value="500")] n_therm:usize,
    #[arg(long,default_value="200")] n_meas:usize,
    #[arg(long,default_value="5")] n_skip:usize,
    #[arg(long,default_value="0.15")] epsilon:f64,
}

fn main(){
    let a=Args::parse();
    let lt=2*a.ls;
    let mut rng=rand::thread_rng();
    let t0=Instant::now();
    let mut lat=Lat::new(a.ls,lt,a.beta);
    for s in 0..a.n_therm{
        lat.sweep_a(a.alpha,a.epsilon,&mut rng);
        if(s+1)%100==0{eprintln!("therm {}: P={:.6}",s+1,lat.plaq());}
    }
    let mut meas=Vec::with_capacity(a.n_meas);
    for _ in 0..a.n_meas{
        for _ in 0..a.n_skip{lat.sweep_a(a.alpha,a.epsilon,&mut rng);}
        meas.push(lat.measure_ds());
    }
    let mean:f64=meas.iter().sum::<f64>()/meas.len()as f64;
    let var:f64=meas.iter().map(|x|(x-mean).powi(2)).sum::<f64>()/meas.len()as f64;
    let err=(var/meas.len()as f64).sqrt();
    println!("ALPHA {:.3}: dS/dalpha = {:.6} +/- {:.6}",a.alpha,mean,err);
    eprintln!("# Time: {:.1}s",t0.elapsed().as_secs_f64());
}
