import sqlite3
import logging
import datetime
import json
import sys
import glob, os
import os.path

from GeraTodasApostas import Apostas


logging.basicConfig(filename='SalvaApostaSQLDB.log',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


def SalvaApostasDB(ListaDeApostas):
    try:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()   

        logging.info('Criando a tabela caso não exista.') 
       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS apostas6dezenas 
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
         dez01 interger, 
         dez02 interger,
         dez03 interger,
         dez04 interger,
         dez05 interger,
         dez06 interger);
        """)


        logging.info('Iniciando loop em todas as apostas e salvando na tabela apostas6dezenas.') 
        TempoInicial = datetime.datetime.now()
        id = 0
        contador = 0 
        for aposta in ListaDeApostas:
            contador += 1
            id += 1
            cursor.execute("""
                INSERT INTO apostas6dezenas (dez01, dez02, dez03, dez04, dez05, dez06) 
                VALUES (?,?,?,?,?,?)
                """, (aposta[0],aposta[1],aposta[2],aposta[3],aposta[4],aposta[5],))

            #conn.commit()
            if contador == 1000000:
                TempoFinal = datetime.datetime.now()
                TempoTotal = TempoFinal - TempoInicial
                logging.info('Total de Apostas salvas: ' + str(id) + ' - Tempo total: ' + str(TempoTotal)) 
                contador = 0
                conn.commit()
                #break
        
        if contador > 0:
            conn.commit()

        conn.close

    except Exception as e:
        logging.debug('Erro ocorreu em SalvaApostasDB. ' + str(e))  
    finally:
        if ListaDeApostas is not None:
            del ListaDeApostas
        if conn is not None:
            conn.close


def GeraTodasCombinacoesApostas():
    dezenas = 6
    clsApostas = Apostas()
    logging.info('Criando lista com todas as apostas.')  
    ListaDeApostas = clsApostas.CalculaApostas(dezenas)
    logging.info('Apostas criadas.') 
    return ListaDeApostas


def ApagaTabelaApostas():
    try:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "ApostasMegaSena.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()   

        logging.info('Apagando tabela caso exista.') 
       
        cursor.execute("""
        DROP TABLE IF EXISTS apostas6dezenas; 
        """)

        logging.info('Tabela apagada.') 

        conn.commit
        conn.close
    except Exception as e:
        logging.error('Erro ocorreu em ApagaTabelaApostas.' + str(e))  
    finally:
        if conn is not None:
            conn.close  

if __name__ == '__main__':
    try:
        logging.info('Incio.')    
        ApagaTabelaApostas()
        ListaDeApostas = GeraTodasCombinacoesApostas()
        SalvaApostasDB(ListaDeApostas)
        logging.info('Fim.')    
    
    except Exception as error:
        logging.debug('Erro ocorreu no main.' + str(error))  
