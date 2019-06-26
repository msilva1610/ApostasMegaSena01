import sqlite3
import sys
import glob
import os
import os.path
import json
import logging
import datetime

from GeraTodasApostas import Apostas

logging.basicConfig(filename='RefinaapostasDB02.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio')

def CalculaPA(dezenas):
    r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 
    dezenas.sort()
    ParDePAs = 0
    delta1 = dezenas[1] - dezenas[0]
    for index in range(len(dezenas) - 1):
        if (dezenas[index + 1] - dezenas[index]) == delta1:
            ParDePAs += 1
        elif delta1 == 3:
            r3 = ParDePAs
            delta1 = 0
        elif delta1 == 4:
            r4 = ParDePAs
            delta1 = 0
        elif delta1 == 5:
            r5 = ParDePAs
            delta1 = 0
        elif delta1 == 6:
            r6 = ParDePAs
            delta1 = 0                        
        elif delta1 == 7:
            r7 = ParDePAs
            delta1 = 0                        
        elif delta1 == 8:
            r8 = ParDePAs
            delta1 = 0
        elif delta1 == 9:
            r9 = ParDePAs
            delta1 = 0
        elif delta1 == 10:
            r10 = ParDePAs
            delta1 = 0
        elif delta1 == 11:
            r11 = ParDePAs
            delta1 = 0
        elif delta1 == 12:
            r12 = ParDePAs
            delta1 = 0
        elif delta1 == 13:
            r13 = ParDePAs
            delta1 = 0
        elif delta1 == 14:
            r14 = ParDePAs
            delta1 = 0
        elif delta1 == 15:
            r15 = ParDePAs
            delta1 = 0
        elif delta1 == 16:
            r16 = ParDePAs
            delta1 = 0
        elif delta1 == 17:
            r17 = ParDePAs
            delta1 = 0
        elif delta1 == 18:
            r18 = ParDePAs
            delta1 = 0
        elif delta1 == 19:
            r19 = ParDePAs
            delta1 = 0
        elif delta1 == 20:
            r20 = ParDePAs
            delta1 = 0            
    return r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20


def DezenasQueMaisSaem(dezenas):
    DezenasMais = [5,10,53,23,4,54]
    TotalDezenas = list(set(dezenas) & set(DezenasMais))  # Encontra os iguais
    return len(TotalDezenas)


def CalculaDezenasEspelho(dezenas):
    dez2d = []
    dezespelho = []
    dezenas.sort()
    TotalParesDezenasEspelho = 0
    for d in (dezenas):
        temp = "{:02d}".format(d)
        dez2d.append(temp)
    for dig in dez2d:
        digespelho = dig[1]+dig[0]
        if digespelho in dez2d:
            TotalParesDezenasEspelho += 1
    return (TotalParesDezenasEspelho/2)


def CalculaPresencaDigitos(dezenas):
    digitos = []
    TotalDigitos = 0
    dezenas.sort()
    for d in dezenas:
        for digito in str(d):
            digitos.append(digito)
    TotalDigitos = list(dict.fromkeys(digitos))
    return len(TotalDigitos)


def CalculaIntervaloDezena(dezenas):
    IntervalorDezenaOk = True
    dz = 0
    dezenas.sort()
    for d in dezenas:
        dz += 1
        if (d not in range(1,26) and d == 1):
            IntervalorDezenaOk = False
        elif (d not in range(2,37) and d == 2):
            IntervalorDezenaOk = False
        elif (d not in range(5,47) and d == 3):
            IntervalorDezenaOk = False
        elif (d not in range(13,54) and d == 4):
            IntervalorDezenaOk = False
        elif (d not in range(23,59) and d == 5):
            IntervalorDezenaOk = False
        elif (d not in range(35,60) and d == 6):
            IntervalorDezenaOk = False
    return IntervalorDezenaOk


def CalculaConsecutivos(dezenas):
    numAnterior = 1
    totConsecutivos = 0
    dezenas.sort()
    for d in dezenas:
        if (d - numAnterior) == 1:
            totConsecutivos += 1
        numAnterior = d
    return totConsecutivos


