import collections
import random
import numpy as np
#from sklearn.utils import shuffle
#import measure_algorithm as ma
import time
import pandas as pd

Kcal = 600
rateProt = 0.3
rateCarb = 0.4
rateLip = 0.25
rateFib = 0.05

fProt = (Kcal*rateProt)
fCarb = (Kcal*rateCarb)
fLip = (Kcal*rateLip)
fFib = (Kcal*rateFib)

alimentos = pd.read_csv('BDdefaultAlimentos.csv',sep=';')

def prot(df,qtd):
    return (qtd/100.0)*df.iloc[0][3]

def carb(df,qtd):
    return (qtd/100.0)*df.iloc[0][6]

def lip(df,qtd):
        return (qtd/100.0)*df.iloc[0][4]

def fib(df,qtd):
    return (qtd/100.0)*df.iloc[0][7]

#recebe um vetor de tuplas do tipo [(alimento,qtd)]
#ex: [(arroz,80),(feijao,100)]
def fitness(refeicao):
    somProt = 0
    somCarb = 0
    somLip = 0
    somFib = 0
    for alimento in refeicao:
        aux = alimentos[alimentos.alimento == alimento[0]]
        somProt += prot(aux,alimento[1])
        somCarb += carb(aux,alimento[1])
        somLip += lip(aux,alimento[1])
        somFib += fib(aux,alimento[1])
    somProt *= 4
    somCarb *= 4
    somLip *= 9
    somFib *= 4

    if (somProt > fProt or somCarb > fCarb or somLip > fLip or somFib > fFib):
        return 0

    return (somProt/fProt + somCarb/fCarb + somLip/fLip + somFib/fFib)/4.0


if __name__ == '__main__':

    refeicao = [('BATATA DOCE COZIDA',100),('FRANGO PEITO SEM PELE GRELHADO',200)]
    #refeicao = [('TESTE1',100),('TESTE2',100)]
    print(fitness(refeicao))
