import math
import random

# --- Ackley Parameters ---
N = 30
C1 = 20
C2 = 0.2
C3 = 2*math.pi
# -------------------------

def individualGeneration():
    individual = []
    for i in range(N):
        individual.append(round(random.uniform(-15.0, 15.0), 2))
    
    return individual

def calculateFitness(individual):
    return round(ackleyFunction(individual, N, C1, C2, C3), 3)

def createPopulation(population_size):
    population = []
    fitness = []
    for i in range(population_size):
        individual = individualGeneration()
        population.append(individual)
        fitness.append(calculateFitness(individual))
    
    return population, fitness

def ackleyFunction(array, N, C1, C2, C3):
    sum1 = 0
    sum2 = 0
    for i in range(N):
        sum1 += array[i]**2   
        sum2 += math.cos(C3*array[i])
    
    return -C1*math.exp(-C2*math.sqrt((1/N)*sum1)) - math.exp((1/N)*sum2) + C1 + 1


population_size = 5
population, fitness = createPopulation(population_size)
print(fitness)