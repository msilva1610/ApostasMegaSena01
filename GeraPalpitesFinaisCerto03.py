import sqlite3
import sys
import glob
import os
import os.path
import json
import logging
import datetime
from time import sleep
import progressbar
import requests

import threading
import multiprocessing

from multiprocessing.dummy import Pool

pool = Pool(4) # real    0m7.645s
# pool = Pool(1) # real    0m12.832s

futures = []

# logging.basicConfig(filename='GeraPalpitesFinais.log', level=logging.DEBUG,
#                     format=' %(asctime)s - %(levelname)s - %(message)s')

# logging.info('Inicio ...')

def contaQuinas(dezenas,quina):
    t = 0
    for d in dezenas:
        if d in quina:
            t += 1
    return t


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


def dropTabelapalpitesfinais():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Drop tabela palpitesfinais caso exista.')

    cursor.execute("""
        DROP TABLE IF EXISTS palpitesfinais;
    """)
    conn.commit()
    conn.close()


def criaTabelapalpitesfinais():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Criando a tabela palpitesfinais caso não exista.')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palpitesfinais
        (id INTEGER NOT NULL PRIMARY KEY,
         dez01 INT,
         dez02 INT,
         dez03 INT,
         dez04 INT,
         dez05 INT,
         dez06 INT,
         qtdeTernosSorteadas INT,
         qtdeQuadrasSorteadas INT,
         qtdeQuinasSorteadas INT,
         qtdeSenasSorteadas INT);
    """)
    conn.commit()
    conn.close()


def ListaPalpites01():
    sql = """
    SELECT a.id, a.dez01,a.dez02,a.dez03,a.dez04,a.dez05,a.dez06
    FROM apostas6dezenasrefinadascerta a
    WHERE a.impares = 1
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
    and a.m = 1;
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Gerando lista de palpites ...')

    cursor.execute(sql)

    ListaPalpites01 = cursor.fetchall()

    conn.commit()
    conn.close()

    return ListaPalpites01


