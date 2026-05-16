{
count = 0;
rk2_dist = vector(6);
for(D=-300, -200,
  if(isfundamental(D),
    bnf = bnfinit(x^2 - D, 1);
    cyc = bnf.clgp[2];
    is_2gp = 1;
    if(#cyc > 0,
      for(i=1, #cyc, if(cyc[i] % 2, is_2gp = 0; break));
      if(is_2gp,
        rk2 = #cyc;
        if(rk2 <= 5, rk2_dist[rk2]++);
      );
    );
    count = count + 1;
    print("D=", D, " cyc=", cyc, " 2gp=", is_2gp);
  );
);
print("DONE: count=", count, " dist=", rk2_dist);
}
