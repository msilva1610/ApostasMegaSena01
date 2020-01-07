import json
import datetime
from concurrent.futures import ThreadPoolExecutor

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

def countQuinasbyDezenas(dezenas,quina):
    t = 0
    for d in dezenas:
        if d in quina:
            t += 1  
    return t


def dadoDexRetornaQtdeQuinas(idQuina):
    quina = quinas[idQuina]
    return quina

def dadoPalpiteretornaQuina(palpiteId):
    qtdeternos,qtdequadras,qtdequinas = 0,0,0
    palpite = palpites[palpiteId]
    t = 0
    id_aposta, dezenas = TrataCampo(palpite)
    # [1, 2, 6, 14, 26, 53]
    # with ThreadPoolExecutor(max_workers=None) as executor:
    #     for quina in executor.map(dadoDexRetornaQtdeQuinas, range(len(quinas))):
    for id in range(len(quinas)):
        quina = dadoDexRetornaQtdeQuinas(id)
        qtde = len(set(dezenas) & set(quina))
        if qtde == 3:
            qtdeternos += 1
        elif qtde == 4:
            qtdequadras += 1
        elif qtde == 5:
            qtdequinas += 1
    return {
        'id_aposta': id_aposta, 
        'dezenas': dezenas, 
        'qtdeternos': qtdeternos,
        'qtdequadras': qtdequadras,
        'qtdequinas': qtdequinas}


def findQuinasThreads():
    palpitesProcessed = {}
    palpitesProcessed['dezenas'] = []
    totalDePalpites = len(palpites)
    # totalDePalpites = 200

    for id in range(totalDePalpites):
        result = dadoPalpiteretornaQuina(id)
    # with ThreadPoolExecutor(max_workers=None) as executor:
    #     for result in executor.map(dadoPalpiteretornaQuina, range(totalDePalpites)):
    #         # print('response: {0}'.format(result))
    #         pass


def findQuinas(quinas, palpites):
    palpitesProcessed = {}
    palpitesProcessed['dezenas'] = []
    qtdeTernosSorteadas = 0
    qtdeQuadrasSorteadas = 0 
    qtdeQuinasSorteadas = 0
    for palpite in palpites:
        id_aposta, dezenas = TrataCampo(palpite)
        for quina in quinas: 
            qtde = countQuinasbyDezenas(dezenas,quina)
            # qtde = len(set(dezenas) & set(quina))
            if qtde == 3:
                qtdeTernosSorteadas += 1
            elif qtde == 4:
                qtdeQuadrasSorteadas += 1
            elif qtde == 5:
                qtdeQuinasSorteadas += 1
        palpitesProcessed['dezenas'].append({
            'id_aposta': int(id_aposta),
            'dezenas': dezenas,
            'qtdeTernosSorteadas': int(qtdeTernosSorteadas),
            'qtdeQuadrasSorteadas': int(qtdeQuadrasSorteadas),
            'qtdeQuinasSorteadas': int(qtdeQuinasSorteadas)
        })
        qtdeTernosSorteadas = 0
        qtdeQuadrasSorteadas = 0 
        qtdeQuinasSorteadas = 0
    return palpitesProcessed

    
def loadJson():
    with open('ListaDeQuinas.json') as json_file:
        ListaDeQuinas = json.load(json_file)
    with open('ListaPalpites.json') as json_file:
        ListaPalpites = json.load(json_file)
    return ListaDeQuinas, ListaPalpites

if __name__ == '__main__':
    global quinas
    global palpites

    start = datetime.datetime.now()
    quinas, palpites = loadJson()
    for i in range(20):
        data = findQuinas(quinas, palpites)
    # findQuinasThreads()
    end = datetime.datetime.now()
    print('Tempo total: {}'.format(end-start))