def calculaColunas(dezenas):
    TotalColunas = 0
    for d in dezenas:
        if d in [1,11,21,31,41,51]:
            TotalColunas += 1
        elif d in [2,12,22,32,42,52]:
            TotalColunas += 1
        elif d in [3,13,23,33,43,53]:
            TotalColunas += 1
        elif d in [4,14,24,34,44,54]:
            TotalColunas += 1
        elif d in [5,15,25,35,45,55]:
            TotalColunas += 1
        elif d in [6,16,26,36,46,56]:
            TotalColunas += 1
        elif d in [7,17,27,37,47,57]:
            TotalColunas += 1
        elif d in [8,18,28,38,48,58]:
            TotalColunas += 1
        elif d in [9,19,29,39,49,59]:
            TotalColunas += 1
        elif d in [10,20,30,40,50,60]:
            TotalColunas += 1
    return TotalColunas
        
    
def CalculaLinhas(dezenas):
    TotalLinhas = 0
    for d in dezenas:
        if d in range(1,10):
            TotalLinhas += 1
        elif d in (range(11,20)):
            TotalLinhas += 1
        elif d in (range(21,30)):
            TotalLinhas += 1
        elif d in (range(31,40)):
            TotalLinhas += 1
        elif d in (range(41,50)):
            TotalLinhas += 1
        elif d in (range(51, 60)):
            TotalLinhas += 1
    return TotalLinhas


def CalculaQuadraticos(dezenas):
    Numquadraticos = [1,4,9,16,25,36,49]
    TotNumquadraticos = 0
    for d in dezenas:
        if d in Numquadraticos:
            TotNumquadraticos += 1
    return TotNumquadraticos


def CalculaMultiplos(dezenas):
    m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    for m in (range(2,31)):
        if m == 3:
            m3 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 4:
            m4 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 5:
            m5 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 6:
            m6 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 7:
            m7 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 8:
            m8 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 9:
            m9 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 10:
            m10 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 11:
            m11 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 12:
            m12 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 13:
            m13 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 14:
            m14 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 15:
            m15 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 16:
            m16 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 17:
            m17 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 18:
            m18 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 19:
            m19 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 20:
            m20 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 21:
            m21 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 22:
            m22 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 23:
            m23 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 24:
            m24 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 25:
            m25 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 26:
            m26 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 27:
            m27 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 28:
            m28 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 29:
            m29 = CalcMultiplosParaDezenas(m,dezenas)
        elif m == 30:
            m30 = CalcMultiplosParaDezenas(m,dezenas)
    return m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30


def CalcMultiplosParaDezenas(m, dezenas):
    TotalMultiplos = 0
    for d in dezenas:
        if d >= m:
            if d % m == 0:
                TotalMultiplos += 1

    return TotalMultiplos


def CalculaMultiplosJson(dezenas):
    try:
        tot_m = 0
        multiplos = {}
        multiplos['de'] = []    
        for m in range(2,31):    
            tot_m = 0
            for d in dezenas:
                if d >= m:
                    if d % m == 0:
                        #Essa dezena (d) é multiplo de m
                        tot_m += 1
            if tot_m > 1:
                multiplos['de'].append({str(m):tot_m})
        return multiplos    
    except:
        logging.error('error ocorreu em validaquadrante...')
    finally:
        del multiplos


def droptabelarefinada():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS apostas6dezenasrefinadas;")
    conn.close()


