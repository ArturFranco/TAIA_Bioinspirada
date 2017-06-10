import numpy as np
import pandas as pd
import random
import time
import math

# ----- NUTRI INPUTS -----

Kcal = 705
rateProt = 0.26
rateCarb = 0.4
rateLip = 0.30
rateFib = 0.04
refeicaoIN = [('ARROZ INTEGRAL COZIDO',100),
              ('SALMAO SEM PELE FRESCO GRELHADO',100),
              ('BATATA INGLESA COZIDA',100)]

# -------------------------
fProt = (Kcal*rateProt)
fCarb = (Kcal*rateCarb)
fLip = (Kcal*rateLip)
fFib = (Kcal*rateFib)

# -------------------------
_mesuare = 5.0
_populationSize = 50
_haltCondition = 500
_qtdBits = 6
_error = 0.05
_nRecombination = (_populationSize * 7.0)/2.0
_strategy = 0 #if 1 -> AG else -> EE
# -------------------------
alimentos = pd.read_csv('alimentos.csv', sep=';')
del alimentos['Unnamed: 0']

aux = pd.DataFrame()
aux['alimento'] = alimentos['alimento']
aux['proteina'] = alimentos['proteina'].apply(lambda x: x*4)
aux['lipideos'] = alimentos['lipideos'].apply(lambda x: x*9)
aux['carboidrato'] = alimentos['carboidrato'].apply(lambda x: x*4)
aux['fibras'] = alimentos['fibras'].apply(lambda x: x*4)

#    ok
def isIn(num,min,max):

    if(num >= min and num <= max):
        return True
    return False

#    ok
def foodMaxAmount(food):

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

    qtdG = alimentos[alimentos.alimento == food][nutrient]

    maxAmount = ((fNutri/fConv)/qtdG)*100

    return math.floor((maxAmount/_mesuare))*_mesuare

maxArray = []
for food in refeicaoIN:
    maxArray.append(foodMaxAmount(food[0]))
#print maxArray
#    ok
def createPopulation(populationSize, refeicaoIN):
    population = []
    i = 0
    while i < populationSize:
        individual = []
        j = 0
        for food in refeicaoIN:
            qtdMin = food[1]
            qtdMax = maxArray[j]
            #print(qtdMin, qtdMax)
            qtd = random.randint(qtdMin/_mesuare, qtdMax/_mesuare)*_mesuare
            individual.append(qtd)
            j += 1

        fit = fitnessIndividual(individual)
        if fit != False:
            if (isIn(fit,1-_error,1+_error)):
                population.append(individual)
                i+= 1
            #else:
            #    print 'erro'

    return population

#    ok
def prot(df,qtd):
    return (qtd/100.0)*df.iloc[0]['proteina']

def carb(df,qtd):
    return (qtd/100.0)*df.iloc[0]['carboidrato']

def lip(df,qtd):
    return (qtd/100.0)*df.iloc[0]['lipideos']

def fib(df,qtd):
    return (qtd/100.0)*df.iloc[0]['fibras']

#    ok
# Recebe um vetor de tuplas do tipo (alimento, qtd)
# Ex: [(arroz, 80), (feijao, 100), (carne, 150)]
def fitnessIndividual(meal):
    sumProt = 0
    sumCarb = 0
    sumLip = 0
    sumFib = 0

    for i in range(0,len(meal)):
        aux = alimentos[alimentos.alimento == refeicaoIN[i][0]]
        sumProt += prot(aux, meal[i])
        sumCarb += carb(aux, meal[i])
        sumLip += lip(aux, meal[i])
        sumFib += fib(aux, meal[i])
        #print(food[0] +' - '+ str(prot(aux, food[1])) +' - '+str(lip(aux, food[1])) +' - '+ str(carb(aux, food[1]))+' - '+ str(fib(aux, food[1])))
    sumProt *= 4
    sumCarb *= 4
    sumLip *= 9
    sumFib *= 4

    if((sumProt/fProt > (1+_error)) or  (sumCarb/fCarb > (1+_error)) or (sumLip/fLip > (1+_error)) or (sumFib/fFib > (1+_error))):
        return False
    #print ('p: '+str(sumProt)+' l: ' +str(sumLip) +' c: '+ str(sumCarb)+' f: '+ str(sumFib))
    result = (sumProt/fProt + sumCarb/fCarb + sumLip/fLip + sumFib/fFib)/4.0
    return result

#    ok
def fitnessPopulation(population):
    fitness = []
    i = 0
    for meal in population:
        mealFitness = fitnessIndividual(meal)
        fitness.append((i, mealFitness))
        i += 1

    return fitness

# NAO ENTENDI QUAL EH ESSA SELACAO DE PAIS
def parentsSelection1(population, fitness):

    maxFitness = sum([fitness[c][1] for c in range(len(population))])
    pick = random.uniform(0, maxFitness)

    current = 0
    for i, meal in enumerate(population):
        current += fitness[i][1]
        if current > pick:
            return meal

