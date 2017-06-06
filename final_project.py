import numpy as np
import pandas as pd
import random
import time
import math

# ----- NUTRI INPUTS -----

Kcal = 600
rateProt = 0.3
rateCarb = 0.4
rateLip = 0.25
rateFib = 0.05
refeicaoIN = [('BATATA DOCE COZIDA',100),
              ('FRANGO PEITO SEM PELE GRELHADO',200)]

# -------------------------

fProt = (Kcal*rateProt)
fCarb = (Kcal*rateCarb)
fLip = (Kcal*rateLip)
fFib = (Kcal*rateFib)

# -------------------------

_populationSize = 15
_haltCondition = 500
_qtdBits = 6

# -------------------------

def foodMaxAmount(df, food, fDict):
    aux = pd.DataFrame()
    aux['alimento'] = df['alimento']
    aux['proteina'] = df['proteina'].apply(lambda x: x*4)
    aux['lipideos'] = df['lipideos'].apply(lambda x: x*9)
    aux['carboidrato'] = df['carboidrato'].apply(lambda x: x*4)
    aux['fibras'] = df['fibras'].apply(lambda x: x*4)

    qtdKcal = aux.set_index('alimento').loc[food].max()
    nutrient = aux.set_index('alimento').loc[food].idxmax()
    
    if nutrient == 'lipideos':
        fConv = 9
        fNutri = fLip
    else:
        fConv = 4
        if nutrient == 'proteina':
            fNutri = fProt
        elif nutrient == 'carboidrato':
            fNutri = fCarb
        else:
            fNutri = fFib
    
    qtdG = df[df.alimento == food][nutrient]
    
    maxAmount = ((fNutri/fConv)/qtdG)*100
    
    return math.floor(maxAmount/10)*10

def createPopulation(populationSize, refeicaoIN):
    population = []
    for i in range(populationSize):
        individual = []
        for food in refeicaoIN:
            qtdMin = food[1]
            qtdMax = foodMaxAmount(alimentos, food[0], fDict)
            print(qtdMin, qtdMax)
            qtd = random.randint(qtdMin/10, qtdMax/10)*10
            individual.append(qtd)
            
        population.append(individual)
        
    return population

def prot(df,qtd):
    return (qtd/100.0)*df.iloc[0]['proteina']

def carb(df,qtd):
    return (qtd/100.0)*df.iloc[0]['carboidrato']

def lip(df,qtd):
    return (qtd/100.0)*df.iloc[0]['lipideos']

def fib(df,qtd):
    return (qtd/100.0)*df.iloc[0]['fibras']

# Recebe um vetor de tuplas do tipo (alimento, qtd)
# Ex: [(arroz, 80), (feijao, 100), (carne, 150)]
def fitness(meal):
    sumProt = 0
    sumCarb = 0
    sumLip = 0
    sumFib = 0
    for food in meal:
        aux = alimentos[alimentos.alimento == food[0]]
        sumProt += prot(aux, food[1])
        sumCarb += carb(aux, food[1])
        sumLip += lip(aux, food[1])
        sumFib += fib(aux, food[1])
        
    sumProt *= 4
    sumCarb *= 4
    sumLip *= 9
    sumFib *= 4

    if (sumProt > fProt or sumCarb > fCarb or sumLip > fLip or sumFib > fFib):
        return 0

    return (sumProt/fProt + sumCarb/fCarb + sumLip/fLip + sumFib/fFib)/4.0

def fitnessPopulation(population):
    fitness = []
    i = 0
    for meal in population:
        mealFitness = fitness(meal)
        fitness = [(i, mealFitness)]
        i += 1
    
    return fitness

def parentsSelection(population, fitness):
    
    maxFitness = sum([fitness[c][1] for c in range(len(population))])
    pick = random.uniform(0, maxFitness)
    
    current = 0
    for i, meal in enumerate(population):
        current += fitness[i][1]
        if current > pick:
            return meal

def int_list_to_bits(int_list, m):
    bits = ''
    for number in int_list:
        bits += format(number, '0'+str(m)+'b')
    return bits

def bits_to_int_list(bits, m):
    n = len(bits)
    if (n%m == 0):
        int_list = []
        for i in range(int(n/m)):
            bits_sliced = bits[(i*m):((i+1)*m)]
            number = int(bits_sliced, 2)
            int_list.append(number)
        return int_list
    print("'n' is not divisible by 'm'")

def coinRecombination(parent1, parent2):
    child1, child2 = [], []
    for i in range(len(parent1)):
        prob = random.random()
        if prob < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    
    return child1, child2

def mutation(individual):
    bitsIndividual = int_list_to_bits(individual, _qtdBits)
    mutated = ''
    for bit in bitsIndividual:
        prob = random.random()
        if prob < 0.5:
            mutated += bit
        else:
            if bit == '0':
                mutated += '1'
            else:
                mutated += '0'
    
    mutated = bits_to_int_list(mutated, _qtdBits)
    mutated = [math.floor(x/10)*10 for x in mutated]
    
    return mutated

def survivalSelection(population, fitness):
    worsts = sorted(fitness, key=lambda x: x[1])[-2:]
    for worst in worsts:
        del fitness[worst[0]]
        del population[worst[0]]
    
    return population, fitness 

def evolutiveAlgorithm():
    
    population = createPopulation(_populationSize, refeicaoIN)
    
    #fitnessArray = fitnessPopulation(population)
    
    for i in range(_haltCondition):
        
        fitness = fitnessPopulation(population)
        
        # Parents Selection
        parent1 = parentsSelection(population, fitness)
        parent2 = parentsSelection(population, fitness)
        while parent1 == parent2:
            parent2 = parentsSelection(population, fitness)
        
        # Crossover
        child1, child2 = coinRecombination(parent1, parent2)
        
        # Mutation
        child1 = mutation(child1)
        child2 = mutation(child2)
        
        # Evaluate childs
        population.append(child1)
        fitnessChild = (fitness[-1:][0]+1, fitness(child1))
        fitness.append(fitnessChild)
        population.append(child2)
        fitnessChild = (fitness[-1:][0]+1, fitness(child2))
        fitness.append(fitnessChild)
        
        # Survival Selection
        population, fitness = survivalSelection(population, fitness)
    
    better = sorted(fitness, key=lambda x: x[1])[0]
    
    return population[better[0]]

alimentos = pd.read_csv('alimentos.csv', sep=';')
del alimentos['Unnamed: 0']

result = evolutiveAlgorithm()

print('Sua dieta é:')
for food in result:
    print(food[0] + ' - quantidade: ' + str(food[1]) + 'g')