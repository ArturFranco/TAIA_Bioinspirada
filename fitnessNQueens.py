import collections
import random
import numpy as np
from sklearn.utils import shuffle
import measure_algorithm as ma
import time

_population = 100
_offspring = 2
_N = 8
_expo = 3
_halt = 10000
_mutationProb = 0.4
_recombinationProb = 0.9
__DEBUG = 1

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

def NumberCollisions(individual):
    collisions = 0
    _size = len(individual)

    for i in range(0,len(individual)):
        collisions += collections.Counter(individual)[individual[i]] - 1
        #
        l = i - 1
        k = individual[i]-1
        while l >= 0 and k >= 0:
            if individual[l]  == k:
                collisions +=1
            l -= 1
            k -= 1
        #
        l = i + 1
        k = individual[i] + 1
        while l < _size and k < _size:
            if individual[l]  == k:
                collisions +=1
            l += 1
            k += 1
        #
        l = i - 1
        k = individual[i]+1
        while l >= 0 and k < _size:
            if individual[l]  == k:
                collisions +=1
            l -= 1
            k += 1
        #
        l = i + 1
        k = individual[i]-1
        while l < _size and k >= 0:
            if individual[l]  == k:
                collisions +=1
            l += 1
            k -= 1

    return collisions

def fitnessPopulation(population):
    fitness = []
    for i in range(0,len(population)):
        collisions = NumberCollisions(population[i])
        fitness.append((i,1.0/(1+collisions)))
    return fitness

def hasSolution(population,fenotype, fitness, g):
    result = []
    for i in fitness:
        if (i[1] == 1) and (population[i[0]][1] == 0):
            aux = list(population[i[0]])
            aux[1] = 1
            population[i[0]] = tuple(aux) #marca como solucao
            result.append((g,fenotype[i[0]],population[i[0]][2]))

    return result

def listElementsIndex(population, index):
    result = []

    for i in index:
        result.append(population[i])

    return result

#return the position of parent1 and parent2 in population
def tournament(poputalion, numberIndividuals):
    #choice 5 elements randomly
    positions = random.sample(range(0,_population), numberIndividuals)
    #get the subset of population by positions
    positions = listElementsIndex(population, positions)
    
    fenotype = []
    for i in positions:
        fenotype.append(bits_to_int_list(i[0],_expo))

    fitness = fitnessPopulation(fenotype)
    fitness.sort(key = lambda x: x[1], reverse = True)

    return positions[fitness[0][0]][0], positions[fitness[1][0]][0]

def recombination(parent1, parent2):
    dimension = len(parent1)
    point = random.randint(1, dimension-1)
    subparents1 = [parent1[:point], parent1[point:]]
    subparents2 = [parent2[:point], parent2[point:]]
    child1 = subparents1[0] + subparents2[1]
    child2 = subparents2[0] + subparents1[1]
    offspring = [child1, child2]

    return child1, child2

def mutation(a):
    #Randomly select two indexs
    index = random.sample(range(0,len(a) -1), 2)
    #Permutation between two genes
    result = ''
    for i in range(0,len(a)):
        if i == index[0]:
            result += a[index[1]]
        elif i == index[1]:
            result += a[index[0]]
        else:
            result += a[i]
    return result

def survivalSelection(population, n):
	#First, we sorted the population according fitness
	#get fenotype
    fenotype = []
    for element in population:
        fenotype.append(bits_to_int_list(element[0],_expo))

    fitness = fitnessPopulation(fenotype)
    fitness.sort(key=lambda x: x[1])

	#So, we remove the n worst population elements
    aux = []
    for i in range(0,n):
        aux.append(fitness[i][0])

    aux.sort(reverse = True)
    i = 0
    while i < n:
        del population[aux[i]]
        i += 1

