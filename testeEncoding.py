# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json
import io

html = """
 <html>
  <head>
  </head>
  <body>
    <p>Não!</p>    
  </body>
 </html>
"""

soup = None

resultados = {}
resultados['palavra'] = []

with open("acentos.html", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, "html.parser")

p = soup.find('p')

print(p)

#pp = str(p.string).encode('utf-8')

pp = str(p.string)


print(pp)

resultados['palavra'].append(pp)

print(resultados) 

# with open('acentos.json', 'w', encoding='utf8', errors='ignore') as outfile:  
#     json.dump(resultados, outfile)

with io.open('acentos.json', 'w', encoding='utf8') as outfile:
  json.dump(resultados, outfile,ensure_ascii=False)
