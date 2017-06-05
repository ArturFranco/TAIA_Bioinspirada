import math
import random
import numpy as np
import scipy.stats

# --- Ackley Parameters ---
N = 30
C1 = 20
C2 = 0.2
C3 = 2*math.pi
nRecombination = 50 #numero de filhos gerados a partir de crossover
nMutation = 4 #numero de filhos gerados para cada filho gerado no crossover
typeMutation = 1 #1 para caso 1 e 2 para caso 2
typeRecombination = 2 #1 para ILP, else DLP

GlobalT = 1/math.sqrt(2*N)
LocalT = 1/math.sqrt(2*math.sqrt(N))
mutation1T = 1/math.sqrt(N)

bias = 0.0001 #valor minimo para o passo de mutacao
iterations = 10000
population_size = 30
#--- Gaussian distribution ------
mean = 0
std = 1
gaussian = scipy.stats.norm(mean,std)
# -------------------------

def gaussianPerturbation(mean, std):
    x = np.random.normal(mean,std)
    return gaussian.cdf(x)

def individualGeneration(N,typeMutation):
    vObject = []
    Sigma = []
    if (typeMutation == 1):
        normal = gaussianPerturbation(mean, std)
        for i in range(N):
            vObject.append(random.uniform(-15,15))
            Sigma.append(normal)
    elif (typeMutation == 2):
        for i in range(N):
            vObject.append(random.uniform(-15,15))
            Sigma.append(gaussianPerturbation(mean, std))
    return (vObject,Sigma)

def calculateFitness(individual):
    ret = ackleyFunction(individual, N, C1, C2, C3)
    return ret

def createPopulation(population_size, N):
    population = []
    fitness = []
    for i in range(population_size):
        individual = individualGeneration(N,typeMutation)
        population.append(individual)
        fit = calculateFitness(individual[0])
        fitness.append(fit)
    return population, fitness

def parentsSelection(population):
    parent1 = random.randint(0, len(population)-1)
    parent2 = random.randint(0, len(population)-1)
    while parent1 == parent2:
        parent2 = random.randint(0, len(population)-1)

    return population[parent1], population[parent2]

def ackleyFunction(array, N, C1, C2, C3):
    sum1 = 0.0
    sum2 = 0.0
    for i in range(N):
        sum1 += array[i]**2
        sum2 += math.cos(C3*array[i])
    return -C1*math.exp(-C2*math.sqrt((1.0/N)*sum1)) - math.exp((1.0/N)*sum2) + C1 + np.e

# Intermediary Local Point Recombination
def recombinationILP(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        ILP = (parent1[i]+parent2[i])/2.0
        child.append(round(ILP,5))
    return child

# Discrete Local Point Recombination
def recombinationDLP(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        prob = random.random()
        if prob < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

def mutation2(individual):
    vObject = individual[0]
    Sigma = individual[1]
    firstFactor = GlobalT * gaussianPerturbation(mean, std)
    for i in range(N):
        Sigma[i] = Sigma[i] * math.exp(firstFactor + LocalT * gaussianPerturbation(mean, std))
        if Sigma[i] < bias:
            Sigma[i] = bias
        vObject[i] = vObject[i] + Sigma[i] * gaussianPerturbation(mean, std)
    return (vObject,Sigma)

def mutation1(individual):
    vObject = individual[0]
    Sigma = individual[1]

    Sigma[0] = Sigma[0] * math.exp(mutation1T * gaussianPerturbation(mean, std))
    if Sigma[0] < bias:
        Sigma[0] = bias

    normal = gaussianPerturbation(mean, std)
    for i in range(N):
        Sigma[i] = Sigma[0]
        vObject[i] = vObject[i] + Sigma[i]*normal
    return (vObject,Sigma)

def survivalSelection(population):

    population.sort(key=lambda x: x[1])
    result = []
    fitness = []
    for i in range(population_size):
        result.append(population[i][0])
        fitness.append(population[i][1])
    return result,fitness

if __name__ == '__main__':

    #creating the population randomly
    population, fitness = createPopulation(population_size,N)
    #print ''
    #print fitness
    #print ''

    i = 1
    count = 0
    avgFitness = np.mean(fitness)

    bestElement = []
    bestFitness = []
    meanFitness = []
    stdFitness = []

    while (i <= iterations and count < 100):
        aux = []
        #print 'Generation' + str(i)
        fitness = []
        for cross in range(nRecombination):
            #parents selection
            parent1,parent2 = parentsSelection(population)
                #print parent1
                #print ''
                #print parent2
                #print ''
            #crossver
            if typeRecombination == 1:
                child = (recombinationILP(parent1[0],parent2[0]),recombinationDLP(parent1[1],parent2[1]))
            else:
                child = (recombinationDLP(parent1[0],parent2[0]),recombinationDLP(parent1[1],parent2[1]))
            #mutation
            for mut in range(nMutation):
                if typeMutation == 1:
                    mutation = mutation1(child)
                    fit = calculateFitness(mutation[0])
                    aux.append((mutation,fit))
                elif typeMutation == 2:
                    mutation = mutation2(child)
                    fit = calculateFitness(mutation[0])
                    aux.append((mutation,fit))
            #print aux[0]
            #print ''
        #print fitness

        #survival selection
        population, fitness = survivalSelection(aux)
            #print ''

        #saving important Data
        auxMean = np.mean(fitness)
        if (auxMean >= avgFitness):
            count += 1
        else:
            count = 0
        avgFitness = auxMean

        bestElement.append(population[0])
        meanFitness.append(avgFitness)
        bestFitness.append(fitness[0])
        stdFitness.append(np.std(fitness))
        print 'The Best Individual of generation: '+ str(i) + ' has fit: '+ str(fitness[0])
        i +=1

    #plots in meanFitness, bestFitness and stdFitness
    #pode usar o vetor bestElement para saber a configuracao do melhor individuo por geracao
