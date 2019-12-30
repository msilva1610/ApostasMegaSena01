import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io
import itertools


logging.basicConfig(filename='sorteioternos.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Criando tabela sorteiosternos')


def SalvaTodasTernos(ListaTernos):
    logging.info('Inserindo lote na tabela sorteiosterno')

    sql = """
        INSERT INTO sorteiosterno (id_concurso, dezTerno01,dezTerno02,dezTerno03)
        VALUES (?,?,?,?);
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    for terno in ListaTernos['Ternos']:
        id_concurso = terno['id_concurso']
        dezTerno01 = terno['TernosPorSorteio'][0]
        dezTerno02 = terno['TernosPorSorteio'][1]
        dezTerno03 = terno['TernosPorSorteio'][2]

        cursor.execute(sql,(id_concurso,dezTerno01,dezTerno02,dezTerno03))

    conn.commit()
    cursor.close()
    logging.info('Lote Inserido com sucesso na tabela sorteiosTerno')


def MontaListaSorteios():
    sql = """
        SELECT concurso, dez01, dez02, dez03, dez04, dez05, dez06 FROM sorteios;
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Selecionando sorteios na tabela de sorteios') 
    cursor.execute(sql)    

    ListaSorteios = cursor.fetchall()

    # conn.commit()
    conn.close()  
    logging.info('Tabela selecionada com sucesso')
    return ListaSorteios


def GeraTodasTernos(sorteio, numDezenas):
    logging.info('Criando combinações')
    ListaCombinacoes = list(itertools.combinations(sorteio, numDezenas))
    logging.info('combinações criadas com sucesso')
    return ListaCombinacoes


def dropTabelaSorteioTerno():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela sorteiosterno caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS sorteiosterno;")

    logging.info('Tabela sorteiosterno apagada com sucesso.')

    conn.close()


def CriarTabelaSorteiosTerno():
    sql = """
        CREATE TABLE IF NOT EXISTS sorteiosterno
        (id INTEGER NOT NULL PRIMARY KEY,
         id_concurso INT NOT NULL,
         dezTerno01 int,
         dezTerno02 int,
         dezTerno03 int);
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Criando Tabela sorteiosterno caso não exista ...') 
    cursor.execute(sql)    

    conn.commit()
    conn.close()  
    logging.info('Tabela sorteiosterno criada com sucesso')


def main():
    dropTabelaSorteioTerno()
    CriarTabelaSorteiosTerno()
    ListaSorteios = MontaListaSorteios()

    DezenasSorteios = []
    ListaTernos = {}
    ListaTernos['Ternos'] = []
    contador = 0
    for linha in ListaSorteios:
        DezenasSorteios = []
        ListaTernos['Ternos'] = []

        id_concurso = linha[0]
        DezenasSorteios.append(linha[1])
        DezenasSorteios.append(linha[2])
        DezenasSorteios.append(linha[3])
        DezenasSorteios.append(linha[4])
        DezenasSorteios.append(linha[5])
        DezenasSorteios.append(linha[6])
        DezenasSorteios.sort()

        ListaTernosPorSorteio = GeraTodasTernos(DezenasSorteios,3)    
        for terno in ListaTernosPorSorteio:
            dezenas = list(terno)
            ListaTernos['Ternos'].append({'id_concurso': id_concurso, 'TernosPorSorteio':list(dezenas)})
        SalvaTodasTernos(ListaTernos)


if __name__ == '__main__':
    main()
