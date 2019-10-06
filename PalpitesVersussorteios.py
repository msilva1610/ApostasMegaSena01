import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io
import itertools


logging.basicConfig(filename='PalpitesVersussorteios.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio')

def MontaListaSorteios():
    sql = """
        SELECT dez01, dez02, dez03, dez04, dez05, dez06 FROM sorteios;
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('executando select na tabela de sorteios ...') 
    cursor.execute(sql)    

    ListaSorteios = cursor.fetchall()

    conn.close()  
    logging.info('select na tabela sorteios executado com sucesso')
    return ListaSorteios

def MontaListaPalpites():
    sql = """
        SELECT dez01, dez02, dez03, dez04, dez05, dez06 FROM palpitesfinais;
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('executando select na tabela de palpites finais ...') 
    cursor.execute(sql)    

    ListaPalpites = cursor.fetchall()

    # conn.commit()
    conn.close()  
    logging.info('select na tabela concurso executado com sucesso')
    return ListaPalpites

def Orquestrador():
    ListaSorteios = []
    ListaSorteios = MontaListaSorteios()
    listaPalpites = MontaListaPalpites()
    totalPalpites = len(listaPalpites)
    totalSorteios = len(ListaSorteios)
    totalNaoEncontrados = 0

    for sorteio in ListaSorteios:
        sorted(sorteio)
        # [8, 9, 10, 24, 42, 44]
        s = tuple(sorted(sorteio))
        if (s not in listaPalpites):
            totalNaoEncontrados += 1
            print(s)
            if totalNaoEncontrados == 100: break

    print("Total de Palpites: {}".format(totalPalpites))
    print("Total de sorteios: {}".format(totalSorteios))
    print("Total de não encontrados: {}".format(totalNaoEncontrados))


if __name__ == '__main__':
    Orquestrador()
    logging.info('Fim')