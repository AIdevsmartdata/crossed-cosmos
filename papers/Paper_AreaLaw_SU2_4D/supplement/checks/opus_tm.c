/* opus_tm.c — vérification adverse (Opus), écrit SANS reprendre tm_cert.c ni verif_cert.c.
 *
 * Marches sur Z^3, directions 0:+x 1:-x 2:+y 3:-y 4:+z 5:-z (même codage de fichier que le certificat, imposé par
 * le format ; tout le reste est réécrit). Etat = (d_1..d_m), d_1 = pas le plus récent ; code = sum d_i 6^(m-i).
 * Suivant(s,d) = (d,d_1..d_{m-1}) : code' = d*6^(m-1) + code/6.  N(s,d) = 1 + #{i : -(d_1+..+d_i) = vec(d)}.
 *
 * Modes :
 *  perron m fichier_poids [maxit]     : itération de puissance sur les 6^m états BRUTS (aucune symétrie),
 *                                       bornes de Collatz-Wielandt min/max (Tv)/v.  fichier_poids = "Q K p1..pK"
 *                                       (poids p[min(N,K)]/Q) ; "BS" = poids de Borgs-Seiler 1/(N+1).
 *  plein m fichier_poids certificat   : vérification du certificat sur TOUS les 6^m états bruts : H~(s) := H[orbite(s)]
 *                                       (orbite = code minimal sur 48 matrices de permutation signée appliquées aux
 *                                       VECTEURS), puis  B*sum_d p*H~(suivant) <= A*Q*H~(s)  pour CHAQUE état brut.
 *                                       Aucun argument de symétrie n'intervient dans la validité (H~ > 0 suffit).
 *  orbites m fichier_poids certificat nech : vérification sur les représentants du fichier (argument d'équivariance)
 *                                       + nech états BRUTS tirés au hasard (vérifiés directement).
 * Compilation : gcc -O3 -march=native -fopenmp -o opus_tm opus_tm.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128;

static int M; static uint64_t P6[30];
static int VEC[6][3] = {{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
static int GD[48][6];            /* image de la direction d par l'élément g du groupe */
static uint64_t Qw; static int Kw; static uint64_t pw[80]; static double wd[80]; static int BS = 0;

static int dir_of(int x, int y, int z){ for(int d=0; d<6; d++) if(VEC[d][0]==x && VEC[d][1]==y && VEC[d][2]==z) return d; return -1; }
static void build_group(void){
  int perm[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}}; int g = 0;
  for(int p=0; p<6; p++) for(int sg=0; sg<8; sg++){
    int Mx[3][3] = {{0}};                     /* matrice : colonne a = image de e_a = signe * e_{perm[a]} */
    for(int a=0; a<3; a++) Mx[perm[p][a]][a] = ((sg>>a)&1) ? -1 : 1;
    for(int d=0; d<6; d++){ int v[3]; for(int r=0; r<3; r++){ v[r]=0; for(int c=0;c<3;c++) v[r]+=Mx[r][c]*VEC[d][c]; }
      GD[g][d] = dir_of(v[0],v[1],v[2]); if(GD[g][d]<0){ fprintf(stderr,"groupe\n"); exit(9);} }
    g++; }
  /* contrôle : 48 éléments distincts, chacun bijectif */
  for(int a=0;a<48;a++){ int seen[6]={0}; for(int d=0;d<6;d++) seen[GD[a][d]]++; for(int d=0;d<6;d++) if(seen[d]!=1){fprintf(stderr,"non bijectif\n");exit(9);}
    for(int b=0;b<a;b++){ int same=1; for(int d=0;d<6;d++) if(GD[a][d]!=GD[b][d]) same=0; if(same){fprintf(stderr,"doublon groupe\n");exit(9);} } }
}
static inline void decode(uint64_t c, int *s){ for(int i=M-1;i>=0;i--){ s[i]=(int)(c%6); c/=6; } }   /* s[0]=d_1 */
static inline uint64_t orbit_key(const int *s){
  uint64_t best = UINT64_MAX;
  for(int g=0; g<48; g++){ uint64_t c=0; for(int i=0;i<M;i++){ c = c*6 + (uint64_t)GD[g][s[i]]; if(best != UINT64_MAX && c > best/P6[M-1-i]) { c = UINT64_MAX; break; } }
    if(c < best) best = c; }
  return best;
}
/* nombre de coïncidences de la fenêtre avec chacun des 6 voisins */
static inline void counts(const int *s, int *cnt){
  int x=0,y=0,z=0; for(int d=0;d<6;d++) cnt[d]=1;
  for(int i=0;i<M;i++){ x-=VEC[s[i]][0]; y-=VEC[s[i]][1]; z-=VEC[s[i]][2];
    if(abs(x)+abs(y)+abs(z)==1){ int d=dir_of(x,y,z); cnt[d]++; } }
}
static void read_weights(const char *f){
  if(!strcmp(f,"BS")){ BS=1; Kw=60; Qw=0; for(int n=1;n<=Kw;n++) wd[n]=1.0/(n+1); return; }
  FILE *fp=fopen(f,"r"); if(!fp){perror(f);exit(1);} unsigned long long q; if(fscanf(fp,"%llu %d",&q,&Kw)!=2){exit(1);} Qw=q;
  for(int n=1;n<=Kw;n++){ unsigned long long t; if(fscanf(fp,"%llu",&t)!=1) exit(1); pw[n]=t; wd[n]=(double)t/(double)Qw; } fclose(fp);
}
static inline int widx(int N){ return N>Kw?Kw:N; }

