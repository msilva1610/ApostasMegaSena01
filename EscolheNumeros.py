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

logging.basicConfig(filename='EscolheNumeros.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio')

def EscolherNumeros():
    logging.info('Lendo Tabela apostas6dezenasrefinadas ')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()
    cursor.execute("""
			select a.id, dez01, dez02, dez03, dez04, dez05, dez06 
            from apostas6dezenas a, apostas6dezenasrefinadasplus b
            where a.id = b.id
			""",)

    ListaDeApostas = cursor.fetchall()

    conn.close

    logging.info('Lista de Numeros Refinados Gerado com sucesso.')
    return ListaDeApostas

def Imprimirnum():
    print('Inicio Imprimirnum02 ...')
    apostas = []
    totalApostas = 0
    apostas = EscolherNumeros()
    print("Calculando total de apostas ...")
    totalApostas = len(apostas)
    print("Total de Apostas: {}".format(totalApostas))
    ultimosorteio = [9,18,19,22,42,47]
    totDezenas = 0
    r = 0
    while (totDezenas < 28):
        time.sleep(5)
        id = random.randrange(totalApostas)
        aposta = apostas[id]
        for a in aposta:
            if a in ultimosorteio:
                continue
        print('aposta: {} - {}'.format(totDezenas, aposta))    
        totDezenas += 1


if __name__ == '__main__':
    Imprimirnum()