def criaTabelaApostasRefinadas():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Criando a tabela caso não exista.')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apostas6dezenasrefinadas
        (id INTEGER NOT NULL PRIMARY KEY,
         impares interger,
         pares interger,
         somadasdezenas interger,
         SomaDosDigitosDaDezena interger,
         TotalDePrimos interger,
         qtdeDezFinonacci interger,
		 qtde_q1 integer,
		 qtde_q2 integer,
		 qtde_q3 integer,
		 qtde_q4 integer,
         TotNumquadraticos integer,
         TotalLinhas integer,
         TotalColunas integer,
         totConsecutivos integer,
         IntervalorDezenaOk Boolean,
         TotalDigitos integer,
         TotalParesDezenasEspelho integer,
         TotalDezenasQueMaisSaem integer,
         r3 integer,
         r4 integer,
         r5 integer,
         r6 integer,
         r7 integer,
         r8 integer,
         r9 integer,
         r10 integer,
         r11 integer,
         r12 integer,
         r13 integer,
         r14 integer,
         r15 integer,
         r16 integer,
         r17 integer,
         r18 integer,
         r19 integer,
         r20 integer,
		 m3 integer,
		 m4 integer,
		 m5 integer,
		 m6 integer,
		 m7 integer,
		 m8 integer,
		 m9 integer,
		 m10 integer,
		 m11 integer,
		 m12 integer,
		 m13 integer,
		 m14 integer,
		 m15 integer,
		 m16 integer,
		 m17 integer,
		 m18 integer,
		 m19 integer,
		 m20 integer,
		 m21 integer,
		 m22 integer,
		 m23 integer,
		 m24 integer,
		 m25 integer,
		 m26 integer,
		 m27 integer,
		 m28 integer,
		 m29 integer,
		 m30 integer);
    """)
    # conn.commit()
    conn.close()


def CalculaParImparSomaDez(dezenas):
    try:
        impares = 0
        pares = 0
        SomaDezenas = 0
        for d in dezenas:
            if d % 2 != 0:
                impares += 1
            else:
                pares += 1
            SomaDezenas += d
        return impares, pares, SomaDezenas    
    except:
        logging.error('error ocorreu em CalculaParImparSomaDez...') 
    finally:
        del impares
        del pares
        del SomaDezenas    


def SomaDigitosDezenas(dezenas):
    try:
        soma_dos_digitos_das_dezenas = 0
        for d in dezenas:
            strdezena = str(d)
            for s in strdezena:
                soma_dos_digitos_das_dezenas += int(s)
        return  soma_dos_digitos_das_dezenas
    except:
        logging.error('error ocorreu em soma digitos dezenas...') 
    finally:
        del soma_dos_digitos_das_dezenas


def ContaPrimos(dezenas):
    try:
        NumerosPrimos = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
        totPrimos = 0
        for d in dezenas:
            if d in NumerosPrimos:
                totPrimos += 1
        return totPrimos
    except:
        logging.error('error ocorreu em conta primos...')
    finally:
        del NumerosPrimos
        del totPrimos


def ValidaDezenaNoQuadrante(dezenas):
    try:
        qtde_q1, qtde_q2,qtde_q3, qtde_q4 = 0, 0, 0, 0
        quadrante = {}
        quadrante['quadrantes'] = []
        q1 = {1,2,3,4,5,11,12,13,14,15,21,22,23,24,25}
        q2 = {6,7,8,9,10,16,17,18,19,20,26,27,28,29,30}
        q3 = {31,32,33,34,35,41,42,43,44,45,51,52,53,54,55}
        q4 = {36,37,38,39,40,46,47,48,49,50,56,57,58,59,60}
        for d in dezenas:
            if d in q1:
                qtde_q1 += 1
            elif d in q2:
                qtde_q2 += 1
            elif d in q3:
                qtde_q3 += 1
            else:
                qtde_q4 += 1
        return qtde_q1, qtde_q2, qtde_q3, qtde_q4
    except:
        logging.error('error ocorreu em validaquadrante...')
    finally:
        del quadrante
        del q1
        del q2
        del q3
        del q4


def ValidaFibonacci(dezenas):
    try:
        totFibo = 0
        Fibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        for d in dezenas:
            if d in Fibonacci:
                totFibo += 1
        return totFibo
    except:
        logging.error('error ocorreu em fibonacci...')
    finally:
        del totFibo
        del Fibonacci


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSenaRefinada.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    cursor.execute("""
    INSERT INTO apostas6dezenasrefinadas (id, impares, pares, somadasdezenas, SomaDosDigitosDaDezena, TotalDePrimos, qtdeDezFinonacci, qtde_q1, qtde_q2, qtde_q3, qtde_q4 ) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (id_aposta,impares,pares,SomaDezenas,soma_dos_digitos_das_dezenas,TotalDePrimos,qtdeDezFinonacci,qtde_q1, qtde_q2, qtde_q3, qtde_q4,))
    conn.commit()
    conn.close


