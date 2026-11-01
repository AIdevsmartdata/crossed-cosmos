/* tm_cert.c — matrice de transfert à mémoire m pour les marches pondérées sur Z^3, réduite par les 48 symétries,
 * itération de puissance (flottants) puis CERTIFICAT ENTIER EXACT : vecteur h > 0 et rho' = a/b tels que
 *     sum_d p[N(s,d)] * h[next(s,d)] * b  <=  a * Q * h[s]      pour tout état s      (arithmétique __int128)
 * ce qui prouve que le rayon spectral de la matrice des poids p/Q est <= a/b.
 *
 * Etat = suite des m derniers pas (d_1 = plus récent). Nouveau pas d : N = 1 + #{i in 1..m : P_i = d},
 * P_i = -(d_1 + ... + d_i) (positions des m sites précédents, relatives au site courant).
 * Poids du pas : p[N]/Q (p[N] = p[Kmax] pour N > Kmax).
 * Forme canonique (représentant unique d'orbite) : d_1 = +x ; le premier pas hors de l'axe x vaut +y ;
 * le premier pas selon l'axe z vaut +z.  Code = sum_i d_i 6^(m-i) (d_1 = chiffre de poids fort).
 * Directions : 0:+x 1:-x 2:+y 3:-y 4:+z 5:-z.
 *
 * Usage : tm_cert m fichier_poids [fichier_sortie_h]
 *   fichier_poids : Q  Kmax  p_1 ... p_Kmax   (entiers décimaux, séparés par des blancs)
 * Compilation : gcc -O3 -fopenmp -o tm_cert tm_cert.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

typedef unsigned __int128 u128;
static int M;                       /* mémoire */
static uint64_t P6[24];
static const int DX[6][3] = {{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
static uint64_t *codes; static size_t nst, cap;

static void push(uint64_t c){ if(nst==cap){cap=cap?2*cap:1024; codes=realloc(codes,cap*sizeof *codes); if(!codes){perror("realloc");exit(2);} } codes[nst++]=c; }

/* DFS d'énumération des suites canoniques ; ynon : un pas hors-x déjà vu ; zvu : un pas z déjà vu */
static void dfs(int i, uint64_t code, int ynon, int zvu){
  if(i==M){ push(code); return; }
  for(int d=0; d<6; d++){
    if(i==0 && d!=0) continue;
    int axe=d/2;
    if(!ynon && axe!=0 && d!=2) continue;     /* premier pas hors-x doit être +y */
    if(ynon && !zvu && axe==2 && d!=4) continue; /* premier pas z doit être +z (après un hors-x) */
    /* remarque : si le premier hors-x est +y, un pas z ultérieur est le premier pas z */
    int ny = ynon || (axe!=0), nz = zvu || (axe==2);
    dfs(i+1, code + (uint64_t)d*P6[M-1-i], ny, nz);
  }
}
static int cmpu64(const void*a,const void*b){ uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b; return x<y?-1:x>y; }

/* canonicalise une suite s[0..M-1] (s[0] = plus récent) : renvoie le code canonique */
static uint64_t canon(const int *s){
  int perm[3], sgn[3];               /* image de l'axe a : axe perm[a], signe sgn[a] (0:+,1:-) */
  for(int a=0;a<3;a++){perm[a]=-1;sgn[a]=0;}
  /* 1) l'axe de s[0] -> x, avec signe + */
  int a0=s[0]/2; perm[a0]=0; sgn[a0]=s[0]&1;
  /* 2) premier pas d'axe != a0 -> +y */
  int a1=-1;
  for(int i=0;i<M;i++){ int a=s[i]/2; if(a!=a0){ a1=a; perm[a1]=1; sgn[a1]=s[i]&1; break; } }
  /* 3) troisième axe -> z ; signe : premier pas selon cet axe -> +z */
  int a2=-1; for(int a=0;a<3;a++) if(a!=a0 && a!=a1){ if(a1<0){ /* pas de pas hors a0 : choisir arbitrairement */ } }
  if(a1<0){ /* seuls des pas selon a0 : les autres axes n'apparaissent pas */
    int k=1; for(int a=0;a<3;a++) if(a!=a0){ perm[a]=k++; sgn[a]=0; }
  } else {
    for(int a=0;a<3;a++) if(a!=a0 && a!=a1) a2=a;
    perm[a2]=2; sgn[a2]=0;
    for(int i=0;i<M;i++){ if(s[i]/2==a2){ sgn[a2]=s[i]&1; break; } }
  }
  uint64_t c=0;
  for(int i=0;i<M;i++){ int a=s[i]/2, e=s[i]&1; int d=2*perm[a] + (e^sgn[a]); c += (uint64_t)d*P6[M-1-i]; }
  return c;
}
static size_t find(uint64_t c){
  size_t lo=0, hi=nst;
  while(lo<hi){ size_t mid=(lo+hi)/2; if(codes[mid]<c) lo=mid+1; else hi=mid; }
  if(lo>=nst || codes[lo]!=c){ fprintf(stderr,"etat introuvable %llu\n",(unsigned long long)c); exit(3); }
  return lo;
}

int main(int argc, char **argv){
  if(argc<3){ fprintf(stderr,"usage: tm_cert m fichier_poids [sortie_h]\n"); return 1; }
  M=atoi(argv[1]); if(M<1||M>13){ fprintf(stderr,"m hors limites\n"); return 1; }
  P6[0]=1; for(int i=1;i<24;i++) P6[i]=6*P6[i-1];
  FILE *fw=fopen(argv[2],"r"); if(!fw){perror("poids");return 1;}
  unsigned long long Qll; int K; if(fscanf(fw,"%llu %d",&Qll,&K)!=2||K<1||K>64){fprintf(stderr,"poids mal formés\n");return 1;}
  uint64_t Q=Qll, p[65]; for(int n=1;n<=K;n++){ unsigned long long t; if(fscanf(fw,"%llu",&t)!=1){fprintf(stderr,"poids manquants\n");return 1;} p[n]=t; }
  fclose(fw);
  for(int n=1;n<=K;n++) if(p[n] > ((uint64_t)1<<50)){ fprintf(stderr,"numérateur trop grand\n"); return 1; }
  dfs(0,0,0,0);
  qsort(codes,nst,sizeof *codes,cmpu64);
  for(size_t i=1;i<nst;i++) if(codes[i]==codes[i-1]){ fprintf(stderr,"doublon\n"); return 3; }
  fprintf(stderr,"m=%d : %zu etats canoniques\n",M,nst);
  uint32_t *to=malloc(6*nst*sizeof *to); uint8_t *nn=malloc(6*nst);
  if(!to||!nn){perror("malloc");return 2;}
  #pragma omp parallel for schedule(dynamic,4096)
  for(size_t i=0;i<nst;i++){
    int s[24], t[24]; uint64_t c=codes[i];
    for(int k=0;k<M;k++){ s[k]=(int)((c/P6[M-1-k])%6); }
    if(canon(s)!=c){ fprintf(stderr,"etat non canonique !\n"); exit(3); }
    int pos[24][3]; int x=0,y=0,z=0;
    for(int k=0;k<M;k++){ x-=DX[s[k]][0]; y-=DX[s[k]][1]; z-=DX[s[k]][2]; pos[k][0]=x; pos[k][1]=y; pos[k][2]=z; }
    for(int d=0; d<6; d++){
      int N=1; for(int k=0;k<M;k++) if(pos[k][0]==DX[d][0]&&pos[k][1]==DX[d][1]&&pos[k][2]==DX[d][2]) N++;
      if(N>255) N=255;
      t[0]=d; for(int k=1;k<M;k++) t[k]=s[k-1];
      to[6*i+d]=(uint32_t)find(canon(t)); nn[6*i+d]=(uint8_t)N;
    }
  }
  /* itération de puissance */
  double *w=malloc(256*sizeof(double)); for(int N=0;N<256;N++){ int n=N<1?1:(N>K?K:N); w[N]=(double)p[n]/(double)Q; }
  double *h=malloc(nst*sizeof(double)), *g=malloc(nst*sizeof(double));
  for(size_t i=0;i<nst;i++) h[i]=1.0;
  double lo=0,hi=0; int it;
  for(it=0; it<5000; it++){
    double mx=0;
    #pragma omp parallel for reduction(max:mx)
    for(size_t i=0;i<nst;i++){ double v=0; for(int d=0;d<6;d++) v+=w[nn[6*i+d]]*h[to[6*i+d]]; g[i]=v; if(v>mx) mx=v; }
    lo=1e300; hi=0;
    #pragma omp parallel for reduction(min:lo) reduction(max:hi)
    for(size_t i=0;i<nst;i++){ double r=g[i]/h[i]; if(r<lo) lo=r; if(r>hi) hi=r; }
    for(size_t i=0;i<nst;i++) h[i]=g[i]/mx;
    if(it>20 && (hi-lo)<1e-14*hi) break;
  }
  fprintf(stderr,"iterations=%d  rho flottant dans [%.15f, %.15f]\n",it,lo,hi);
  /* certificat entier */
  double hmax=0; for(size_t i=0;i<nst;i++) if(h[i]>hmax) hmax=h[i];
  uint64_t *H=malloc(nst*sizeof(uint64_t)); uint64_t Hmin=UINT64_MAX,Hmax=0;
  const double SC=1099511627776.0; /* 2^40 */
  for(size_t i=0;i<nst;i++){ double v=floor(h[i]/hmax*SC); if(v<1) v=1; H[i]=(uint64_t)v; if(H[i]<Hmin)Hmin=H[i]; if(H[i]>Hmax)Hmax=H[i]; }
  const uint64_t B=(uint64_t)1<<30;  /* rho' = A/B */
  uint64_t A=0;
  for(size_t i=0;i<nst;i++){
    u128 S=0; for(int d=0;d<6;d++){ int N=nn[6*i+d]; int n=N>K?K:N; S += (u128)p[n]*(u128)H[to[6*i+d]]; }
    u128 num=S*(u128)B, den=(u128)Q*(u128)H[i];
    u128 a=(num+den-1)/den; if(a>(u128)UINT64_MAX){fprintf(stderr,"debordement\n");return 4;}
    if((uint64_t)a>A) A=(uint64_t)a;
  }
  /* vérification exacte avec A final */
  size_t bad=0;
  for(size_t i=0;i<nst;i++){
    u128 S=0; for(int d=0;d<6;d++){ int N=nn[6*i+d]; int n=N>K?K:N; S += (u128)p[n]*(u128)H[to[6*i+d]]; }
    if(S*(u128)B > (u128)A*(u128)Q*(u128)H[i]) bad++;
  }
  printf("m=%d etats=%zu rho_cert=%llu/%llu = %.15f  (flottant [%.15f,%.15f])  verif_echecs=%zu  Hmin=%llu Hmax=%llu\n",
         M,nst,(unsigned long long)A,(unsigned long long)B,(double)A/(double)B,lo,hi,bad,(unsigned long long)Hmin,(unsigned long long)Hmax);
  if(argc>=4){ FILE *fo=fopen(argv[3],"wb"); if(!fo){perror("sortie");return 1;}
    fwrite(&nst,sizeof nst,1,fo); fwrite(codes,sizeof *codes,nst,fo); fwrite(H,sizeof *H,nst,fo);
    fwrite(&A,sizeof A,1,fo); fwrite(&B,sizeof B,1,fo); fclose(fo); }
  return bad?5:0;
}
