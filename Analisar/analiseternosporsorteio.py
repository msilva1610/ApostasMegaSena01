import sqlite3
import sys
import os
import os.path
import json
import logging
import datetime
import io
import itertools


logging.basicConfig(filename='analisaternosporsorteio.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.info('inicio analisaternosporsorteio')


def dropTabelaContaTerno():

    BASE_DIR = "/Users/Mau/devops/2019/megasena/ApostasMegaSena01/"
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela contaterno caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS contaterno;")

    logging.info('Tabela contaterno apagada com sucesso.')

    conn.close()


def CriaTabelaContaTerno():
    sql = """
        CREATE TABLE IF NOT EXISTS contaterno
        (id INTEGER NOT NULL PRIMARY KEY,
         id_concurso INT NOT NULL,
         total int);
    """
    BASE_DIR = "/Users/Mau/devops/2019/megasena/ApostasMegaSena01/"
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Criando Tabela contaterno caso nãoo exista ...') 
    cursor.execute(sql)    

    conn.commit()
    conn.close()  
    logging.info('Tabela contaterno criada com sucesso')


def SalvaContaTernos(id_concurso,totalternos):
    # logging.info('Inserindo contaterno')

    sql = """
        INSERT INTO contaterno (id_concurso, total)
        VALUES (?,?);
    """
    BASE_DIR = "/Users/Mau/devops/2019/megasena/ApostasMegaSena01/"
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    cursor.execute(sql,(id_concurso,totalternos))

    conn.commit()
    cursor.close()
    # logging.info('Inserido registro na contaterno com sucesso')


def ContaTernosPorSorteio(id_concurso, ListaTernos):
    sql = """
        SELECT id_concurso 
        FROM sorteiosterno 
        where id_concurso < ?
        and   dezTerno01 = ?
        and   dezTerno02 = ?
        and   dezTerno03 = ?;
    """
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = "/Users/Mau/devops/2019/megasena/ApostasMegaSena01/"
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Lista de sorteio gerada com sucesso ...') 
    cursor.execute(sql,(int(id_concurso),int(ListaTernos[0]), int(ListaTernos[1]), int(ListaTernos[2]))  )  

    ListaSorteios = cursor.fetchall()

    # conn.commit()
    # print(id_concurso,int(ListaTernos[0]), ListaTernos[1], ListaTernos[2])
    conn.close()  
    logging.info('Contagem de ternos realizada com sucesso')
    return len(ListaSorteios)



def MontaListaSorteios():
    sql = """
        SELECT concurso, dez01, dez02, dez03, dez04, dez05, dez06 FROM sorteios;
    """
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = "/Users/Mau/devops/2019/megasena/ApostasMegaSena01/"
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    TempoInicial = datetime.datetime.now()

    logging.info('Lista de sorteio gerada com sucesso ...') 
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

def main():
    dropTabelaContaTerno()
    CriaTabelaContaTerno()
    
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

        ListaTernosPorSorteio = GeraTodasQuadras(DezenasSorteios,3)    
        for dezenas in ListaTernosPorSorteio:
            dezarr = (list(dezenas))
            dezarr.sort()
            ListaTernos['Ternos'].append({'id_concurso': id_concurso, 'TernoPorSorteio':list(dezarr)})
        
        id_concurso_anterior = 0
        totalternos = 0
        TernosCalculados = {}
        TernosCalculados['Ternos'] = []
        for dezena in ListaTernos['Ternos']:
            if dezena['id_concurso'] != id_concurso_anterior:
                if id_concurso_anterior != 0:
                    print(id_concurso_anterior, totalternos)
                id_concurso_anterior = dezena['id_concurso']
                totalternos = 0

            totalternos += ContaTernosPorSorteio(id_concurso_anterior,dezena['TernoPorSorteio'])
            SalvaContaTernos(id_concurso_anterior,totalternos)


if __name__ == '__main__':
    main()
