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
    apostas = []
    apostas = EscolherNumeros()
    ultimosorteio = [15,36,45,51,52,59]
    totalApostas = 0
    r = 0
    while (totalApostas < 41):
        aposta = random.choices(apostas)
        for a in aposta:
            if a in ultimosorteio:
                r += 1
                print("r: {}".format(r))
        if r == 0:
            print("Aposta {}: {}".format(totalApostas, aposta))
            time.sleep(5)
            totalApostas += 1
        r = 0
def Imprimirnum01():
    apostas = []
    apostas = EscolherNumeros()
    print(len(apostas))
    ultimosorteio = [15,36,45,51,52,59]
    totalApostas = 0
    r = 0
    while (totalApostas < 41):
        time.sleep(60)
        aposta = random.choices(apostas)
        for a in aposta:
            for i in a:
                if i in ultimosorteio:
                    r += 1
        if r == 0:
            print('aposta: {} - {}'.format(totalApostas, aposta))    
            totalApostas += 1
        r = 0
def Imprimirnum02():
    print('Inicio Imprimirnum02 ...')
    apostas = []
    totalApostas = 0
    apostas = EscolherNumeros()
    print("Calculando total de apostas ...")
    totalApostas = len(apostas)
    print("Total de Apostas: {}".format(totalApostas))
    ultimosorteio = [15,36,45,51,52,59]
    totDezenas = 0
    r = 0
    while (totDezenas < 100):
        time.sleep(1)
        id = random.randrange(totalApostas)
        aposta = apostas[id]
        print('aposta: {} - {}'.format(totDezenas, aposta))    
        totDezenas += 1


if __name__ == '__main__':
    Imprimirnum02()
