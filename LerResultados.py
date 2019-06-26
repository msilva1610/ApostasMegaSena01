# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json
import io

soup = None

# with open("d_mega.htm", encoding="utf-8") as fp:
# ('iso-8859-1')

# with open("d_mega.htm", encoding='utf-8', errors='ignore') as fp:

def formatDecimal(number):
    d = str(number).replace('.','')
    d = str(d).replace(',','')
    return (float(int(d)/100))

with open("d_mega.htm", 'rb') as fp:
    soup = BeautifulSoup(fp, "html.parser")

Tabela = soup.find('table')

resultados = {}
resultados['sorteios'] = []
contalinha = 0
for linha in Tabela.findAll('tr'):
    contalinha += 1
    td = linha.findAll('td')
    # print(len(td))
    if (len(td) == 21):
        resultados['sorteios'].append({
            'Concurso': int(td[0].string), 
            'Data Sorteio': td[1].string,
            'Dez01': int(td[2].string),'Dez02': int(td[3].string), 'Dez03': int(td[4].string), 'Dez04': int(td[5].string),'Dez05': int(td[6].string),'Dez06': int(td[7].string),
            'Arrecadacao_Total': formatDecimal(td[8].string),
            'Ganhadores_Sena': int(td[9].string),
            'Cidade': str(td[10].string).rstrip(),
            'UF': str(td[11].string).rstrip(),
            'Rateio_Sena': formatDecimal(td[12].string),
            'Ganhadores_Quina': int(td[13].string),
            'Rateio_Quina': formatDecimal(td[14].string),
            'Ganhadores_Quadra': int(td[15].string),
            'Rateio_Quadra': formatDecimal(td[16].string),
            'Acumulado': str(td[17].string).rstrip(),
            'Valor_Acumulado': formatDecimal(td[18].string),
            'Estimativa_Premio': formatDecimal(td[19].string),
            'Acumulado_Mega_da_Virada': formatDecimal(td[20].string),
            })

# for r in resultados:
#     print(r)

with io.open('sorteios.json', 'w', encoding='utf8', errors='ignore') as outfile:  
    json.dump(resultados, outfile, ensure_ascii=False)

