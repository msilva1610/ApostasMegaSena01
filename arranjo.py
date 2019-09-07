import itertools

def CalculaApostas(volante, numDezenas):
        apostas = list(itertools.combinations(volante, numDezenas))
        return apostas

d = [1,2,3,4,5,6,7,8]
size = 6
arr = CalculaApostas(d,size)
print(len(arr))
for i in arr:
    print(i)