static int mode_perron(int maxit){
  uint64_t S = P6[M];
  uint8_t *cn = malloc(6*S); double *v = malloc(8*S), *u = malloc(8*S);
  if(!cn||!v||!u){perror("malloc");return 2;}
  #pragma omp parallel for schedule(static)
  for(uint64_t c=0;c<S;c++){ int s[32], cnt[6]; decode(c,s); counts(s,cnt); for(int d=0;d<6;d++) cn[6*c+d]=(uint8_t)cnt[d]; v[c]=1.0; }
  double lo=0, hi=0; int it;
  for(it=0; it<maxit; it++){
    double mx=0; lo=1e300; hi=0;
    #pragma omp parallel for schedule(static) reduction(max:mx,hi) reduction(min:lo)
    for(uint64_t c=0;c<S;c++){ uint64_t b=c/6; double t=0; for(int d=0;d<6;d++) t += wd[widx(cn[6*c+d])]*v[d*P6[M-1]+b];
      u[c]=t; if(t>mx) mx=t; double r=t/v[c]; if(r<lo) lo=r; if(r>hi) hi=r; }
    #pragma omp parallel for schedule(static)
    for(uint64_t c=0;c<S;c++) v[c]=u[c]/mx;
    if(it>10 && hi-lo < 1e-13*hi) break;
  }
  printf("perron m=%d etats=%llu poids=%s it=%d  rho dans [%.13f, %.13f]\n", M,(unsigned long long)S, BS?"BS":"fichier", it, lo, hi);
  return 0;
}

typedef struct { uint64_t k; uint64_t h; } KH;
static int cmpkh(const void *a, const void *b){ uint64_t x=((const KH*)a)->k, y=((const KH*)b)->k; return x<y?-1:(x>y); }
static KH *tab; static uint64_t ntab;
static inline int lookup(uint64_t k, uint64_t *h){ uint64_t lo=0,hi=ntab; while(lo<hi){ uint64_t mid=(lo+hi)/2; if(tab[mid].k<k) lo=mid+1; else hi=mid; }
  if(lo<ntab && tab[lo].k==k){ *h=tab[lo].h; return 1; } return 0; }
