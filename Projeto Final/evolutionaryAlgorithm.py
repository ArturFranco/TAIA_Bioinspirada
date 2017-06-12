import numpy as np
import pandas as pd
import random
import time
import math

# ----- NUTRI INPUTS -----

_Kcal = 850
_rateProt = 0.26
_rateCarb = 0.4
_rateLip = 0.30
_rateFib = 0.04
_refeicaoIN = [('ARROZ INTEGRAL COZIDO',100),
              ('SALMAO SEM PELE FRESCO GRELHADO',100),
              ('BATATA INGLESA COZIDA',100)]

# -------------------------

_fProt = (_Kcal*_rateProt)
_fCarb = (_Kcal*_rateCarb)
_fLip = (_Kcal*_rateLip)
_fFib = (_Kcal*_rateFib)

_foodMaxArray = []

# -------------------------

_multiple = 5.0
_populationSize = 50
_haltCondition = 100
_error = 0.05
_pRecombination = 0.8
_pMutation = 0.8
_nRecombination = (_populationSize*7.0)/2.0
_strategy = 'AG' # or 'EE'

# -------------------------

alimentos = pd.read_csv('alimentos.csv', sep=';')
del alimentos['Unnamed: 0']

aux = pd.DataFrame()
aux['alimento'] = alimentos['alimento']
aux['proteina'] = alimentos['proteina'].apply(lambda x: x*4)
aux['lipideos'] = alimentos['lipideos'].apply(lambda x: x*9)
aux['carboidrato'] = alimentos['carboidrato'].apply(lambda x: x*4)
aux['fibras'] = alimentos['fibras'].apply(lambda x: x*4)

def isIn(num,min,max):

    if(num >= min and num <= max):
        return True
    return False

def foodMaxAmount(food):
    
    nutrient = aux.set_index('alimento').loc[food].idxmax()

    if nutrient == 'lipideos':
        fConv = 9
        fNutri = _fLip
    else:
        fConv = 4
        if nutrient == 'proteina':
            fNutri = _fProt
        elif nutrient == 'carboidrato':
            fNutri = _fCarb
        else:
            fNutri = _fFib

    qtdG = alimentos[alimentos.alimento == food][nutrient]

    maxAmount = ((fNutri/fConv)/qtdG)*100

    return math.floor((maxAmount/_multiple))*int(_multiple)

for food in _refeicaoIN:
	_foodMaxArray.append(foodMaxAmount(food[0]))

def createPopulation(populationSize, _refeicaoIN):
    population = []
    i = 0
    while i < populationSize:
        individual = []
        j = 0
        for food in _refeicaoIN:
            qtdMin = food[1]
            qtdMax = _foodMaxArray[j]
            #print(qtdMin, qtdMax)
            qtd = random.randint(qtdMin/_multiple, qtdMax/_multiple)*_multiple
            individual.append(qtd)
            j += 1

        fit = fitnessIndividual(individual)
        if fit != False:
            population.append(individual)
            i+= 1

    return population

def prot(df,qtd):
    return (qtd/100.0)*df.iloc[0]['proteina']

def carb(df,qtd):
    return (qtd/100.0)*df.iloc[0]['carboidrato']

def lip(df,qtd):
    return (qtd/100.0)*df.iloc[0]['lipideos']

def fib(df,qtd):
    return (qtd/100.0)*df.iloc[0]['fibras']

def fitnessIndividual(meal):
    sumProt = 0
    sumCarb = 0
    sumLip = 0
    sumFib = 0
    for i in range(0,len(meal)):
        aux = alimentos[alimentos.alimento == _refeicaoIN[i][0]]
        sumProt += prot(aux, meal[i])
        sumCarb += carb(aux, meal[i])
        sumLip += lip(aux, meal[i])
        sumFib += fib(aux, meal[i])

    sumProt *= 4
    sumCarb *= 4
    sumLip *= 9
    sumFib *= 4

    if((sumProt/_fProt > (1+_error)) or (sumCarb/_fCarb > (1+_error)) or (sumLip/_fLip > (1+_error)) or (sumFib/_fFib > (1+_error))):
        return False

    result = (sumProt/_fProt + sumCarb/_fCarb + sumLip/_fLip + sumFib/_fFib)/4.0
    return result

def fitnessPopulation(population):
    fitness = []
    i = 0
    for meal in population:
        mealFitness = fitnessIndividual(meal)
        fitness.append((i, mealFitness))
        i += 1

    return fitness

