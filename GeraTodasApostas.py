# -*- coding: utf-8 -*-
import itertools
class Apostas:
    '''
    Gera todas as combinações da mega sena de acordo com o número de apostas
    '''
    def __init__(self):
        self.volante = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
        self.apostas = []
    def CalculaApostas(self, numDezenas): 
        self.apostas = list(itertools.combinations(self.volante, numDezenas))
        return self.apostas



