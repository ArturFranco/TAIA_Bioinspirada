import random

# Intermediary Local Point Recombination
def recombinationILP(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        ILP = (parent1[i]+parent2[i])/2
        child.append(round(ILP,2))
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