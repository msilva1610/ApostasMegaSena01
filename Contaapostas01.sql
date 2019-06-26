insert into apostas6dezenasrefinadastemp
SELECT *
  FROM apostas6dezenasrefinadas
  where (qtde_q1 >= 1 and qtde_q2 >= 1 and qtde_q3 >= 1 and qtde_q4 >= 1)
  and (pares not in (5,6,0))
  and (TotalDePrimos not in (4,5,6))
  and (qtdeDezFinonacci not in (3,4,5,6))
  and (somadasdezenas >= 102 and somadasdezenas <= 268)
  and (SomaDosDigitosDaDezena >= 27 and SomaDosDigitosDaDezena <= 58)
  and (m3 in (1,2,3) or (m4 in (0,1,2,3)) or (m5 in (0,1,2)) or (m6 in (0,1,2))
  or  (m7 in (0,1,2)) or (m8 in (0,1,2)) or (m9 in (0,1)) or (m10 in (0,1,2))
  or  (m11 in (0,1)) or (m12 in (0,1,2)) or (m13 in (0,1,2)) or (m14 in (0,1,2))
  or  (m15 in (0,1)) or (m16 in (0,1)) or (m17 in (0,1)) or (m18 in (0,1))
  or  (m19 in (0,1)) or (m20 in (0,1)) or (m21 in (0,1)) or (m22 in (0,1)) 
  or  (m22 in (0,1)) or (m23 in (0,1)) or (m24 in (0,1)) or (m25 in (0,1)) 
  or  (m26 in (0,1)) or (m27 in (0,1)) or (m28 in (0,1)) or (m29 in (0,1)) 
  or  (m30 in (0,1)))
  and totallinhas in (3,4,5)
  and totalcolunas in (4,5,6)
  and totconsecutivos in (0,1,2)
  and intervalordezenaok = 1
  and totaldigitos in (5,6,7,8)
  and totalparesdezenasespelho = 0
  and (r3 in (2,3) or r4 in (1,2) or r5 in (1,2) or r6 in (1,2) 
  or r7 in (1,2) or r8 in (1,2) or r9 in (1,2) or r10 in (0,1,2) or r11 in (0,1,2) 
  or r12 in (0,1,2) or r13 in (0,1) or r14 in (0,1) or r15 in (0,1) 
  or r16 in (0,1) or r17 in (0,1) or r18 in (0,1) or r19 in (0,1) or r20 in (0,1))
LIMIT 1000;


select count(*)
from apostas6dezenasrefinadas
where r3 > 3