import sqlite3
import sys
import glob
import os
import os.path
import json
import logging
import datetime


logging.basicConfig(filename='RefinaApostasDB02Plus.log',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


def droptabelarefinadaPlus():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('apagando tabela caso não exista.')

    cursor.execute("DROP TABLE IF EXISTS apostas6dezenasrefinadasPlus;")
    conn.close()


def criatabelarefinadaPlus():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Criando a tabela caso não exista.')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apostas6dezenasrefinadasPlus
        (id INTEGER NOT NULL PRIMARY KEY,
         impares interger,
         pares interger,
         somadasdezenas interger,
         SomaDosDigitosDaDezena interger,
         TotalDePrimos interger,
         qtdeDezFinonacci interger,
		 qtde_q1 integer,
		 qtde_q2 integer,
		 qtde_q3 integer,
		 qtde_q4 integer,
         TotNumquadraticos integer,
         TotalLinhas integer,
         TotalColunas integer,
         totConsecutivos integer,
         IntervalorDezenaOk Boolean,
         TotalDigitos integer,
         TotalParesDezenasEspelho integer,
         TotalDezenasQueMaisSaem integer,
         r3 integer,
         r4 integer,
         r5 integer,
         r6 integer,
         r7 integer,
         r8 integer,
         r9 integer,
         r10 integer,
         r11 integer,
         r12 integer,
         r13 integer,
         r14 integer,
         r15 integer,
         r16 integer,
         r17 integer,
         r18 integer,
         r19 integer,
         r20 integer,
		 m3 integer,
		 m4 integer,
		 m5 integer,
		 m6 integer,
		 m7 integer,
		 m8 integer,
		 m9 integer,
		 m10 integer,
		 m11 integer,
		 m12 integer,
		 m13 integer,
		 m14 integer,
		 m15 integer,
		 m16 integer,
		 m17 integer,
		 m18 integer,
		 m19 integer,
		 m20 integer,
		 m21 integer,
		 m22 integer,
		 m23 integer,
		 m24 integer,
		 m25 integer,
		 m26 integer,
		 m27 integer,
		 m28 integer,
		 m29 integer,
		 m30 integer);
    """)
    # conn.commit()
    conn.close()


def GeratabelarefinadaPlus():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logging.info('Executando inser na table refinadaplus.')

    cursor.execute("""
        insert into apostas6dezenasrefinadasPlus
        SELECT *
        FROM apostas6dezenasrefinadas
        where (qtde_q1 >= 1 and qtde_q2 >= 1 and qtde_q3 >= 1 and qtde_q4 >= 1)
        and (pares not in (5,6,0))
        and (TotalDePrimos not in (4,5,6))
        and (qtdeDezFinonacci not in (3,4,5,6))
        and (somadasdezenas >= 102 and somadasdezenas <= 268)
        and (SomaDosDigitosDaDezena >= 27 and SomaDosDigitosDaDezena <= 58)
        and (m3 in (1,2,3) or (m4 in (0,1,2,3)) or (m5 in (0,1,2)) or (m6 in (0,1,2))
        or  (m7 in (0,1,2)) or (m8 in (0,1,2)) or (m9 in (0,1)) or (m10 in (0,1,2))
        or  (m11 in (0,1)) or (m12 in (0,1,2)) or (m13 in (0,1,2)) or (m14 in (0,1,2))
        or  (m15 in (0,1)) or (m16 in (0,1)) or (m17 in (0,1)) or (m18 in (0,1))
        or  (m19 in (0,1)) or (m20 in (0,1)) or (m21 in (0,1)) or (m22 in (0,1)) 
        or  (m22 in (0,1)) or (m23 in (0,1)) or (m24 in (0,1)) or (m25 in (0,1)) 
        or  (m26 in (0,1)) or (m27 in (0,1)) or (m28 in (0,1)) or (m29 in (0,1)) 
        or  (m30 in (0,1)))
        and totallinhas in (3,4,5)
        and totalcolunas in (4,5,6)
        and totconsecutivos in (0,1,2)
        and intervalordezenaok = 1
        and totaldigitos in (5,6,7,8)
        and totalparesdezenasespelho = 0
        and (r3 in (2,3) or r4 in (1,2) or r5 in (1,2) or r6 in (1,2) 
        or r7 in (1,2) or r8 in (1,2) or r9 in (1,2) or r10 in (0,1,2) or r11 in (0,1,2) 
        or r12 in (0,1,2) or r13 in (0,1) or r14 in (0,1) or r15 in (0,1) 
        or r16 in (0,1) or r17 in (0,1) or r18 in (0,1) or r19 in (0,1) or r20 in (0,1))
    """)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    logging.info('Inicio ...')
    droptabelarefinadaPlus()
    criatabelarefinadaPlus()
    GeratabelarefinadaPlus()
    logging.info('Fim ...')
