import numpy as np
import pandas as pd
# Python 3+
import Tkinter as tk
# Python 2.7
#import Tkinter as tk
import random
import time
import math
from functools import partial

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

# Show the result on the screen
def resultFunction(obj, bt):
    global _result
    _result = evolutionaryAlgorithm()
    
    bt.pack_forget()
    
    i = 0
    for food in _result:
        labelResult = tk.Label(obj, text=_refeicaoIN[i][0]+' - '+str(int(food))+'g')
        labelResult.pack(side="top", fill="both", expand=True)
        labelResult.configure(background='spring green')
        labelResult.configure(font=('Verdana', 16))
        i += 1

# Class related to the Program Interface
class NutriFilsApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("NutriFilsApp")
        self.geometry("600x400+200+200")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (ScreenOne, ScreenTwo, ScreenThree, ScreenFour):
            page_name = page.__name__
            frame = page(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # starts on first screen
        self.show_frame("ScreenOne")

    # function to change the page
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Class related to the first screen of the program
class ScreenOne(tk.Frame):

    # getting values of the entries and storing in global variables
    # changing to second screen
    def gettingValues(self, controller):
        global _Kcal, _rateProt, _rateCarb, _rateLip, _rateFib, _fProt, _fCarb, _fLip, _fFib
        
        _Kcal = int(self.inputKcal.get())
        _rateProt = float(self.inputRateProt.get())
        _rateCarb = float(self.inputRateCarb.get())
        _rateLip = float(self.inputRateLip.get())
        _rateFib = float(self.inputRateFib.get())

        _fProt = _Kcal*_rateProt 
        _fCarb = _Kcal*_rateCarb
        _fLip = _Kcal*_rateLip
        _fFib = _Kcal*_rateFib
        
        controller.show_frame("ScreenTwo")
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='spring green')
        
        topEdge = tk.Label(self)
        topEdge.pack(side='top', fill='x')
        topEdge.configure(background='spring green')
        bottomEdge = tk.Label(self, height=2)
        bottomEdge.pack(side='bottom', fill='x')
        bottomEdge.configure(background='spring green')
        rightEdge = tk.Label(self, width=15)
        rightEdge.pack(side='right', fill='y')
        rightEdge.configure(background='spring green')
        leftEdge = tk.Label(self, width=15)
        leftEdge.pack(side='left', fill='y')
        leftEdge.configure(background='spring green')

        labelText = tk.Label(self, text='Nutritionist Inputs')
        labelText.pack(side='top', fill='both', expand=True)
        labelText.configure(background='spring green')
        labelText.configure(font=("Verdana", 16))

        labelKcal = tk.Label(self, text='kcal Amount')
        labelKcal.pack(side='top', fill='both', expand=True)
        labelKcal.configure(background='spring green')
        self.inputKcal = tk.Entry(self, justify='center')
        self.inputKcal.pack(side='top', fill='both', expand=True)

        labelRateProt = tk.Label(self, text='Protein Ratio')
        labelRateProt.pack(side='top', fill='both', expand=True)
        labelRateProt.configure(background='spring green')
        self.inputRateProt = tk.Entry(self, justify='center')
        self.inputRateProt.pack(side='top', fill='both', expand=True)

        labelRateCarb = tk.Label(self, text='Carbohydrate Ratio')
        labelRateCarb.pack(side='top', fill='both', expand=True)
        labelRateCarb.configure(background='spring green')
        self.inputRateCarb = tk.Entry(self, justify='center')
        self.inputRateCarb.pack(side='top', fill='both', expand=True)

        labelRateLip = tk.Label(self, text='Lipid Ratio')
        labelRateLip.pack(side='top', fill='both', expand=True)
        labelRateLip.configure(background='spring green')
        self.inputRateLip = tk.Entry(self, justify='center')
        self.inputRateLip.pack(side='top', fill='both', expand=True)

        labelRateFib = tk.Label(self, text='Fiber Ratio')
        labelRateFib.pack(side='top', fill='both', expand=True)
        labelRateFib.configure(background='spring green')
        self.inputRateFib = tk.Entry(self, justify='center')
        self.inputRateFib.pack(side='top', fill='both', expand=True)

        space = tk.Label(self)
        space.pack(side='top', fill='both', expand=True)
        space.configure(background='spring green')

        buttonNext = tk.Button(self, width=20, text='Next')
        buttonNext['command'] = partial(self.gettingValues, controller)
        buttonNext.pack()
        buttonNext.configure(background='DarkSeaGreen1')

