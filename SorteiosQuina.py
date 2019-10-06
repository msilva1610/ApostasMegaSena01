import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io
import itertools


logging.basicConfig(filename='sorteioquina.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio')


def SalvaTodasQuadras01(ListaQuinas):
    logging.info('Inserindo lote na tabela sorteiosquina')

    sql = """
        INSERT INTO sorteiosquina (id_concurso, dezQuadra01,dezQuadra02,dezQuadra03,dezQuadra04, dezQuadra05)
        VALUES (?,?,?,?,?,?);
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for quina in ListaQuinas['Quinas']:
        id_concurso = quina['id_concurso']
        dezQuadra01 = quina['QuinaPorSorteio'][0]
        dezQuadra02 = quina['QuinaPorSorteio'][1]
        dezQuadra03 = quina['QuinaPorSorteio'][2]
        dezQuadra04 = quina['QuinaPorSorteio'][3]
        dezQuadra05 = quina['QuinaPorSorteio'][4]

        cursor.execute(sql,(id_concurso,dezQuadra01,dezQuadra02,dezQuadra03,dezQuadra04,dezQuadra05))

    conn.commit()
    cursor.close()
    logging.info('Lote Inserido com sucesso na tabela sorteiosquina')


def MontaListaSorteios():
    sql = """
        SELECT concurso, dez01, dez02, dez03, dez04, dez05, dez06 FROM sorteios;
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('executando select na tabela de concurso ...') 
    cursor.execute(sql)    

    ListaSorteios = cursor.fetchall()

    # conn.commit()
    conn.close()  
    logging.info('select na tabela sorteiosquina executado com sucesso')
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

    logging.info('apagando tabela sorteioquina caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS sorteiosquina;")

    logging.info('Tabela sorteioquina apagada com sucesso.')

    conn.close()


def CritaTabelaSorteioQuadra():
    sql = """
        CREATE TABLE IF NOT EXISTS sorteiosquina 
        (id INTEGER NOT NULL PRIMARY KEY,
         id_concurso INT NOT NULL,
         dezQuadra01 int,
         dezQuadra02 int,
         dezQuadra03 int,
         dezQuadra04 int,
         dezQuadra05 int);
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Criando Tabela sorteioquina caso nãoo exista ...') 
    cursor.execute(sql)    

    conn.commit()
    conn.close()  
    logging.info('Tabela sorteioquina criada com sucesso')


def Orquestrador():
    dropTabelaSorteioQuadra()
    CritaTabelaSorteioQuadra()
    ListaSorteios = MontaListaSorteios()

    DezenasSorteios = []
    ListaQuinas = {}
    ListaQuinas['Quinas'] = []
    contador = 0
    for linha in ListaSorteios:
        DezenasSorteios = []
        ListaQuinas['Quinas'] = []


        id_concurso = linha[0]
        DezenasSorteios.append(linha[1])
        DezenasSorteios.append(linha[2])
        DezenasSorteios.append(linha[3])
        DezenasSorteios.append(linha[4])
        DezenasSorteios.append(linha[5])
        DezenasSorteios.append(linha[6])
        DezenasSorteios.sort()

        ListaQuinasPorSorteio = GeraTodasQuadras(DezenasSorteios,5)    
        for quina in ListaQuinasPorSorteio:
            ListaQuinas['Quinas'].append({'id_concurso': id_concurso, 'QuinaPorSorteio':list(quina)})
        SalvaTodasQuadras01(ListaQuinas)


if __name__ == '__main__':
    Orquestrador()
    logging.info('Fim')