def ContaTotalDeApostas():
    logging.info('Calculando total de apostas...') 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
			select count(*) Total from apostas6dezenas
			""")
    TotalDeApostas = int(cursor.fetchone()[0])
    logging.info('Total de apostas encontradas: ' + str(TotalDeApostas)) 
    conn.close()
    return TotalDeApostas


def MontaLoteDeApostas(id_inicial, id_final):
    logging.info('Montado lote de apostas ' + str(id_inicial) + ' - ' + str(id_final))
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()
    cursor.execute("""
			select id, dez01, dez02, dez03, dez04, dez05, dez06 
            from apostas6dezenas
            where id >= ? and id < ?
			""", (id_inicial, id_final, ))

    ListaDeApostas = cursor.fetchall()

    conn.close

    logging.info('lote de apostas finalizado.')
    return ListaDeApostas


def TrataCampo(linha):
    dezenas = []
    id_aposta = 0
    i = 0
    for campo in linha:
        i += 1
        if i == 1:
            id_aposta = campo
        else:
            dezenas.append(campo)
    return id_aposta, dezenas


def RefinaApostas01(ListaDeApostas):
    logging.info('Iniciando conexao o banco ApostasMegaSena ...') 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    id_aposta = 0
    dezenas = []
    contador = 0
    logging.info('Iniciando loop em apostas ...') 

    for linha in ListaDeApostas:
        id_aposta, dezenas = TrataCampo(linha)

        dezenas.sort()

        ### impares, pares, somadas dezenas
        impares, pares, SomaDezenas = CalculaParImparSomaDez(dezenas)
        ### soma digitos das dezenas
        soma_dos_digitos_das_dezenas = SomaDigitosDezenas(dezenas)
        ### Conta Primos
        TotalDePrimos = ContaPrimos(dezenas)

        ### Qtde dezenas por quadrante
        qtde_q1, qtde_q2, qtde_q3, qtde_q4 = ValidaDezenaNoQuadrante(dezenas)

        qtdeDezFinonacci = ValidaFibonacci(dezenas)

        m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30 = CalculaMultiplos(dezenas)

        TotNumquadraticos = CalculaQuadraticos(dezenas)

        TotalLinhas = CalculaLinhas(dezenas)

        TotalColunas = calculaColunas(dezenas)

        totConsecutivos = CalculaConsecutivos(dezenas)

        IntervalorDezenaOk = CalculaIntervaloDezena(dezenas)

        TotalDigitos = CalculaPresencaDigitos(dezenas)

        TotalParesDezenasEspelho = CalculaDezenasEspelho(dezenas)

        TotalDezenasQueMaisSaem = DezenasQueMaisSaem(dezenas)

        r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20 = CalculaPA(dezenas)

        cursor.execute("""
        INSERT INTO apostas6dezenasrefinadas (id, impares, pares, somadasdezenas, SomaDosDigitosDaDezena, TotalDePrimos, qtdeDezFinonacci, qtde_q1, qtde_q2, qtde_q3, qtde_q4,TotNumquadraticos, TotalLinhas, TotalColunas, totConsecutivos, IntervalorDezenaOk, TotalDigitos, TotalParesDezenasEspelho, TotalDezenasQueMaisSaem, r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (id_aposta,impares,pares,SomaDezenas,soma_dos_digitos_das_dezenas,TotalDePrimos,qtdeDezFinonacci,qtde_q1, qtde_q2, qtde_q3, qtde_q4, TotNumquadraticos, TotalLinhas, TotalColunas, totConsecutivos, IntervalorDezenaOk, TotalDigitos, TotalParesDezenasEspelho, TotalDezenasQueMaisSaem,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20, m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30,))

        contador += 1

        if contador == 500000:
            TempoFinal = datetime.datetime.now()
            TempoTotal = TempoFinal - TempoInicial
            logging.info('Total de Apostas salvas: ' + str(id_aposta) + ' - Tempo total: ' + str(TempoTotal)) 
            contador = 0
            TempoInicial = datetime.datetime.now()
            conn.commit()

    if contador > 0:
        conn.commit()

    conn.close

    logging.info('Fim')


def OrquestraRefinaApostas():
    Lotes = 0
    id_inicial = 0
    id_final = 0
    ListaDeApostas = []
    TotalDeApostas = ContaTotalDeApostas()
    if TotalDeApostas >= 1000000:
        Lotes = TotalDeApostas / 1000000
    
    for i in range(int(Lotes)+1):
        if i == 1: # inicio do calculo
            id_inicial = (i - 1)
            id_final = 1000000
            print('id inicial: {} id final: {}'.format(id_inicial,id_final))
            ListaDeApostas = MontaLoteDeApostas(id_inicial, id_final)
        else:
            id_inicial = (i - 1) * 1000000
            id_final = (i * 1000000)
            # print('id inicial: {} id final: {}'.format(id_inicial,id_final))
            ListaDeApostas = MontaLoteDeApostas(id_inicial, id_final)
        RefinaApostas01(ListaDeApostas)
        logging.info(str(i) + ' Lista de apostas finalizado.')
        print((str(i) + ' Lista de apostas finalizado.'))


if __name__ == '__main__':
    droptabelarefinada()
    criaTabelaApostasRefinadas()
    OrquestraRefinaApostas()
