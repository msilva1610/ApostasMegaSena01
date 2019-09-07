def combinacao(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    dezenas = tuple(iterable)
    n = len(dezenas)
    c = 0
    if r > n:
        return
    print('Indices inicial: {}'.format(list(range(r))))
    indices = list(range(r))
    print('Primeira combinacao: {}'.format(tuple(dezenas[i] for i in indices)))
    yield tuple(dezenas[i] for i in indices)
    # lógica para segunda combinação
    while True:
        for i in reversed(range(r)):
            c += 1
            print('{} - Inicio para segunda combinação. valor de i: {}'.format(c,i)) 
            print('>Valor de indices: {}'.format(indices[i]))
            print('Teste para segunda combinação: {} é diferente de {}'.format(indices[i],i + n - r))
            if indices[i] != i + n - r:
                print('Sim, sair do for: {} é diferente de {}'.format(indices[i],i + n - r))
                break
            elif indices[i] == i + n - r:
                print('Não, ficar do for: {} é igual a {}'.format(indices[i],i + n - r))

        else:
            print('Saindo do while')
            return
        indices[i] += 1
        print('>>>Novo valor de indices: {}'.format(indices[i]))
        print('>>>Valor de range(i+1,r): {} - r: {}'.format(range(i+1), r))
        for j in range(i+1, r):
            print('Valor de j: {}'.format(j))
            indices[j] = indices[j-1] + 1
            print('>>>>>Novo Valor de indices: {}'.format(indices[j]))
        print('{} - combinacoes: {}'.format(c, tuple(dezenas[i] for i in indices)))
        yield tuple(dezenas[i] for i in indices)

volante = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
a = [10,20,30,40]
print(list(combinacao(a,3)))