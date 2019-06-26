SELECT count(*)
  FROM apostas6dezenasrefinadas
  where not (qtde_q1 > 3 or qtde_q2 > 3 or qtde_q3 or qtde_q4 > 3)
  and (pares not in (5,6,0))
  and (TotalDePrimos not in (4,5,6))
  and (qtdeDezFinonacci not in (3,4,5,6))
  and (somadasdezenas >= 102 and somadasdezenas <= 268)
  and (SomaDosDigitosDaDezena >= 27 and SomaDosDigitosDaDezena <= 58)
 -- sobram: 4.453.561
