import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io
import itertools


logging.basicConfig(filename='ValidaFiltros.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio')


def InsertTabelaApostasRefinadasCerta(listaApostasRefinadas):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Inicio do loop em  listaApostasRefinadas ...') 

    for lstaf in listaApostasRefinadas:
        # Trata cada campo retornado
        campoTratado = trataCamposSQL(lstaf)
        for c in campoTratado['apostasrefinadas']:
            c1 = ValidaDezenas(c)
            campos = c1['Apostas']

            id = campos['id']
            dez01 = campos['dez01']
            dez02 = campos['dez02']
            dez03 = campos['dez03']
            dez04 = campos['dez04']
            dez05 = campos['dez05']
            dez06 = campos['dez06']
            impares = campos['impares']
            pares = campos['pares']
            quadrante  = campos['quadrante']
            totaldeprimos = campos['totaldeprimos']
            qtdeDezFinonacci = campos['qtdeDezFinonacci']
            somadasdezenas = campos['somadasdezenas']
            SomaDosDigitosDaDezena = campos['SomaDosDigitosDaDezena']
            TotNumquadraticos = campos['TotNumquadraticos']
            TotalColunas = campos['TotalColunas']
            totConsecutivos = campos['totConsecutivos']
            IntervalorDezenaOk = campos['IntervalorDezenaOk']
            TotalDigitos = campos['TotalDigitos']
            TotalParesDezenasEspelho = campos['TotalParesDezenasEspelho']
            razao = campos['razao']
            m = campos['m']

            cursor.execute("""
            INSERT INTO  (id,dez01,dez02,dez03,dez04,dez05,
                    dez06,impares,pares,quadrante,totaldeprimos,qtdeDezFinonacci,somadasdezenas,
                    SomaDosDigitosDaDezena,TotNumquadraticos,TotalColunas,totConsecutivos,
                    IntervalorDezenaOk,TotalDigitos,TotalParesDezenasEspelho,razao,m)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
            """, (id, dez01,dez02,dez03,dez04,dez05,dez06,impares,pares,quadrante,totaldeprimos,qtdeDezFinonacci,somadasdezenas,SomaDosDigitosDaDezena,TotNumquadraticos,TotalColunas,totConsecutivos,IntervalorDezenaOk,TotalDigitos,TotalParesDezenasEspelho,razao,m,))
    
    logging.info('Efetuando commit no banco ... ')
    conn.commit()
    conn.close


def droptabelarefinadaCerta():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS ;")
    conn.close()