def geneticAlgorithm(population,fenotype):
    generation  = 1
    solutions   = []
    fit     = fitnessPopulation(fenotype)
    fit.sort(key=lambda x: x[1], reverse = True)
    solutions.extend(hasSolution(population,fenotype,fit,generation))
    fitness     = []

    #Fitness, iteration = 0
    temp = []
    for i, l in enumerate(fit):
        temp.append(l[1])
    fitness.append(temp)
    
    while (generation < _halt) and (len(solutions) < _population):
        generation += 1
        #choice parents
        parent1, parent2 = tournament(population,5)
        typeSolution1 = 0
        typeSolution2 = 0
        #apply crossover
        aux = random.randint(0,100)
        if aux <= 100*_recombinationProb:
            child1, child2 = recombination(parent1,parent2)
            #verify if child1 and child2 are solutions
            if NumberCollisions(bits_to_int_list(child1,_expo)) == 0:
                typeSolution1 = 1
            elif NumberCollisions(bits_to_int_list(child2,_expo)) == 0:
                typeSolution2 = 1
        else:
            child1,child2 = parent1,parent2

        #apply mutation
        aux = random.randint(0,100)
        if aux <= 100*_mutationProb:
            child1 = mutation(child1)
            typeSolution1 = 0
            #verify if child1 is solution
            if NumberCollisions(bits_to_int_list(child1,_expo)) == 0:
                typeSolution1 = 2

        aux = random.randint(0,100)
        if aux <= 100*_mutationProb:
            child2 = mutation(child2)
            typeSolution2 = 0
            #verify if child2 is solution
            if NumberCollisions(bits_to_int_list(child2,_expo)) == 0:
                typeSolution2 = 2

        #add the children in population and get the solutions
        if NumberCollisions(bits_to_int_list(child1,_expo)) == 0:
            population.append((child1,1,typeSolution1))
            if len(solutions) < _population:
                solutions.append((generation,bits_to_int_list(child1,_expo),typeSolution1))
        else:
            population.append((child1,0,0))

        if NumberCollisions(bits_to_int_list(child2,_expo)) == 0:
            population.append((child2,1,typeSolution2))
            if len(solutions) < _population:
                solutions.append((generation,bits_to_int_list(child2,_expo),typeSolution2))
        else:
            population.append((child2,0,0))

        #get the survivors
        survivalSelection(population, 2)

        fenotype = []
        for element in population:
            fenotype.append(bits_to_int_list(element[0],_expo))

        fit     = fitnessPopulation(fenotype)
        temp    = []
        for i, l in enumerate(fit):
            temp.append(l[1])
        fitness.append(temp)

    if len(solutions) == 0:
        print 'Nao obteve sucesso'

    return solutions, population, fitness

if __name__ == '__main__':
    population = []
    fenotype   = []
    solutions  = []
    statistics = []
    i = 0

    #for force a quick solution->while i < _population-1:
    while i < _population:
        individual =  random.sample(range(0,_N), _N)
        if individual not in fenotype:
            fenotype.append(individual)
            i += 1

    fenotype.append([5,2,4,7,0,3,1,6])
    for element in fenotype:
        population.append((int_list_to_bits(element,_expo),0,0))

    solutions, population, statistics = geneticAlgorithm(population, fenotype)

    if __DEBUG:
        fenotype = []

        #Measure algorithm
        if len(solutions) > 0:
            ma.graph_type(solutions)
            ma.evolution_population(solutions, _halt)

            fit = []
            for i, l in enumerate(statistics):
                fit.append(np.mean(l))
            ma.plot_fitness(fit, "Fitness by iteration: Population")

            for element in solutions:
                fenotype.append(element[1])

            fitness = fitnessPopulation(fenotype)
            ma.config_individual(fenotype[fitness.index(max(fitness))])
        else: #Don't have any solution
            fit = []
            for i, l in enumerate(statistics):
                fit.append(np.mean(l))
            ma.plot_fitness(fit, "Fitness by iteration")

            for element in population:
                fenotype.append(bits_to_int_list(element[0],_expo))
            fitness = fitnessPopulation(fenotype)
            #The best of the worst
            ma.config_individual(fenotype[fitness.index(max(fitness))])