def ListaDeQuinasSorteadas():
    sql = """
        select dezQuadra01,dezQuadra02,dezQuadra03,dezQuadra04,dezQuadra05
        from sorteiosquina;
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Gerando lista de quinas sorteadas.')

    cursor.execute(sql)

    ListaDeQuinas = cursor.fetchall()

    conn.commit()
    conn.close()

    return ListaDeQuinas


def Orquestrador():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()    
    sql = """
    INSERT INTO palpitesfinais
    (id, dez01, dez02, dez03, dez04, dez05, dez06, qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    contador = 0
    contadorPalpites = 0 
    # qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
    ListaDeQuinas = ListaDeQuinasSorteadas()
    ListaPalpites = ListaPalpites01()
    QtdePalpites = len(ListaPalpites)

    print('Quantidades de palpites: {}'.format(QtdePalpites))
    # logging.info('Iniciando loop em lista de palpites... ')
    bar = progressbar.ProgressBar(maxval=QtdePalpites, \
    widgets=[progressbar.Bar('=', '[', ']'), 'Processando ... ', progressbar.Percentage()])    
    bar.start()

    arrdata = []
    contaLista = 0
    contarequests = 0 
    futures = []
    for palpite in ListaPalpites:
        # qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
        contador += 1
        contadorPalpites += 1

        id_aposta, dezenas = TrataCampo(palpite)

        data = {'id_aposta':id_aposta, 'dezenas': dezenas, 'listaQuinas':ListaDeQuinas}
        arrdata.append(data)
        contaLista += 1 
        s = datetime.datetime.now()
        jsonData = json.dumps(arrdata)
        # jsonData = json.loads(str(arrdata))

        e = datetime.datetime.now() - s
        # print('Tempo parse: {} - len: {}'.format(e, len(arrdata)))
    #         # r = requests.post('http://localhost:8090/calcQuinas', data = jsonData)  
        if contaLista == 1:
            futures.append(pool.apply_async(requests.post,['http://localhost:8090/calcQuinas'],{'data': jsonData} ))
            contaLista = 0
            arrdata = []

        if contarequests == 1000:
            for future in futures:
                future.get().json()
            arrdata = []
            contarequests = 0
            futures = []
        bar.update(contadorPalpites)

    if contaLista > 0:
        futures.append(pool.apply_async(requests.post,['http://localhost:8090/calcQuinas'],{'data': jsonData} ))
        contaLista = 0
        arrdata = []

    if contarequests > 0:
        for future in futures:
            future.get().json()
        arrdata = []
        contarequests = 0
        futures = []
    bar.finish()


def Orquestrador01():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()    
    sql = """
    INSERT INTO palpitesfinais
    (id, dez01, dez02, dez03, dez04, dez05, dez06, qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    contador = 0
    contadorPalpites = 0 
    # qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
    # ListaDeQuinas = ListaDeQuinasSorteadas()
    ListaPalpites = ListaPalpites01()
    QtdePalpites = len(ListaPalpites)

    print('Quantidades de palpites: {}'.format(QtdePalpites))
    # logging.info('Iniciando loop em lista de palpites... ')
    bar = progressbar.ProgressBar(maxval=QtdePalpites, \
    widgets=[progressbar.Bar('=', '[', ']'), 'Processando ... ', progressbar.Percentage()])    
    bar.start()

    arrdata = []
    contaLista = 0
    contarequests = 0 
    futures = []
    for palpite in ListaPalpites:
        # qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
        contadorPalpites += 1

        id_aposta, dezenas = TrataCampo(palpite)

        data = {'id_aposta':id_aposta, 'dezenas': dezenas}
        arrdata.append(data)
        contaLista += 1 

        jsonData = json.dumps(arrdata)

        if contaLista == 1000:
            contarequests += 1000
            futures.append(pool.apply_async(requests.post,['http://localhost/calcQuinasInt'],{'data': jsonData} ))
            contaLista = 0
            arrdata = []

        if contarequests == 10000:
            for future in futures:
                # print(future.get())
                retornocalc = future.get().json()

                for retorno in retornocalc:
                    id_aposta = retorno['id_aposta']
                    qtdeTernosSorteadas = retorno['Ternos']
                    qtdeQuadrasSorteadas = retorno['Quadras']
                    qtdeQuinasSorteadas = retorno['Quinas']
                    qtdeSenasSorteadas = 0
                    dez01 = retorno['dezenas'][0]
                    dez02 = retorno['dezenas'][1]
                    dez03 = retorno['dezenas'][2]
                    dez04 = retorno['dezenas'][3]
                    dez05 = retorno['dezenas'][4]
                    dez06 = retorno['dezenas'][5]
                    # print(int(id_aposta), dez01, dez02, dez03, dez04, dez05, dez06, int(qtdeTernosSorteadas), int(qtdeQuadrasSorteadas), int(qtdeQuinasSorteadas), qtdeSenasSorteadas)
                    cursor.execute(sql, (int(id_aposta), dez01, dez02, dez03, dez04, dez05, dez06, int(qtdeTernosSorteadas), int(qtdeQuadrasSorteadas), int(qtdeQuinasSorteadas), qtdeSenasSorteadas,))            
                    contador += 1

            arrdata = []
            contarequests = 0
            futures = []

        if contador == 10000:
            logging.info('Salvando palpite ' + str(contadorPalpites))
            conn.commit()
            contador = 0

        bar.update(contadorPalpites)

    if contaLista > 0:
        futures.append(pool.apply_async(requests.post,['http://localhost:8090/calcQuinasInt'],{'data': jsonData} ))
        contaLista = 0
        arrdata = []

    if contarequests > 0:
        for future in futures:
            retornocalc = future.get().json()
            for retorno in retornocalc:
                id_aposta = retorno['id_aposta']
                qtdeTernosSorteadas = retorno['Ternos']
                qtdeQuadrasSorteadas = retorno['Quadras']
                qtdeQuinasSorteadas = retorno['Quinas']
                qtdeSenasSorteadas = 0
                dez01 = retorno[1]
                dez02 = retorno[2]  
                dez03 = retorno[3] 
                dez04 = retorno[4] 
                dez05 = retorno[5] 
                dez06 = retorno[6]
                cursor.execute(sql, (int(id_aposta), dez01, dez02, dez03, dez04, dez05, dez06, int(qtdeTernosSorteadas), int(qtdeQuadrasSorteadas), int(qtdeQuinasSorteadas), qtdeSenasSorteadas,))            
        arrdata = []
        contarequests = 0
        futures = []
    bar.finish()

    if contador > 0:
        conn.commit()
    conn.close()


if __name__ == '__main__':
    start = datetime.datetime.now()

    dropTabelapalpitesfinais()
    criaTabelapalpitesfinais()
    Orquestrador01()

    end = datetime.datetime.now() - start
    print("tempo total: {}".format(end))

    logging.info('Fim ...')