def criaTabelaApostasRefinadasCerta():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Criando a tabela caso não exista.')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        (id INTEGER,
         dez01 INT,
         dez02 INT,
         dez03 INT,
         dez04 INT,
         dez05 INT,
         dez06 INT,
         impares Boolean,
         pares  Boolean,
         quadrante Boolean,
         totaldeprimos Boolean,
         qtdeDezFinonacci Boolean,
         somadasdezenas Boolean,
         SomaDosDigitosDaDezena Boolean,
         TotNumquadraticos Boolean,
         TotalColunas Boolean,
         totConsecutivos Boolean,
         IntervalorDezenaOk Boolean,
         TotalDigitos Boolean,
         TotalParesDezenasEspelho Boolean,
         razao Boolean,
         m Boolean);
    """)
    # conn.commit()
    conn.close()


def MontaListaApostasRefinadas(id_inicial, id_final):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Executando select na tabela de apostas6dezenasrefinadas ...') 
    cursor.execute("""
        SELECT b.*, a.dez01, a.dez02, a.dez03, a.dez04, a.dez05, a.dez06
        FROM apostas6dezenasrefinadas b, apostas6dezenas a
        where a.id = b.id
        and b.id > ? and b.id <= ?
    """, (id_inicial, id_final, )) 

    ListaPalpites = cursor.fetchall()

    # conn.commit()
    conn.close()  
    logging.info('Select na tabela apostas6dezenasrefinadas executado com sucesso')
    return ListaPalpites


def ValidaDezenas(campoTratado):
    listaApostachk = {}
    listaApostachk['Apostas'] = []
    par, impar, quadrante, totaldeprimos, qtdeDezFinonacci = False, False, False, False, False
    somadasdezenas, SomaDosDigitosDaDezena,TotalLinhas,TotNumquadraticos = False, False, False, False
    TotalColunas, totConsecutivos, IntervalorDezenaOk, TotalDigitos = False,False,False,False
    TotalParesDezenasEspelho, razao, m = False, False, False
    q=0

    if campoTratado['impares'] not in (0,6):
        par = True
    if campoTratado['pares'] not in (0,6):
        impar = True
    
    if (campoTratado['qtde_q1'] in (1,2,3)):
        q += 1
    if (campoTratado['qtde_q2'] in (1,2,3)):
        q += 1
    if (campoTratado['qtde_q3'] in (1,2,3)):
        q += 1 
    if (campoTratado['qtde_q4'] in (1,2,3)):
        q += 1
    # aceito um qudrante sem dezena(s)
    if q >= 3:
        quadrante = True
    # (TotalDePrimos not in (4,5,6))
    if (campoTratado['TotalDePrimos'] not in (4,5,6)):
        totaldeprimos = True
    # (qtdeDezFinonacci not in (3,4,5,6))
    if (campoTratado['qtdeDezFinonacci'] not in (3,4,5,6)):
        qtdeDezFinonacci = True
    # (somadasdezenas >= 102 and somadasdezenas <= 268)
    if (campoTratado['somadasdezenas'] >= 102 and campoTratado['somadasdezenas'] <= 268):
        somadasdezenas = True
    #  (SomaDosDigitosDaDezena >= 27 and SomaDosDigitosDaDezena <= 58)
    if (campoTratado['SomaDosDigitosDaDezena'] >= 27 and campoTratado['SomaDosDigitosDaDezena'] <= 58):
        SomaDosDigitosDaDezena = True
    # and totallinhas in (3,4,5)
    if (campoTratado['TotalLinhas'] in (3,4,5)):
        TotalLinhas = True
    # (qtdeDezFinonacci not in (3,4,5,6))
    if (campoTratado['TotNumquadraticos'] not in (3,4,5,6)):
        TotNumquadraticos = True
    # and totalcolunas in (4,5,6)
    if (campoTratado['TotalColunas'] in (4,5,6)):
        TotalColunas = True
    # and totconsecutivos in (0,1,2)
    if (campoTratado['totConsecutivos'] in (0,1,2)):
        totConsecutivos = True    
    # and intervalordezenaok = 1
    if (campoTratado['IntervalorDezenaOk'] == 1):
        IntervalorDezenaOk = True 
    # and totaldigitos in (5,6,7,8)        
    if (campoTratado['TotalDigitos'] in (5,6,7,8)):
        TotalDigitos = True 
    # and totalparesdezenasespelho = 0
    if (campoTratado['TotalParesDezenasEspelho'] <= 1):
        TotalParesDezenasEspelho = True 
    r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20 = \
        campoTratado['r3'],campoTratado['r4'], campoTratado['r5'], campoTratado['r6'], \
        campoTratado['r7'], campoTratado['r8'], campoTratado['r9'], \
        campoTratado['r10'],campoTratado['r11'], campoTratado['r12'], campoTratado['r13'], \
        campoTratado['r14'], campoTratado['r15'], campoTratado['r16'], campoTratado['r17'], \
        campoTratado['r18'], campoTratado['r19'], campoTratado['r20']    

    if (r3 in (2,3) or r4 in (1,2) or r5 in (1,2) or r6 in (1,2) or \
        r7 in (1,2) or r8 in (1,2) or r9 in (1,2) or r10 in (0,1,2) or \
        r11 in (0,1,2) or r12 in (0,1,2) or r13 in (0,1) or r14 in (0,1) or r15 in (0,1) or \
        r16 in (0,1) or r17 in (0,1) or r18 in (0,1) or r19 in (0,1) or r20 in (0,1)):
        razao = True

    m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30 = \
        campoTratado['m3'],campoTratado['m4'],campoTratado['m5'],campoTratado['m6'], \
        campoTratado['m7'],campoTratado['m8'],campoTratado['m9'],campoTratado['m10'], \
        campoTratado['m11'],campoTratado['m12'],campoTratado['m13'],campoTratado['m14'], \
        campoTratado['m15'],campoTratado['m16'],campoTratado['m17'],campoTratado['m18'], \
        campoTratado['m19'],campoTratado['m20'],campoTratado['m21'],campoTratado['m22'], \
        campoTratado['m23'],campoTratado['m24'],campoTratado['m25'],campoTratado['m26'], \
        campoTratado['m27'],campoTratado['m28'],campoTratado['m29'],campoTratado['m30']

    if (m3 in (1,2,3) or (m4 in (0,1,2,3)) or (m5 in (0,1,2)) or (m6 in (0,1,2)) \
        or  (m7 in (0,1,2)) or (m8 in (0,1,2)) or (m9 in (0,1)) or (m10 in (0,1,2)) \
        or  (m11 in (0,1)) or (m12 in (0,1,2)) or (m13 in (0,1,2)) or (m14 in (0,1,2)) \
        or  (m15 in (0,1)) or (m16 in (0,1)) or (m17 in (0,1)) or (m18 in (0,1)) \
        or  (m19 in (0,1)) or (m20 in (0,1)) or (m21 in (0,1)) or (m22 in (0,1)) \
        or  (m22 in (0,1)) or (m23 in (0,1)) or (m24 in (0,1)) or (m25 in (0,1)) \
        or  (m26 in (0,1)) or (m27 in (0,1)) or (m28 in (0,1)) or (m29 in (0,1)) \
        or  (m30 in (0,1))):
        m = True


    listaApostachk['Apostas'] = {
        'id': campoTratado['id'],
        'dez01': campoTratado['dez01'],
        'dez02': campoTratado['dez02'],
        'dez03': campoTratado['dez03'],
        'dez04': campoTratado['dez04'],
        'dez05': campoTratado['dez05'],
        'dez06': campoTratado['dez06'],
        'impares': impar,
        'pares': par,
        'quadrante': quadrante,
        'totaldeprimos': totaldeprimos,
        'qtdeDezFinonacci': qtdeDezFinonacci,
        'somadasdezenas': somadasdezenas,
        'SomaDosDigitosDaDezena': SomaDosDigitosDaDezena,
        'TotNumquadraticos': TotNumquadraticos,
        'TotalColunas': TotalColunas,
        'totConsecutivos': totConsecutivos,
        'IntervalorDezenaOk': IntervalorDezenaOk,
        'TotalDigitos': TotalDigitos,
        'TotalParesDezenasEspelho': TotalParesDezenasEspelho,
        'razao': razao,
        'm': m,
    }
    

    return listaApostachk


def trataCamposSQL(listaApostas):
    listaTratada = {}
    listaTratada['apostasrefinadas'] = []
    listaTratada['apostasrefinadas'].append({
        'id': int(listaApostas[0]),
        'impares': int(listaApostas[1]),
        'pares': int(listaApostas[2]),
        'somadasdezenas': int(listaApostas[3]),
        'SomaDosDigitosDaDezena': int(listaApostas[4]),
        'TotalDePrimos': int(listaApostas[5]),
        'qtdeDezFinonacci': int(listaApostas[6]),
        'qtde_q1' : int(listaApostas[7]),
        'qtde_q2' : int(listaApostas[8]),
        'qtde_q3' : int(listaApostas[9]),
        'qtde_q4' : int(listaApostas[10]),
        'TotNumquadraticos': int(listaApostas[11]),
        'TotalLinhas': int(listaApostas[12]),
        'TotalColunas': int(listaApostas[13]),
        'totConsecutivos': int(listaApostas[14]),
        'IntervalorDezenaOk': int(listaApostas[15]),
        'TotalDigitos' : int(listaApostas[16]),
        'TotalParesDezenasEspelho': int(listaApostas[17]),
        'TotalDezenasQueMaisSaem': int(listaApostas[18]),
        'r3': int(listaApostas[19]),
        'r4': int(listaApostas[20]),
        'r5': int(listaApostas[21]),
        'r6': int(listaApostas[22]),
        'r7': int(listaApostas[23]),
        'r8': int(listaApostas[24]),
        'r9': int(listaApostas[25]),
        'r10': int(listaApostas[26]),
        'r11': int(listaApostas[27]),
        'r12': int(listaApostas[28]),
        'r13': int(listaApostas[29]),
        'r14': int(listaApostas[30]),
        'r15': int(listaApostas[31]),
        'r16': int(listaApostas[32]),
        'r17': int(listaApostas[33]),
        'r18': int(listaApostas[34]),
        'r19': int(listaApostas[35]),
        'r20': int(listaApostas[36]),
        'm3': int(listaApostas[37]),
        'm4': int(listaApostas[38]),
        'm5': int(listaApostas[39]),
        'm6': int(listaApostas[40]),
        'm7': int(listaApostas[41]),
        'm8': int(listaApostas[42]),
        'm9': int(listaApostas[43]),
        'm10': int(listaApostas[44]),
        'm11': int(listaApostas[45]),
        'm12': int(listaApostas[46]),
        'm13': int(listaApostas[47]),
        'm14': int(listaApostas[48]),
        'm15': int(listaApostas[49]),
        'm16': int(listaApostas[50]),
        'm17': int(listaApostas[51]),
        'm18': int(listaApostas[52]),
        'm19': int(listaApostas[53]),
        'm20': int(listaApostas[54]),
        'm21': int(listaApostas[55]),
        'm22': int(listaApostas[56]),
        'm23': int(listaApostas[57]),
        'm24': int(listaApostas[58]),
        'm25': int(listaApostas[59]),
        'm26': int(listaApostas[60]),
        'm27': int(listaApostas[61]),
        'm28': int(listaApostas[62]),
        'm29': int(listaApostas[63]),
        'm30': int(listaApostas[64]),
        'dez01': int(listaApostas[65]),
        'dez02': int(listaApostas[66]),
        'dez03': int(listaApostas[67]),
        'dez04': int(listaApostas[68]),
        'dez05': int(listaApostas[69]),
        'dez06': int(listaApostas[70]),
    })
    return listaTratada


def Orquestrador():
    totalDeApostas = 50000000
    Lotes = 0
    id_inicial = 0
    id_final = 0
    ListaDeApostas = []
    if totalDeApostas >= 1000000:
        Lotes = totalDeApostas / 1000000    

    for i in range(int(Lotes)+1):
        if i == 1: # inicio do calculo
            id_inicial = (i - 1)
            id_final = 1000000
            logging.info('id inicial: ' + str(id_inicial) + ' - Id final: ' + str(id_final)) 
            listaApostasRefinadas = MontaListaApostasRefinadas(id_inicial, id_final)
            InsertTabelaApostasRefinadasCerta(listaApostasRefinadas)
        else:
            id_inicial = (i - 1) * 1000000
            id_final = (i * 1000000)
            logging.info('id inicial: ' + str(id_inicial) + ' - Id final: ' + str(id_final)) 
            listaApostasRefinadas = MontaListaApostasRefinadas(id_inicial, id_final)
            InsertTabelaApostasRefinadasCerta(listaApostasRefinadas)

def main():
    droptabelarefinadaCerta()
    criaTabelaApostasRefinadasCerta()
    Orquestrador()
    logging.info('Fim')

if __name__ == '__main__':
    main()
