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
    ultimosorteio = [14,24,32,38,46,53]
    totDezenas = 0
    r = 0
    while (totDezenas < 28):
        proximo = False
        time.sleep(5)
        id = random.randrange(totalApostas)
        aposta = apostas[id]
        for a in aposta:
            if a in ultimosorteio:
                proximo = True
                break
        # print('aposta: {} - {} {} {} {} {} {}'.format(totDezenas, aposta))    
        if proximo:
            continue
        else:
            print("{:02d} {:02d} {:02d} {:02d} {:02d} {:02d}".format(aposta[1], aposta[2],aposta[3],aposta[4],aposta[5],aposta[6]))    
            totDezenas += 1


if __name__ == '__main__':
    Imprimirnum()
