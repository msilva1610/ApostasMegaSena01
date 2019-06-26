import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io

logging.basicConfig(filename='SalvaResultados.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('Inicio Salva Resultados')


def LerSorteios():
    sql = """
    INSERT INTO sorteios (Concurso,DataSorteio,dez01,dez02,dez03,dez04,dez05,dez06,
                         Arrecadacao_Total,Ganhadores_Sena,Cidade,UF,Rateio_Sena,Ganhadores_Quina,Rateio_Quina,
                         Ganhadores_Quadra,Rateio_Quadra,Acumulado,Valor_Acumulado,Estimativa_Premio,Acumulado_Mega_da_Virada)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    logging.info('Iniciando conexao o banco ApostasMegaSena ...') 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Lendo json')

    with io.open('sorteios.json', 'r', encoding='utf8', errors='ignore') as json_file:
        sorteios = json.load(json_file, strict=False)
        for linha in sorteios['sorteios']:
            cursor.execute(sql,(linha['Concurso'],linha['Data Sorteio'],
            linha['Dez01'],linha['Dez02'],linha['Dez03'],linha['Dez04'],linha['Dez05'],linha['Dez06'],
            linha['Arrecadacao_Total'],linha['Ganhadores_Sena'],linha['Cidade'],linha['UF'],
            linha['Rateio_Sena'],linha['Ganhadores_Quina'],linha['Rateio_Quina'],linha['Ganhadores_Quadra'],
            linha['Rateio_Quadra'],linha['Acumulado'],linha['Valor_Acumulado'],linha['Estimativa_Premio'],
            linha['Acumulado_Mega_da_Virada'],)) 
        conn.commit()
        conn.close()  
    logging.info('fim')
     


def droptabelasorteios():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS sorteios;")
    conn.close()


def criatabelasorteios():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('criando tabela caso não exista.')

    cursor.execute(""" 

    CREATE TABLE IF NOT EXISTS sorteios
    (Concurso INTEGER NOT NULL PRIMARY KEY,
     DataSorteio char(10),
     dez01 integer,
     dez02 integer,
     dez03 integer,
     dez04 integer,
     dez05 integer,
     dez06 integer,
     Arrecadacao_Total float,
     Ganhadores_Sena integer,
     Cidade text,
     UF char(2),
     Rateio_Sena float,
     Ganhadores_Quina integer,
     Rateio_Quina float,
     Ganhadores_Quadra integer,
     Rateio_Quadra float,
     Acumulado char(3),
     Valor_Acumulado float,
     Estimativa_Premio float,
     Acumulado_Mega_da_Virada float) 
    """)
    conn.close()

if __name__ == '__main__':
    droptabelasorteios()
    criatabelasorteios()
    LerSorteios()