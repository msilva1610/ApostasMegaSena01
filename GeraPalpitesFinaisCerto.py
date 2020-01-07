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


logging.basicConfig(filename='GeraPalpitesFinais.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio ...')

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
    qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
    ListaDeQuinas = ListaDeQuinasSorteadas()
    ListaPalpites = ListaPalpites01()
    QtdePalpites = len(ListaPalpites)

    print('Quantidades de palpites: {}'.format(QtdePalpites))

    bar = progressbar.ProgressBar(maxval=QtdePalpites, \
        widgets=[progressbar.Bar('=', '[', ']'), 'Processando ... ', progressbar.Percentage()])    

    bar.start()
    logging.info('Iniciando loop em lista de palpites... ')
    for palpite in ListaPalpites:
        qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
        contador += 1
        id_aposta, dezenas = TrataCampo(palpite)
        for quina in ListaDeQuinas:
            # q = list(set(quina) & set(palpite))
            # qtde = len(q)
            qtde = contaQuinas(dezenas,quina)
            if qtde == 3:
                qtdeTernosSorteadas += 1
            elif qtde == 4:
                qtdeQuadrasSorteadas += 1
            elif qtde == 5:
                qtdeQuinasSorteadas += 1 
            elif qtde == 6:
                qtdeSenasSorteadas += 1
        dez01 = palpite[1]
        dez02 = palpite[2]  
        dez03 = palpite[3] 
        dez04 = palpite[4] 
        dez05 = palpite[5] 
        dez06 = palpite[6]

        cursor.execute(sql, (id_aposta, dez01, dez02, dez03, dez04, dez05, dez06, qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas,))
        contadorPalpites += 1
        bar.update(contadorPalpites)
        if contador == 10000:
            logging.info('Salvando palpite ' + str(contadorPalpites))
            conn.commit()
            contador = 0

    if contador > 0:
        conn.commit()
    
    conn.close()
    bar.finish()
  

if __name__ == '__main__':
    dropTabelapalpitesfinais()
    criaTabelapalpitesfinais()
    Orquestrador()
    logging.info('Fim ...')