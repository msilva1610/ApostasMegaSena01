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


def dropTabelapalpitesfinais():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Criando a tabela palpitesfinais caso não exista.')

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
    SELECT a.dez01,a.dez02,a.dez03,a.dez04,a.dez05,a.dez06
    FROM apostas6dezenasrefinadasPlus b, apostas6dezenas a
    where a.id = b.id;
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
    (dez01, dez02, dez03, dez04, dez05, dez06, qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    contador = 0
    contadorPalpites = 0 
    qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas = 0,0,0,0
    ListaDeQuinas = ListaDeQuinasSorteadas()
    ListaPalpites = ListaPalpites01()
    QtdePalpites = len(ListaPalpites)

    bar = progressbar.ProgressBar(maxval=QtdePalpites, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])    

    bar.start()
    logging.info('Iniciando loop em lista de palpites... ')
    for palpite in ListaPalpites01():
        contador += 1
        for quina in ListaDeQuinas:
            q = list(set(quina) & set(palpite))
            qtde = len(q)
            if qtde == 3:
                qtdeTernosSorteadas += 1
            elif qtde == 4:
                qtdeQuadrasSorteadas += 1
            elif qtde == 5:
                qtdeQuinasSorteadas += 1 
            elif qtde == 6:
                qtdeSenasSorteadas += 1
        dez01 = palpite[0]
        dez02 = palpite[1]  
        dez03 = palpite[2] 
        dez04 = palpite[3] 
        dez05 = palpite[4] 
        dez06 = palpite[5]

        cursor.execute(sql, (dez01, dez02, dez03, dez04, dez05, dez06, qtdeTernosSorteadas, qtdeQuadrasSorteadas, qtdeQuinasSorteadas, qtdeSenasSorteadas,))

        if contador == 100000:
            logging.info('Salvando palpite ' + str(contadorPalpites + 1))
            cursor.commit()
            contador = 0

        contadorPalpites += 1
        bar.update(contadorPalpites)

    if contador > 0:
        cursor.commit()
    
    cursor.close()
    bar.finish()


def Teste04():
    dezenas = [1,2,3,4,5,6]
    quina = [1,2,3,4,5]
    TotalDezenas = list(set(dezenas) & set(quina))  # Encontra os iguais
    print(TotalDezenas)


def Teste03():
    l = ((1,2,3),(1,2,4),(1,2,5))
    #l = [[1,2,3],[1,2,4],[1,2,5]]
    a = l.index((1,2,5)) # funcionou
    print(a)


def TesteBarraProgressiva():
    bar = progressbar.ProgressBar(maxval=20, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(20):
        bar.update(i+1)
        sleep(5.1)
    bar.finish()    

if __name__ == '__main__':
    dropTabelapalpitesfinais()
    criaTabelapalpitesfinais()
    Orquestrador()
    #Teste03()
    # Teste04()
    # TesteBarraProgressiva()
    logging.info('Fim ...')