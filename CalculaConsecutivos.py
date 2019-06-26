def CalculaConsecutivos(dezenas):
    numAnterior = 1
    totConsecutivos = 0
    dezenas.sort()
    for d in dezenas:
        if (d - numAnterior) == 1:
            totConsecutivos += 1
        numAnterior = d
    return totConsecutivos

dezenas = [1,5,10,11,12,13]

print(CalculaConsecutivos(dezenas))