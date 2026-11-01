/* verif_cert.c — VÉRIFICATEUR INDÉPENDANT d'un certificat produit par tm_cert.
 * Méthode volontairement différente : l'orbite d'une suite de pas est identifiée par son code MINIMAL sur les
 * 48 éléments explicites du groupe hyperoctaédral (permutations signées des axes), et non par la forme canonique
 * constructive de tm_cert ; le nombre de visites N est recalculé par un parcours explicite des positions.
 * Vérifie : (i) les états du fichier sont deux à deux dans des orbites distinctes ; (ii) toute transition aboutit
 * dans une orbite représentée ; (iii) pour tout état s :  B * sum_d p[N(s,d)] * H[orb(s,d)]  <=  A * Q * H[s]
 * (arithmétique entière __int128 exacte), avec H >= 1.
 * Usage : verif_cert m fichier_poids fichier_h     Compilation : gcc -O3 -fopenmp -o verif_cert verif_cert.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int M; static uint64_t P6[24];
static int G[48][6];   /* G[g][d] = image de la direction d */
static const int V[6][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
static void groupe(void){
  int perms[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}}, g=0;
  for(int p=0;p<6;p++) for(int sg=0;sg<8;sg++){
    for(int d=0;d<6;d++){ int a=d/2, e=d&1; int b=perms[p][a]; int f=e^((sg>>a)&1); G[g][d]=2*b+f; }
    g++; }
  /* contrôle : chaque G[g] est une bijection qui envoie -d sur -image(d) */
  for(int g2=0;g2<48;g2++){ int vu[6]={0}; for(int d=0;d<6;d++){ vu[G[g2][d]]++; if((G[g2][d]^1)!=G[g2][d^1]){fprintf(stderr,"groupe faux\n");exit(9);} }
    for(int d=0;d<6;d++) if(vu[d]!=1){fprintf(stderr,"groupe faux\n");exit(9);} }
}
static uint64_t mincode(const int *s){  /* s[0] = pas le plus récent = chiffre de poids fort */
  uint64_t best=UINT64_MAX;
  for(int g=0;g<48;g++){ uint64_t c=0; for(int i=0;i<M;i++) c=6*c+G[g][s[i]]; if(c<best) best=c; }
  return best;
}
typedef struct { uint64_t k; uint64_t h; } KH;
static int cmpkh(const void*a,const void*b){ uint64_t x=((const KH*)a)->k,y=((const KH*)b)->k; return x<y?-1:x>y; }
static KH *tab; static size_t nst;
static int cherche(uint64_t k, uint64_t *h){ size_t lo=0,hi=nst; while(lo<hi){size_t mid=(lo+hi)/2; if(tab[mid].k<k) lo=mid+1; else hi=mid;}
  if(lo<nst && tab[lo].k==k){*h=tab[lo].h; return 1;} return 0; }
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 1;}
  M=atoi(argv[1]); P6[0]=1; for(int i=1;i<24;i++) P6[i]=6*P6[i-1]; groupe();
  FILE*fw=fopen(argv[2],"r"); unsigned long long Q; int K; if(fscanf(fw,"%llu %d",&Q,&K)!=2) return 1;
  uint64_t p[70]; for(int n=1;n<=K;n++){ unsigned long long t; if(fscanf(fw,"%llu",&t)!=1) return 1; p[n]=t; } fclose(fw);
  FILE*fh=fopen(argv[3],"rb"); if(!fh){perror("h");return 1;}
  if(fread(&nst,sizeof nst,1,fh)!=1) return 1;
  uint64_t *codes=malloc(nst*8), *H=malloc(nst*8); uint64_t A,B;
  if(fread(codes,8,nst,fh)!=nst||fread(H,8,nst,fh)!=nst||fread(&A,8,1,fh)!=1||fread(&B,8,1,fh)!=1){fprintf(stderr,"lecture\n");return 1;}
  fclose(fh);
  tab=malloc(nst*sizeof(KH));
  #pragma omp parallel for schedule(static)
  for(size_t i=0;i<nst;i++){ int s[24]; uint64_t c=codes[i]; for(int k=M-1;k>=0;k--){ s[k]=c%6; c/=6; } tab[i].k=mincode(s); tab[i].h=H[i]; }
  qsort(tab,nst,sizeof(KH),cmpkh);
  for(size_t i=1;i<nst;i++) if(tab[i].k==tab[i-1].k){ fprintf(stderr,"ECHEC : deux etats dans la meme orbite\n"); return 6; }
  size_t mauvais=0, manquants=0, hnul=0;
  #pragma omp parallel for schedule(static) reduction(+:mauvais,manquants,hnul)
  for(size_t i=0;i<nst;i++){
    int s[24], t[24]; uint64_t c=codes[i]; for(int k=M-1;k>=0;k--){ s[k]=c%6; c/=6; }
    if(H[i]==0) hnul++;
    u128 S=0;
    for(int d=0;d<6;d++){
      /* positions des M sites précédents, relatives au site courant */
      int x=0,y=0,z=0,N=1;
      for(int k=0;k<M;k++){ x-=V[s[k]][0]; y-=V[s[k]][1]; z-=V[s[k]][2]; if(x==V[d][0]&&y==V[d][1]&&z==V[d][2]) N++; }
      int n = N>K?K:N;
      t[0]=d; for(int k=1;k<M;k++) t[k]=s[k-1];
      uint64_t hv; if(!cherche(mincode(t),&hv)){ manquants++; continue; }
      S += (u128)p[n]*(u128)hv;
    }
    if(S*(u128)B > (u128)A*(u128)Q*(u128)H[i]) mauvais++;
  }
  printf("verif_cert m=%d etats=%zu rho'=%llu/%llu=%.15f : inegalites violees=%zu, transitions hors table=%zu, H nuls=%zu => %s\n",
    M,nst,(unsigned long long)A,(unsigned long long)B,(double)A/(double)B,mauvais,manquants,hnul,(mauvais||manquants||hnul)?"ECHEC":"CERTIFICAT VALIDE");
  return (mauvais||manquants||hnul)?7:0;
}
