# -*- coding: utf-8 -*-
import itertools
class GeraCombinacoesDezenas:
    '''
    Gera todas as combinações de um certo numero de dezenas
    '''
    def __init__(self):
        self.combinacoes = []
    def CalculaCombinacoes(self, dezenas, numDezenas): 
        self.combinacoes = list(itertools.combinations(dezenas, numDezenas))
        return self.combinacoes



