def CalculaIntervaloDezena01(dezenas):
    IntervalorDezenaOk = True

    dezenas.sort()

    interdez01 = dezenas[0]
    interdez02 = dezenas[1]
    interdez03 = dezenas[2]
    interdez04 = dezenas[3]
    interdez05 = dezenas[4]
    interdez06 = dezenas[5]
 
    if (interdez01 > 26):
        IntervalorDezenaOk = False
    elif not (interdez02 >= 2 and interdez02 <= 37):
        IntervalorDezenaOk = False
    elif not (interdez03 >= 5 and interdez03 <= 47):
        IntervalorDezenaOk = False
    elif not (interdez04 >= 13 and interdez04 <= 54):
        IntervalorDezenaOk = False
    elif not (interdez05 >= 23 and interdez05 <= 59):
        IntervalorDezenaOk = False        
    elif not (interdez06 >= 35 and interdez06 <= 60):
        IntervalorDezenaOk = False   
    return IntervalorDezenaOk

def CalculaIntervaloDezena(dezenas):
    IntervalorDezenaOk = True
    dz = 0
    dezenas.sort()
    for d in dezenas:
        dz += 1
        if (d not in range(1,26) and dz == 1):
            IntervalorDezenaOk = False
        elif (d not in range(2,37) and dz == 2):
            IntervalorDezenaOk = False
        elif (d not in range(5,47) and dz == 3):
            IntervalorDezenaOk = False
        elif (d not in range(13,54) and dz == 4):
            IntervalorDezenaOk = False
        elif (d not in range(23,59) and dz == 5):
            IntervalorDezenaOk = False
        elif (d not in range(35,60) and dz == 6):
            IntervalorDezenaOk = False
    return IntervalorDezenaOk

dez = [1,2,5,13,23,35]
print(CalculaIntervaloDezena(dez))
print(CalculaIntervaloDezena01(dez))
