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
_halt = 1000
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

######################## SELECTION #################################
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

def roulette (population, numberIndividuals):
    fenotype = []
    for i in population:
        fenotype.append(bits_to_int_list(i[0],_expo))
    fitness = fitnessPopulation(fenotype)

    max     = sum([fitness[c][1] for c in range(len(population))])
    pick    = random.uniform(0, max)
    current = 0

    parents = []
    for j, chromosome in enumerate(population):
        current += fitness[j][1]
        if current > pick:
            if(len(parents) != numberIndividuals):
                parents.append(chromosome[0])

    if len(parents) < numberIndividuals:
        parents.append(population[0][0])

    return parents[0], parents[1]

##################### CROSSOVER ############################
def crossover(parent1, parent2):
    dimension = len(parent1)
    point = random.randint(1, dimension-1)
    subparents1 = [parent1[:point], parent1[point:]]
    subparents2 = [parent2[:point], parent2[point:]]
    child1 = subparents1[0] + subparents2[1]
    child2 = subparents2[0] + subparents1[1]
    offspring = [child1, child2]

    return child1, child2

def order_crossover(parent1, parent2):
    parent1 = bits_to_int_list(parent1, _expo)
    parent2 = bits_to_int_list(parent2, _expo)
    
    index1 = random.randint(0,_N-1)
    index2 = random.randint(index1+1,_N)
    
    subparent1 = parent1[index1:index2]
    subparent2 = parent2[index1:index2]
    parent_aux1 = parent1[index2:] + parent1[:index2]
    parent_aux2 = parent2[index2:] + parent2[:index2]
    subp_aux1 = []
    subp_aux2 = []
    
    for i in range(len(parent1)):
        if parent_aux2[i] not in subparent1:
            subp_aux2.append(parent_aux2[i])
        if parent_aux1[i] not in subparent2:
            subp_aux1.append(parent_aux1[i])
    
    new_index = len(parent1[index2:])
    child1 = subp_aux2[new_index:] + subparent1 + subp_aux2[:new_index]
    child2 = subp_aux1[new_index:] + subparent2 + subp_aux1[:new_index]
    offspring = [int_list_to_bits(child1, _expo), int_list_to_bits(child2, _expo)]
    
    return offspring

def alternative_crossover(parent1, parent2):
    parent1 = bits_to_int_list(parent1, _expo)
    parent2 = bits_to_int_list(parent2, _expo)
    index = random.randint(1,_dimension_-1)
    print(index)
    child1 = parent1[:index]
    child2 = parent2[:index]

    for i in range(_N):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        if parent1[i] not in child2:
            child2.append(parent1[i])
            
    offspring = [int_list_to_bits(child1, _expo), int_list_to_bits(child2, _expo)]
    
    return offspring

##################### MUTATION #############################
def mutation_Genotype(a):
    #Randomly select two indexs
    index = random.sample(range(0,len(a) -1), 2)
    #Permutation between two genes
    result = '' #Genetic
    for i in range(0,len(a)):
        if i == index[0]:
            result += a[index[1]]
        elif i == index[1]:
            result += a[index[0]]
        else:
            result += a[i]
    return result

def mutation_Fenotype(a):
    a = bits_to_int_list(a, _expo)
    #Randomly select two indexs
    index = random.sample(range(0,len(a) -1), 2)
    #Permutation between two genes
    result = []
    for i in range(0,len(a)):
        if i == index[0]:
            result += [a[index[1]]]
        elif i == index[1]:
            result += [a[index[0]]]
        else:
            result += [a[i]]
    return int_list_to_bits(result, _expo)

def inversion_mutation(child):
    child  = bits_to_int_list(child, _expo)

    index1 = random.randint(0,_dimension_-1)
    index2 = random.randint(index1+1, _dimension_)
    subchild = child[index1:index2]
    subchild = subchild[::-1]
    child = child[:index1] + subchild + child[index2:]
    
    return int_list_to_bits(child, _expo)

##################Survival Selection#########################
def survival_fitness_selection(population, n):
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

def survival_replacement_selection(population, parents, childs):
    count1 = 0
    count2 = 0

    for i in range(0,len(population)-1):
        if(count1 == 0 and (population[i][0] == parents[0])):
            population[i][0] = childs[0]
            count1 += 1
        elif(count2 == 0 and (population[i][0] == parents[1])):
            population[i][0] = childs[1]
            count2 +=1
        elif(count1 == 1 and count2 == 1):
            break
    
#########################################################################
def geneticAlgorithm(population,fenotype, types):
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
        if(types[3] == 1):
            parent1, parent2 = tournament(population,5)
        elif (types[3] == 2):
            parent1, parent2 = roulette(population,2)

        typeSolution1 = 0
        typeSolution2 = 0

        #apply crossover
        aux = random.randint(0,100)
        if aux <= 100*_recombinationProb:

            if(types[1] == 1):
                child1, child2 = crossover(parent1,parent2)
            elif(types[1] == 2):
                child1, child2 = order_crossover(parent1,parent2)
            elif(types[1] == 3):
                child1, child2 = alternative_crossover(parent1,parent2)

            #verify if child1 and child2 are solutions
            if NumberCollisions(bits_to_int_list(child1,_expo)) == 0:
                typeSolution1 = 1
            elif NumberCollisions(bits_to_int_list(child2,_expo)) == 0:
                typeSolution2 = 1
        else:
            child1,child2 = parent1,parent2

        if(types[2] == 2): survival_replacement_selection([parent1,parent2], [child1, child2])

        #apply mutation
        aux = random.randint(0,100)
        if aux <= 100*_mutationProb:

            if(types[0] == 1):
                child1 = mutation_Genotype(child1)
            elif(types[0] == 2):
                child1 = mutation_Fenotype(child1)
            elif(types[0] == 3):
                child1 = inversion_mutation(child1)

            typeSolution1 = 0
            #verify if child1 is solution
            if NumberCollisions(bits_to_int_list(child1,_expo)) == 0:
                typeSolution1 = 2

        aux = random.randint(0,100)
        if aux <= 100*_mutationProb:
            if(types[0] == 1):
                child2 = mutation_Genotype(child2)
            elif(types[0] == 2):
                child2 = mutation_Fenotype(child2)
            elif(types[0] == 3):
                child2 = inversion_mutation(child2)
            
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
        if(types[2] == 1): survival_fitness_selection(population, _offspring)

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

    # fenotype.append([5,2,4,7,0,3,1,6])
    for element in fenotype:
        population.append((int_list_to_bits(element,_expo),0,0))

    for i in range(1,3): #Mutation
        for j in range(1,3): #Crossover
            for t in range(1,2): #Survival Selection
                for u in range(1,2): #Parents Selection
                    print i,j,t,u
                    types = [i,j,t,u]
                    solutions, population, statistics = geneticAlgorithm(population, fenotype, types)

                    if __DEBUG:
                        fenotype = []

                        #Measure algorithm
                        if len(solutions) > 0:
                            if(len(solutions) != _population): "Parou sem todos convergirem"

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