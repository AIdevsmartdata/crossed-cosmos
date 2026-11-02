/* cert_incline11.c — (version m <= 12, a,b <= 4096, inégalité sans décalage 2^30) — certificat de Perron ENTIER pour l'opérateur de transfert à mémoire m, INCLINÉ dans la direction e1.
 * Etat s = (d_1,...,d_m), d_1 = pas le plus récent ; code c = sum_i d_i 6^(m-i) ; espace COMPLET 6^m (aucune symétrie).
 * Nouveau pas d : N(s,d) = 1 + #{i in 1..m : P_i = e_d}, P_i = -(d_1+...+d_i) ; état suivant (d,d_1,...,d_{m-1}),
 * code d*6^(m-1) + c/6.  Poids : r(N) = p[min(N,K)]/Q ; inclinaison e^{+lambda} (d=0 : +e1), e^{-lambda} (d=1 : -e1),
 * e^lambda = a/b rationnel.  Certificat : H entier > 0 et P tels que, pour tout état s,
 *     2^30 * sum_d p[N(s,d)] * c_d * H[next(s,d)]  <=  P * Q * a*b * H[s],   c_0 = a^2, c_1 = b^2, c_d = a*b sinon,
 * ce qui prouve rho(T_lambda) <= P / 2^30 (arithmétique unsigned __int128, débordement contrôlé).
 * Version 11 : on vérifie la forme ÉQUIVALENTE  sum_d p[N] c_d H[next] <= P * 2^10 * a*b * H[s]  (Q = 2^40 = 2^30 * 2^10),
 * bornes : gauche <= 6 * 2^40 * 4096^2 * 2^40 < 2^107, droite <= 2^32 * 2^10 * 2^24 * 2^40 = 2^106 : pas de débordement.
 * Usage : cert_incline11 m fichier_poids a b sortie_H.bin   (affiche une ligne JSON)
 * Compilation : gcc -O3 -fopenmp -o cert_incline11 cert_incline11.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
static const int DX[6][3]={{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: cert_incline m poids a b sortie_H\n");return 1;}
  int M=atoi(argv[1]); long a=atol(argv[3]), b=atol(argv[4]);
  if(M<1||M>12||a<1||b<1||a>4096||b>4096){fprintf(stderr,"parametres hors limites\n");return 1;}
  FILE*fw=fopen(argv[2],"r"); if(!fw){perror("poids");return 1;}
  unsigned long long Qll; int K; if(fscanf(fw,"%llu %d",&Qll,&K)!=2||K<1||K>64){fprintf(stderr,"poids\n");return 1;}
  uint64_t Q=Qll,p[65]; for(int n=1;n<=K;n++){unsigned long long t; if(fscanf(fw,"%llu",&t)!=1)return 1; p[n]=t;}
  fclose(fw);
  if(Q!=((uint64_t)1<<40)){fprintf(stderr,"Q attendu 2^40\n");return 1;}
  for(int n=1;n<=K;n++) if(p[n]>Q){fprintf(stderr,"p>Q\n");return 1;}
  uint64_t P6[24]; P6[0]=1; for(int i=1;i<24;i++)P6[i]=6*P6[i-1];
  size_t S=P6[M]; uint8_t*nn=malloc(6*S); if(!nn){perror("malloc");return 2;}
  #pragma omp parallel for schedule(static)
  for(size_t c=0;c<S;c++){
    int s[16]; for(int k=0;k<M;k++) s[k]=(int)((c/P6[M-1-k])%6);
    int x=0,y=0,z=0,px[16],py[16],pz[16];
    for(int k=0;k<M;k++){x-=DX[s[k]][0];y-=DX[s[k]][1];z-=DX[s[k]][2];px[k]=x;py[k]=y;pz[k]=z;}
    for(int d=0;d<6;d++){int N=1; for(int k=0;k<M;k++) if(px[k]==DX[d][0]&&py[k]==DX[d][1]&&pz[k]==DX[d][2]) N++; nn[6*c+d]=(uint8_t)N;}
  }
  double el=(double)a/(double)b, w[6][17];
  for(int d=0;d<6;d++) for(int N=1;N<=16;N++){int n=N>K?K:N; double t=(double)p[n]/(double)Q; w[d][N]= d==0? t*el : (d==1? t/el : t);}
  double*h=malloc(S*sizeof(double)),*g=malloc(S*sizeof(double)); if(!h||!g){perror("malloc");return 2;}
  for(size_t c=0;c<S;c++)h[c]=1.0;
  double lo=0,hi=0; int it;
  for(it=0;it<20000;it++){
    double mx=0;
    #pragma omp parallel for reduction(max:mx) schedule(static)
    for(size_t c=0;c<S;c++){double v=0; size_t base=c/6; for(int d=0;d<6;d++) v+=w[d][nn[6*c+d]]*h[(size_t)d*P6[M-1]+base]; g[c]=v; if(v>mx)mx=v;}
    lo=1e300;hi=0;
    #pragma omp parallel for reduction(min:lo) reduction(max:hi) schedule(static)
    for(size_t c=0;c<S;c++){double r=g[c]/h[c]; if(r<lo)lo=r; if(r>hi)hi=r;}
    #pragma omp parallel for schedule(static)
    for(size_t c=0;c<S;c++) h[c]=g[c]/mx;
    if(it>30 && (hi-lo)<1e-13*hi) break;
  }
  /* entiers : H = ceil(h * 2^40) >= 1 */
  free(g);
  uint64_t*H=malloc(S*sizeof(uint64_t)); if(!H){perror("malloc H");return 2;} double hm=0; for(size_t c=0;c<S;c++) if(h[c]>hm)hm=h[c];
  uint64_t Hmin=UINT64_MAX,Hmax=0;
  for(size_t c=0;c<S;c++){double v=ceil(h[c]/hm*1099511627776.0); if(v<1)v=1; H[c]=(uint64_t)v; if(H[c]<Hmin)Hmin=H[c]; if(H[c]>Hmax)Hmax=H[c];}
  free(h);
  u128 ab=(u128)a*b, cd[6]; cd[0]=(u128)a*a; cd[1]=(u128)b*b; for(int d=2;d<6;d++)cd[d]=ab;
  uint64_t P=(uint64_t)ceil(hi*1073741824.0*(1.0+1e-9))+1; long viol=0; int essais=0;
  for(;;){
    viol=0;
    #pragma omp parallel for reduction(+:viol) schedule(static)
    for(size_t c=0;c<S;c++){
      u128 L=0; size_t base=c/6;
      for(int d=0;d<6;d++){int N=nn[6*c+d]; int n=N>K?K:N; L+=(u128)p[n]*cd[d]*(u128)H[(size_t)d*P6[M-1]+base];}
      u128 R=(u128)P*((u128)1<<10)*ab*(u128)H[c];
      if(L>R) viol++;
    }
    if(viol==0||essais>40)break;
    P+= (P>>20)+1; essais++;
  }
  FILE*fo=fopen(argv[5],"wb"); if(!fo){perror("sortie");return 1;} fwrite(H,sizeof(uint64_t),S,fo); fclose(fo);
  printf("{\"m\": %d, \"a\": %ld, \"b\": %ld, \"etats\": %zu, \"iterations\": %d, \"rho_flottant\": [%.15f, %.15f], "
         "\"P\": %llu, \"rho_cert\": %.15f, \"Hmin\": %llu, \"Hmax\": %llu, \"violations\": %ld, \"essais_P\": %d}\n",
         M,a,b,S,it,lo,hi,(unsigned long long)P,(double)P/1073741824.0,(unsigned long long)Hmin,(unsigned long long)Hmax,viol,essais);
  return viol?4:0;
}
