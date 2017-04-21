import collections
import random
import numpy as np
from sklearn.utils import shuffle

_poputalion = 100

_offspring = 2

_N = 8

_expo = 3

_halt = 10

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
            result.append((g,fenotype[i[0]]))
    return result

def geneticAlgorithm(population,fenotype):

    generation = 1

    solutions = []

    fitness = fitnessPopulation(fenotype)

    fitness.sort(key=lambda x: x[1], reverse = True)

    solutions.extend(hasSolution(population,fenotype,fitness,generation))

    print solutions
    


if __name__ == '__main__':

    population = []
    fenotype = []

    i = 0
    #inicializando a populacao
    while i < _poputalion:
        individual =  random.sample(range(0,_N), _N)
        if individual not in fenotype:
            fenotype.append(individual)
            i += 1
    #colocando os individuos na populacao, em string binaria
    for element in fenotype:
        population.append((int_list_to_bits(element,_expo),0))

    geneticAlgorithm(population, fenotype)
