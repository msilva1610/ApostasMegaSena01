import requests
import zipfile


def DownloadingMegaSena():
    url = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip" 
    r = requests.get(url)
    with open("D_megase.zip", "wb") as code:
        code.write(r.content)

def unzipMegaSena():
    zip_ref = zipfile.ZipFile('D_megase.zip', 'r')
    # zip_ref.extractall(directory_to_extract_to)
    zip_ref.extractall()
    zip_ref.close()    

print('Fazendo download resultados megasena ...')
DownloadingMegaSena()
print('Descompactando resultados megasena ...')
unzipMegaSena()
