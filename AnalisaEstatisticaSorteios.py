import sqlite3
import sys
import glob
import os
import os.path
import json
import logging
import datetime
import random
import time
import RefinaApostasDB02

logging.basicConfig(filename='AnalisaEstatisticaSorteios.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio')

def SelecionaSorteios():
    logging.info('Lendo Tabela sorteios ')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()
    cursor.execute("""
			select dez01, dez02, dez03, dez04, dez05, dez06 
            from sorteios
			""",)

    sorteios = cursor.fetchall()

    conn.close

    logging.info('Lista de sorteios criada com sucesso.')
    return sorteios


def CalculaEstatistica():
    q1,q2,q3,q4 = 0,0,0,0
    sq1,sq2,sq3,sq4 = 0,0,0,0
    totalSorteios = 0
    listaSorteios = SelecionaSorteios()
    totalSorteios = len(listaSorteios)
    q = 0
    for dezenas in listaSorteios:
        sorted(dezenas)
        q1,q2,q3,q4 = RefinaApostasDB02.ValidaDezenaNoQuadrante(dezenas)
        if q1 == 0:
            sq1 += 1
        if q2 == 0:
            sq2 += 1
        if q3 == 0:
            sq3 += 1            
        if q4 == 0:
            sq4 += 1
    print('Quadrantes na aposta q1: {} - {}'.format(sq1, round(100 * float(sq1) / float(totalSorteios))))
    print('Quadrantes na aposta q2: {} - {}'.format(sq2, round(100 * float(sq2) / float(totalSorteios))))
    print('Quadrantes na aposta q3: {} - {}'.format(sq3, round(100 * float(sq3) / float(totalSorteios))))
    print('Quadrantes na aposta q4: {} - {}'.format(sq4, round(100 * float(sq4) / float(totalSorteios))))




if __name__ == '__main__':
    CalculaEstatistica()