# Parents selection used in Genetic Algorithm
def parentsSelectionRoulette(population, fitness):

    maxFitness = sum([fitness[c][1] for c in range(len(population))])
    pick = random.uniform(0, maxFitness)

    current = 0
    for i, meal in enumerate(population):
        current += fitness[i][1]
        if current > pick:
            return meal

# Parents selection used in Evolutionary Strategy
def parentsSelectionRandom(population):
    parent1 = random.randint(0, len(population)-1)
    parent2 = random.randint(0, len(population)-1)
    while parent1 == parent2:
        parent2 = random.randint(0, len(population)-1)

    return population[parent1], population[parent2]

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

    if (fitnessIndividual(child1) > (1+_error)):
        child1 = parent1

    if (fitnessIndividual(child2) > (1+_error)):
        child2 = parent2

    return child1, child2

# Auxiliar function used in mutation
def defineSize(fit):

    if(isIn(fit,1,1+_error)):
        return -_multiple
    elif (isIn(fit,0.9,1)):
        return _multiple
    elif (isIn(fit,0.8,0.9)):
        return 2 * _multiple
    elif (isIn(fit,0.6,0.8)):
        return 3 * _multiple
    elif (isIn(fit,0.4,0.6)):
        return 4 * _multiple
    else:
        return 5 * _multiple

def goldMutation(individual):

    fit = fitnessIndividual(individual)
    sizeStep = defineSize(fit)
    
    aux = individual
    for i in range(len(individual)):
        aux[i] = aux[i] + sizeStep
        if(fitnessIndividual(aux) > (1+_error) or (aux[i] > _foodMaxArray[i])):
            aux[i] = individual[i]
    return aux

def nearestN(fitness):
    aux = []
    for element in fitness:
        aux.append((element[0], math.pow(1-element[1],2)))

    return sorted(aux, key=lambda x: x[1])

def survivalSelectionAG(population, fitness, N):

    aux = nearestN(fitness)
    worsts = aux[-N:]

    aux = []
    for element in worsts:
        aux.append(element[0])

    aux.sort(reverse=True)

    i = 0
    while i < N:
        del fitness[aux[i]]
        del population[aux[i]]
        i += 1

    return population, fitness

def survivalSelectionEE(population, N):

    fitness = fitnessPopulation(population)
    fitness = nearestN(fitness)

    aux = []
    for i in range(N):
        aux.append(population[fitness[i][0]])

    return aux

def evolutionaryAlgorithm():

    # create population
    population = createPopulation(_populationSize, _refeicaoIN)

    # calculate fitness population
    fitness = fitnessPopulation(population)

    i = 0
    while (i < _haltCondition and nearestN(fitness)[0][1] != 0):

        if(_strategy == 'AG'):
            # parents selection
            parent1 = parentsSelectionRoulette(population, fitness)
            parent2 = parentsSelectionRoulette(population, fitness)
            while parent1 == parent2:
                parent2 = parentsSelectionRoulette(population, fitness)

            # crossover
            if(random.random() < _pRecombination):
                child1, child2 = coinRecombination(parent1, parent2)
            else:
                child1 = parent1
                child2 = parent2

            # mutation
            if(random.random() < _pMutation):
                child1 = goldMutation(child1)
                child2 = goldMutation(child2)

            # evaluate childs
            population.append(child1)
            fitnessChild = (_populationSize, fitnessIndividual(child1))
            fitness.append(fitnessChild)
            population.append(child2)
            fitnessChild = (_populationSize+1, fitnessIndividual(child2))
            fitness.append(fitnessChild)

            # survival selection
            population, fitness = survivalSelectionAG(population, fitness,2)

            # recalculate fitness population
            fitness = fitnessPopulation(population)
            
        elif(_strategy == 'EE'):
            aux = []
            for i in range(int(_nRecombination)):
                # parents selection
                parent1 ,parent2 = parentsSelectionRandom(population)

                # crossover
                child1, child2 = coinRecombination(parent1, parent2)

                # mutation
                child1 = goldMutation(child1)
                child2 = goldMutation(child2)

                aux.append(child1)
                aux.append(child2)

            # survival selection
            population = survivalSelectionEE(aux, _populationSize)

            # recalculate fitness population
            fitness = fitnessPopulation(population)

        i +=1

    # taking best individual (solution)
    better = nearestN(fitness)[0]

    return population[better[0]]

if __name__ == '__main__':

    result = evolutionaryAlgorithm()

    print('Sua dieta e:')
    #print result
    i = 0
    for food in result:
        print(_refeicaoIN[i][0] + ' - quantidade: ' + str(food) + ' g')
        i += 1