# Class related to the second screen of the program
class ScreenTwo(tk.Frame):
    # getting values of the entries and storing in global variables
    # changing to third screen
    def calcRegimen(self):
        global _refeicaoIN, _foodMaxArray

        for entryFood, entryQtd in zip(self.selection, self.entriesQtd):
            _refeicaoIN.append((aux['alimento'][entryFood], int(entryQtd.get())))
        
        self.controller.show_frame("ScreenThree")

    def gettingValues(self, controller):
        self.selection = []

        self.buttonConfirm.destroy()
        self.sbFrame.destroy()
        self.textFrame.destroy()

        for index, b in enumerate(self.entriesFood):
          if b.get():
            self.selection.append(index)

        entries = []
        index   = 0
        i, j    = 0, 0

        for i in self.selection:
            label = tk.Label(self, text = "Min Amount of Food " + aux['alimento'][i])
            label.pack(side='top', fill='both', expand=True)
            label.configure(background='spring green')
            self.entriesQtd.append(tk.Entry(self, justify='center'))
            self.entriesQtd[index].pack(side = 'top', fill='both', expand = True)
            index += 1
     
        getInput = tk.Button(self, width = 20, text = 'Ok', command = self.calcRegimen) # This makes the login button, which will go to the CheckLogin def.
        getInput.pack(side = 'bottom')
        getInput.configure(background = 'DarkSeaGreen1')

    def selectFood(self):
        chkbuttons  = []
        index       = 0

        self.buttonSelect.destroy()
        self.buttonConfirm = tk.Button(self, width = 20, text = 'Confirm')
        self.buttonConfirm['command'] = partial(self.gettingValues, self.controller)
        self.buttonConfirm.pack(side = 'bottom')
        self.buttonConfirm.configure(background = 'DarkSeaGreen1')

        self.sbFrame      = tk.Scrollbar(self, orient = "vertical")
        self.textFrame    = tk.Text(self, width = 15, height = 15, yscrollcommand = self.sbFrame.set)
        self.sbFrame.config(command = self.textFrame.yview)
        self.sbFrame.pack(side = "right", fill = "both", expand = False)
        self.textFrame.pack(side = "left", fill = "both", expand = True)

        for i in aux['alimento']:
            self.entriesFood.append(tk.BooleanVar())
            chkbuttons.append(tk.Checkbutton(self, text = i, variable = self.entriesFood[index], font = ('Helvetica', 8)))
            index += 1

        for cb in chkbuttons:
            self.textFrame.window_create("end", window = cb)
            self.textFrame.insert("end", "\n")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = 'spring green')
        
        self.entriesFood = []
        self.entriesQtd = []
        
        topEdge = tk.Label(self)
        topEdge.pack(side='top', fill='x')
        topEdge.configure(background='spring green')
        bottomEdge = tk.Label(self, height=2)
        bottomEdge.pack(side='bottom', fill='x')
        bottomEdge.configure(background='spring green')
        rightEdge = tk.Label(self, width=5)
        rightEdge.pack(side='right', fill='y')
        rightEdge.configure(background='spring green')
        leftEdge = tk.Label(self, width=5)
        leftEdge.pack(side='left', fill='y')
        leftEdge.configure(background='spring green')

        labelText = tk.Label(self, text='Nutritionist Inputs')
        labelText.pack(side='top', fill='both', expand=True)
        labelText.configure(background='spring green')
        labelText.configure(font=("Verdana", 16))

        self.buttonSelect = tk.Button(self, width = 20, text = 'Next', command = self.selectFood)
        self.buttonSelect.pack(side = 'bottom')
        self.buttonSelect.configure(background = 'DarkSeaGreen1')
    