static uint64_t Acert, Bcert, *codes, *Hc;
static void read_cert(const char *f){
  FILE *fp=fopen(f,"rb"); if(!fp){perror(f);exit(1);}
  if(fread(&ntab,8,1,fp)!=1) exit(1);
  codes=malloc(8*ntab); Hc=malloc(8*ntab); if(!codes||!Hc){perror("malloc");exit(2);}
  if(fread(codes,8,ntab,fp)!=ntab || fread(Hc,8,ntab,fp)!=ntab || fread(&Acert,8,1,fp)!=1 || fread(&Bcert,8,1,fp)!=1){ fprintf(stderr,"lecture cert\n"); exit(1);}
  fclose(fp);
  tab = malloc(sizeof(KH)*ntab); if(!tab){perror("malloc");exit(2);}
  uint64_t nonvalide=0;
  #pragma omp parallel for schedule(static) reduction(+:nonvalide)
  for(uint64_t i=0;i<ntab;i++){ int s[32]; if(codes[i]>=P6[M]) nonvalide++; decode(codes[i],s); tab[i].k=orbit_key(s); tab[i].h=Hc[i]; }
  qsort(tab, ntab, sizeof(KH), cmpkh);
  uint64_t dup=0, hzero=0, hmin=UINT64_MAX, hmax=0;
  for(uint64_t i=0;i<ntab;i++){ if(i && tab[i].k==tab[i-1].k) dup++; if(tab[i].h==0) hzero++; if(tab[i].h<hmin) hmin=tab[i].h; if(tab[i].h>hmax) hmax=tab[i].h; }
  /* Burnside : (6^m + 3*4^m + 15*2^m)/48 */
  u128 burn = ((u128)P6[M] + 3*((u128)1<<(2*M)) + 15*((u128)1<<M)); uint64_t nburn = (uint64_t)(burn/48); uint64_t rburn=(uint64_t)(burn%48);
  printf("certificat : n=%llu  Burnside=%llu (reste %llu)  codes_invalides=%llu  doublons_d_orbite=%llu  H_nuls=%llu  Hmin=%llu Hmax=%llu  A/B=%llu/%llu=%.15f\n",
    (unsigned long long)ntab,(unsigned long long)nburn,(unsigned long long)rburn,(unsigned long long)nonvalide,(unsigned long long)dup,(unsigned long long)hzero,
    (unsigned long long)hmin,(unsigned long long)hmax,(unsigned long long)Acert,(unsigned long long)Bcert,(double)Acert/(double)Bcert);
  if(dup||hzero||nonvalide||ntab!=nburn){ printf("ECHEC structure du certificat\n"); exit(7); }
}
/* teste un état brut ; renvoie 0 si OK, 1 si violation, 2 si transition absente ; ratio = B*S/(A*Q*H) */
static inline int test_state(uint64_t c, uint64_t Hs, long double *ratio){
  int s[32], t[32], cnt[6]; decode(c,s); counts(s,cnt);
  u128 Ssum=0;
  for(int d=0; d<6; d++){ t[0]=d; for(int i=1;i<M;i++) t[i]=s[i-1]; uint64_t h; if(!lookup(orbit_key(t),&h)) return 2; Ssum += (u128)pw[widx(cnt[d])]*(u128)h; }
  u128 L = Ssum*(u128)Bcert, R = (u128)Acert*(u128)Qw*(u128)Hs;
  *ratio = (long double)L/(long double)R;
  return L>R ? 1 : 0;
}
static int mode_plein(void){
  uint64_t S=P6[M]; uint64_t *Hf = malloc(8*S); if(!Hf){perror("malloc");return 2;}
  uint64_t absent=0;
  #pragma omp parallel for schedule(static) reduction(+:absent)
  for(uint64_t c=0;c<S;c++){ int s[32]; decode(c,s); uint64_t h; if(!lookup(orbit_key(s),&h)){ absent++; h=0; } Hf[c]=h; }
  printf("H~ construit sur %llu etats bruts, orbites absentes=%llu\n",(unsigned long long)S,(unsigned long long)absent);
  if(absent){ printf("ECHEC\n"); return 7; }
  uint64_t viol=0, hz=0; long double rmax=0;
  #pragma omp parallel
  { long double rloc=0;
    #pragma omp for schedule(static) reduction(+:viol,hz)
    for(uint64_t c=0;c<S;c++){
      int s[32], cnt[6]; decode(c,s); counts(s,cnt); if(Hf[c]==0){ hz++; continue; }
      u128 Ssum=0; uint64_t b=c/6; for(int d=0;d<6;d++) Ssum += (u128)pw[widx(cnt[d])]*(u128)Hf[d*P6[M-1]+b];
      u128 L=Ssum*(u128)Bcert, R=(u128)Acert*(u128)Qw*(u128)Hf[c];
      if(L>R) viol++;
      long double r=(long double)L/(long double)R; if(r>rloc) rloc=r; }
    #pragma omp critical
    { if(rloc>rmax) rmax=rloc; } }
  printf("PLEIN m=%d : etats bruts=%llu  violations=%llu  H~ nuls=%llu  rapport max B*S/(A*Q*H)=%.15Lf  => %s\n",
    M,(unsigned long long)S,(unsigned long long)viol,(unsigned long long)hz, rmax, (viol||hz)?"ECHEC":"CERTIFICAT VALIDE SUR L'ESPACE COMPLET");
  return (viol||hz)?7:0;
}
static uint64_t splitmix(uint64_t *x){ uint64_t z=(*x+=0x9E3779B97F4A7C15ULL); z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
static int mode_orbites(uint64_t nech){
  uint64_t viol=0, absent=0; long double rmax=0;
  #pragma omp parallel
  { long double rloc=0;
    #pragma omp for schedule(dynamic,65536) reduction(+:viol,absent)
    for(uint64_t i=0;i<ntab;i++){ long double r=0; int s[32]; decode(codes[i],s); uint64_t hs; if(!lookup(orbit_key(s),&hs)){absent++;continue;}
      int st=test_state(codes[i],hs,&r); if(st==1) viol++; else if(st==2) absent++; if(r>rloc) rloc=r; }
    #pragma omp critical
    { if(rloc>rmax) rmax=rloc; } }
  printf("ORBITES m=%d : representants=%llu violations=%llu transitions_absentes=%llu rapport_max=%.15Lf\n",
    M,(unsigned long long)ntab,(unsigned long long)viol,(unsigned long long)absent,rmax);
  uint64_t v2=0,a2=0; long double rmax2=0;
  #pragma omp parallel
  { uint64_t seed=0x1234567ULL + 7919ULL*(uint64_t)omp_get_thread_num(); long double rloc=0;
    #pragma omp for schedule(static) reduction(+:v2,a2)
    for(uint64_t i=0;i<nech;i++){ uint64_t c=splitmix(&seed)%P6[M]; int s[32]; decode(c,s); uint64_t hs; long double r=0;
      if(!lookup(orbit_key(s),&hs)){a2++;continue;} int st=test_state(c,hs,&r); if(st==1) v2++; else if(st==2) a2++; if(r>rloc) rloc=r; }
    #pragma omp critical
    { if(rloc>rmax2) rmax2=rloc; } }
  printf("ECHANTILLON BRUT m=%d : etats tires=%llu violations=%llu absents=%llu rapport_max=%.15Lf\n",
    M,(unsigned long long)nech,(unsigned long long)v2,(unsigned long long)a2,rmax2);
  int bad = viol||absent||v2||a2;
  printf("=> %s\n", bad?"ECHEC":"CERTIFICAT VALIDE (representants + echantillon brut)");
  return bad?7:0;
}
int main(int argc, char **argv){
  if(argc<4){ fprintf(stderr,"usage: opus_tm perron|plein|orbites m poids [cert|maxit] [nech]\n"); return 1; }
  M=atoi(argv[2]); P6[0]=1; for(int i=1;i<30;i++) P6[i]=6*P6[i-1];
  build_group(); read_weights(argv[3]);
  if(!strcmp(argv[1],"perron")) return mode_perron(argc>4?atoi(argv[4]):20000);
  if(BS){ fprintf(stderr,"poids entiers requis\n"); return 1; }
  read_cert(argv[4]);
  if(!strcmp(argv[1],"plein")) return mode_plein();
  if(!strcmp(argv[1],"orbites")) return mode_orbites(argc>5?strtoull(argv[5],0,10):10000000ULL);
  return 1;
}
