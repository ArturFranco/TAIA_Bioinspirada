import numpy  as np
import random
from sklearn.utils import shuffle
#Define the size of population
_population_ = 100

#Define the size of offspring
_offspring_ = 2

#Define dimensions of board (dimension x dimension)
_dimension_ = 8 

#Halt condition
_halt_ = 10

#Auxiliary function to sort the population
def sortedPopulation(fitness, parents, status):
	fit, parents, st = zip(*sorted(zip(fitness, parents, status)))
	return fit, list(parents), list(st)

def mutation(individual):
	index = random.sample(range(0,_dimension_), 2) #Randomly select two indexs
	#Permutation between two genes
	individual[index[0]], individual[index[1]] = individual[index[1]], individual[index[0]]

def recombination(parent1, parent2):
	index = random.sample(range(0,_dimension_), 1) #Randomly select an index
	#Two offsprings which will be generated
	offspring = [parent1[x] for x in xrange(index[0])]

	if len(offspring) < len(parent1):
		i = index[0]
		while i < len(parent1):
			if parent2[i] not in offspring:
				offspring.append(parent2[i])

			i = i+1
			#i is maximum and the size of offspring is less than size of individual
			if ((i == len(parent1)) and (len(offspring) < _dimension_)):
				i = 0
	return offspring
	
def survivalSelection(fitness, population, status):
	#First, we sorted the population according fitness
	fitness, population, status = sortedPopulation(fitness, population, status)
	#So, we remove the worst population elements
	for x in xrange(_offspring_):
		del population[-1]

def calculateFitness(individual):
	return individual[0] + individual[7]

def tournament(population, fitness, status, size_tournament):
	parents = random.sample(population, size_tournament)
	fit, parents, st = sortedPopulation(fitness, parents, status)
	#Get two best parents for recombination
	return parents[0], parents[1]

def geneticAlgorithm(fitness, population, status):
	i = 0 #Counter to attempts

	while ((1 not in fitness) and i != _halt_):
		# shuffle(population, status, fitness)
		#Parent Selection
		parent1, parent2 = tournament(population, fitness, status, 5)

		#Recombining parents
		for x in xrange(_offspring_):
			offspring = recombination(parent1, parent2)
			mutation(offspring)
			fitness.append(calculateFitness(offspring))
			population.append(offspring)
			#Swap two lists
			parent1, parent2 = parent2, parent1

		#Remove two worst individuals
		survivalSelection(fitness, population, status)
		i = i+1

	if i == _halt_:
		print "Nao obteve sucesso"

if __name__ == '__main__':
	population = [] #Genotype
	status 	   = [] #Fenotype
	fitness    = [] #Fitness

	#Initialize randomly population
	for i in xrange(_population_): 		#Maximum number of population elements	
		individual =  random.sample(range(1,9), _dimension_)
		location   = []
		
		#Create location dataset
		while len(location) < _dimension_:
			location.append(random.sample(range(0,_dimension_), 2))

		if individual in population:
			random.shuffle(individual)

		#Calculate Fitness for all population elements
		fitness.append(calculateFitness(individual))
		population.append(individual)
		status.append(location)

	#Call genetic algorithm
	geneticAlgorithm(fitness, population, status)