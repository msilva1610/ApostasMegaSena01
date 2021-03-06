import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io
import itertools


logging.basicConfig(filename='sorteioquadra.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Criando tabela sorteiosquadra')


def SalvaTodasQuadras01(ListaQuadras):
    logging.info('Inserindo lote na tabela sorteiosquadra')

    sql = """
        INSERT INTO sorteiosquadra (id_concurso, dezQuadra01,dezQuadra02,dezQuadra03,dezQuadra04)
        VALUES (?,?,?,?,?);
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    for quadra in ListaQuadras['Quadras']:
        id_concurso = quadra['id_concurso']
        dezQuadra01 = quadra['QuadrasPorSorteio'][0]
        dezQuadra02 = quadra['QuadrasPorSorteio'][1]
        dezQuadra03 = quadra['QuadrasPorSorteio'][2]
        dezQuadra04 = quadra['QuadrasPorSorteio'][3]

        cursor.execute(sql,(id_concurso,dezQuadra01,dezQuadra02,dezQuadra03,dezQuadra04))

    conn.commit()
    cursor.close()
    logging.info('Lote Inserido com sucesso na tabela sorteiosquadra')


def MontaListaSorteios():
    sql = """
        SELECT concurso, dez01, dez02, dez03, dez04, dez05, dez06 FROM sorteios;
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Criando Tabela sorteioquadra caso não exista ...') 
    cursor.execute(sql)    

    ListaSorteios = cursor.fetchall()

    # conn.commit()
    conn.close()  
    logging.info('Tabela sorteio quadra criada com sucesso')
    return ListaSorteios


def GeraTodasQuadras(sorteio, numDezenas):
    logging.info('Criando combinações')
    ListaCombinacoes = list(itertools.combinations(sorteio, numDezenas))
    logging.info('combinações criadas com sucesso')
    return ListaCombinacoes


def dropTabelaSorteioQuadra():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela sorteioquadra caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS sorteiosquadra;")

    logging.info('Tabela sorteio quadra apagada com sucesso.')

    conn.close()


def CritaTabelaSorteioQuadra():
    sql = """
        CREATE TABLE IF NOT EXISTS sorteiosquadra
        (id INTEGER NOT NULL PRIMARY KEY,
         id_concurso INT NOT NULL,
         dezQuadra01 int,
         dezQuadra02 int,
         dezQuadra03 int,
         dezQuadra04 int);
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Criando Tabela sorteioquadra caso nãoo exista ...') 
    cursor.execute(sql)    

    conn.commit()
    conn.close()  
    logging.info('Tabela sorteio quadra criada com sucesso')


def main():
    dropTabelaSorteioQuadra()
    CritaTabelaSorteioQuadra()
    ListaSorteios = MontaListaSorteios()

    DezenasSorteios = []
    ListaQuadras = {}
    ListaQuadras['Quadras'] = []
    contador = 0
    for linha in ListaSorteios:
        DezenasSorteios = []
        ListaQuadras['Quadras'] = []

        id_concurso = linha[0]
        DezenasSorteios.append(linha[1])
        DezenasSorteios.append(linha[2])
        DezenasSorteios.append(linha[3])
        DezenasSorteios.append(linha[4])
        DezenasSorteios.append(linha[5])
        DezenasSorteios.append(linha[6])
        DezenasSorteios.sort()

        ListaQuadrasPorSorteio = GeraTodasQuadras(DezenasSorteios,4)    
        for quadra in ListaQuadrasPorSorteio:
            ListaQuadras['Quadras'].append({'id_concurso': id_concurso, 'QuadrasPorSorteio':list(quadra)})
        SalvaTodasQuadras01(ListaQuadras)


if __name__ == '__main__':
    main()
