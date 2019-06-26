def CalculadezenasEspelho(dezenas):
    dez2d = []
    dezespelho = []
    dezenas.sort()
    totDezEspelho = 0
    for d in (dezenas):
        temp = "{:02d}".format(d)
        dez2d.append(temp)
    for dig in dez2d:
        digespelho = dig[1]+dig[0]
        if digespelho in dez2d:
            totDezEspelho += 1
            print(digespelho)
    return (totDezEspelho/2)

minhasDezenas = [2,3,14,20,30,41]
print(CalculadezenasEspelho(minhasDezenas))