# Class related to the third screen of the program
class ScreenThree(tk.Frame):
    
    # getting values of the entries and storing in global variables
    # changing to fourth screen
    def gettingValues(self, controller):
        global _strategy, _multiple, _populationSize, _haltCondition, _error, _refeicaoIN
        global _pRecombination, _pMutation, _nRecombination, _result, _foodMaxArray
        
        _strategy = self.inputStrategy.get()
        _populationSize = int(self.inputPopuSize.get())
        _pRecombination = float(self.inputProbCross.get())
        _pMutation = float(self.inputProbMut.get())
        _haltCondition = int(self.inputHaltCond.get())
        _multiple = float(self.inputMultiple.get())
        _error = float(self.inputError.get())
        
        for food in _refeicaoIN:
            _foodMaxArray.append(foodMaxAmount(food[0]))

        if(_strategy == 'EE'):
            _nRecombination = (_populationSize*7.0)/2.0
        
        controller.show_frame("ScreenFour")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='spring green')
        
        topEdge = tk.Label(self)
        topEdge.pack(side='top', fill='x')
        topEdge.configure(background='spring green')
        bottomEdge = tk.Label(self, height=1)
        bottomEdge.pack(side='bottom', fill='x')
        bottomEdge.configure(background='spring green')
        rightEdge = tk.Label(self, width=15)
        rightEdge.pack(side='right', fill='y')
        rightEdge.configure(background='spring green')
        leftEdge = tk.Label(self, width=15)
        leftEdge.pack(side='left', fill='y')
        leftEdge.configure(background='spring green')

        labelText = tk.Label(self, text='Algorithm Parameters')
        labelText.pack(side='top', fill='both', expand=True)
        labelText.configure(background='spring green')
        labelText.configure(font=("Verdana", 16))

        labelStrategy = tk.Label(self, text='Solution Algorithm (AG or EE)')
        labelStrategy.pack(side='top', fill='both', expand=True)
        labelStrategy.configure(background='spring green')
        self.inputStrategy = tk.Entry(self, justify='center')
        self.inputStrategy.pack(side='top', fill='both', expand=True)

        labelPopuSize = tk.Label(self, text='Population Size')
        labelPopuSize.pack(side='top', fill='both', expand=True)
        labelPopuSize.configure(background='spring green')
        self.inputPopuSize = tk.Entry(self, justify='center')
        self.inputPopuSize.pack(side='top', fill='both', expand=True)

        labelProbCross = tk.Label(self, text='Crossover Probability (1 for EE)')
        labelProbCross.pack(side='top', fill='both', expand=True)
        labelProbCross.configure(background='spring green')
        self.inputProbCross = tk.Entry(self, justify='center')
        self.inputProbCross.pack(side='top', fill='both', expand=True)

        labelProbMut = tk.Label(self, text='Mutation Probability (1 for EE)')
        labelProbMut.pack(side='top', fill='both', expand=True)
        labelProbMut.configure(background='spring green')
        self.inputProbMut = tk.Entry(self, justify='center')
        self.inputProbMut.pack(side='top', fill='both', expand=True)

        labelHaltCond = tk.Label(self, text='Halt Condition')
        labelHaltCond.pack(side='top', fill='both', expand=True)
        labelHaltCond.configure(background='spring green')
        self.inputHaltCond = tk.Entry(self, justify='center')
        self.inputHaltCond.pack(side='top', fill='both', expand=True)

        labelMultiple = tk.Label(self, text='Multiple of Quantity (in grams)')
        labelMultiple.pack(side='top', fill='both', expand=True)
        labelMultiple.configure(background='spring green')
        self.inputMultiple = tk.Entry(self, justify='center')
        self.inputMultiple.pack(side='top', fill='both', expand=True)

        labelError = tk.Label(self, text='Error')
        labelError.pack(side='top', fill='both', expand=True)
        labelError.configure(background='spring green')
        self.inputError = tk.Entry(self, justify='center')
        self.inputError.pack(side='top', fill='both', expand=True)

        space = tk.Label(self, width = 20)
        space.pack(side='top', fill='both', expand=True)
        space.configure(background='spring green')

        buttonSend = tk.Button(self, height = 30, width = 20, text='Send', font = ('Helvetica', 8))
        buttonSend['command'] = partial(self.gettingValues, controller)
        buttonSend.pack()
        buttonSend.configure(background='DarkSeaGreen1')
    
# Class related to the fourth screen of the program
class ScreenFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.configure(background='spring green')
        
        topEdge = tk.Label(self)
        topEdge.pack(side='top', fill='x')
        topEdge.configure(background='spring green')
        bottomEdge = tk.Label(self, height=2)
        bottomEdge.pack(side='bottom', fill='x')
        bottomEdge.configure(background='spring green')
        rightEdge = tk.Label(self, width=5)
        rightEdge.pack(side='right', fill='y')
        rightEdge.configure(background='spring green')
        leftEdge = tk.Label(self, width=5)
        leftEdge.pack(side='left', fill='y')
        leftEdge.configure(background='spring green')

        buttonRun = tk.Button(self, width=50, height=5, text='Run Evolutionary Algorithm')
        buttonRun['command'] = partial(resultFunction, self, buttonRun)
        buttonRun.place(relx=0.5, rely=0.5, anchor='center')
        buttonRun.configure(background='DarkSeaGreen1')

if __name__ == "__main__":

    _count = 0
    _result = []
    
    _Kcal = 0
    _rateProt = 0
    _rateCarb = 0
    _rateLip = 0
    _rateFib = 0
    
    _fProt = 0
    _fCarb = 0
    _fLip = 0
    _fFib = 0

    _refeicaoIN = []
    _foodMaxArray = []

    _multiple = 0
    _populationSize = 0
    _haltCondition = 0
    _error = 0
    _pRecombination = 0
    _pMutation = 0
    _strategy = ''

    _nRecombination = 0

    global aux
    
    alimentos = pd.read_csv('alimentos.csv', sep=';')
    del alimentos['Unnamed: 0']

    aux = pd.DataFrame()
    aux['alimento'] = alimentos['alimento']
    aux['proteina'] = alimentos['proteina'].apply(lambda x: x*4)
    aux['lipideos'] = alimentos['lipideos'].apply(lambda x: x*9)
    aux['carboidrato'] = alimentos['carboidrato'].apply(lambda x: x*4)
    aux['fibras'] = alimentos['fibras'].apply(lambda x: x*4)
    
    app = NutriFilsApp()
    app.mainloop()