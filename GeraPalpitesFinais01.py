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


logging.basicConfig(filename='GeraPalpitesFinais01.log', level=logging.DEBUG,
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


def ListaPalpites01():
    sql = """
    SELECT a.id, a.dez01,a.dez02,a.dez03,a.dez04,a.dez05,a.dez06
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
        # q = []
        q = 0
        for quina in ListaDeQuinas:
            #q = list(set(quina) & set(dezenas))
            #qtde = len(q)
            qtde = contaQuinas(dezenas,quina)
            if qtde == 3:
                qtdeTernosSorteadas += 1
            elif qtde == 4:
                qtdeQuadrasSorteadas += 1
            elif qtde == 5:
                qtdeQuinasSorteadas += 1 
            elif qtde == 6:
                qtdeSenasSorteadas += 1
        dez01 = dezenas[0]
        dez02 = dezenas[1]  
        dez03 = dezenas[2] 
        dez04 = dezenas[3] 
        dez05 = dezenas[4] 
        dez06 = dezenas[5]

        contadorPalpites += 1
        bar.update(contadorPalpites)
        if contador == 10000:
            logging.info('Salvando palpite ' + str(contadorPalpites))
            contador = 0

    
    bar.finish()
  

if __name__ == '__main__':
    Orquestrador()
    logging.info('Fim ...')