def parentsSelection2(population):
    parent1 = random.randint(0, len(population)-1)
    parent2 = random.randint(0, len(population)-1)
    while parent1 == parent2:
        parent2 = random.randint(0, len(population)-1)

    return population[parent1], population[parent2]

#   ok
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

def defineSize(fit):

    if(isIn(fit,1,1.1)):
        return -_mesuare
    elif (isIn(fit,0.9,1)):
        return _mesuare
    elif (isIn(fit,0.8,0.9)):
        return 2 * _mesuare
    elif (isIn(fit,0.6,0.8)):
        return 3 * _mesuare
    elif (isIn(fit,0.4,0.6)):
        return 4 * _mesuare
    else:
        return 5 * _mesuare

#como melhorar ? chamar o defineSize para cada alimento
#   ok
def mutation2(individual):

    fit = fitnessIndividual(individual)
    sizeStep = defineSize(fit)
    #print sizeStep
    aux = individual
    for i in range(len(individual)):
        aux[i] = aux[i] + sizeStep
        if(fitnessIndividual(aux) > (1+_error) or (aux[i] > maxArray[i])):
            aux[i] = individual[i]
    return aux

def nearestN(fitness):
    aux = []
    for element in fitness:
        aux.append((element[0],math.pow(1-element[1],2)))

    return sorted(aux, key=lambda x: x[1])

#   ok
def survivalSelection2(population, fitness,N):

    aux = nearestN(fitness)

    worsts = aux[-N:]

    aux = []
    for element in worsts:
        aux.append(element[0])

    aux.sort(reverse = True)

    i = 0
    while i < N:
        del fitness[aux[i]]
        del population[aux[i]]
        i += 1

    return population, fitness

def survivalSelection3(population,N):

    fitness = fitnessPopulation(population)

    fitness = nearestN(fitness)

    aux = []
    for i in range(N):
        aux.append(population[fitness[i][0]])

    return aux

def evolutiveAlgorithm():

    population = createPopulation(_populationSize, refeicaoIN)

    #fitnessArray = fitnessPopulation(population)
    fitness = fitnessPopulation(population)

    i = 0
    while (i < _populationSize and nearestN(fitness)[1] != 1):


        if(_strategy == 1):
            # Parents Selection
            parent1 = parentsSelection1(population, fitness)
            parent2 = parentsSelection1(population, fitness)
            while parent1 == parent2:
                parent2 = parentsSelection1(population, fitness)

            # Crossover
            child1, child2 = coinRecombination(parent1, parent2)

            # Mutation
            child1 = mutation2(child1)
            child2 = mutation2(child2)

            # Evaluate childs
            population.append(child1)
            fitnessChild = (_populationSize, fitnessIndividual(child1))
            fitness.append(fitnessChild)
            population.append(child2)
            fitnessChild = (_populationSize+1, fitnessIndividual(child2))
            fitness.append(fitnessChild)

            # Survival Selection
            population, fitness = survivalSelection2(population, fitness,2)

            fitness = fitnessPopulation(population)
        else:
            aux = []
            for i in range(int(_nRecombination)):
                # Parents Selection
                parent1 ,parent2 = parentsSelection2(population)

                # Crossover
                child1, child2 = coinRecombination(parent1, parent2)

                # Mutation
                child1 = mutation2(child1)
                child2 = mutation2(child2)

                aux.append(child1)
                aux.append(child2)

            # Survival Selection
            population = survivalSelection3(aux, _populationSize)

            fitness = fitnessPopulation(population)

        i +=1

    #print fitness
    #print fitness[nearestN(fitness)[0][0]]
    better = nearestN(fitness)[0]

    return population[better[0]]

if __name__ == '__main__':

    # print fitnessIndividual([100,100])
    # print foodMaxAmount('SALMAO SEM PELE FRESCO GRELHADO')
    # print foodMaxAmount('ARROZ INTEGRAL COZIDO')
    # population = createPopulation(10,refeicaoIN)
    # print population
    # fitness = fitnessPopulation(population)
    # print fitness
    # print coinRecombination([200,150],[130,120])
    # print mutation2([100,100])
    # print survivalSelection2([(0,0.97),(1,1),(2,1.01),(3,1.02),(4,1.03),(5,1.04),(6,1.003),(7,2),(8,0.05),(9,0.95)],[(0,0.97),(1,1),(2,1.01),(3,1.02),(4,1.03),(5,1.04),(6,1.003),(7,2),(8,0.05),(9,0.95)],2)

    result = evolutiveAlgorithm()

    print('Sua dieta e:')
    #print result
    i = 0
    for food in result:
        print(refeicaoIN[i][0] + ' - quantidade: ' + str(food) + ' g')
        i += 1
