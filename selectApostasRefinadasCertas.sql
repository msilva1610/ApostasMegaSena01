SELECT count(*)
  FROM apostas6dezenasrefinadascerta a, apostas6dezenasrefinadas b
  where a.id = b.id
  and a.impares = 1
  and a.pares = 1
  and a.quadrante = 1
  and a.totaldeprimos = 1
  and a.qtdeDezFinonacci = 1
  and a.somadasdezenas = 1
  and a.SomaDosDigitosDaDezena = 1
  and a.TotNumquadraticos = 1
  and a.TotalColunas = 1
  and a.totConsecutivos = 1
  and a.IntervalorDezenaOk = 1
  and a.TotalDigitos = 1
  and a.TotalParesDezenasEspelho = 1
  and a.razao = 1
  and a.m = 1
  and (b.qtde_q1 <= 3 or b.qtde_q2 <= 3 or b.qtde_q3 <= 3 or b.qtde_q4 <= 3)
-- 29162395
-- 810.664 ms
