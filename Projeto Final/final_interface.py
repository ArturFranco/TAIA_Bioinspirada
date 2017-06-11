from Tkinter import *
import os, sys
import numpy as np
import pandas as pd
import random
import time
import math

# ------------- Parameters GUI ------------- #
creds       = 'tempfile.temp' # This just sets the variable creds to 'tempfile.temp'
font        = ("Helvetica", 10)
bd          = 3

refeicaoIN  = []
fProt, fCarb, fLip, fFib = 0, 0, 0, 0
# --------------------------------------------
_mesuare = 5.0
_populationSize = 50
_haltCondition = 10
_qtdBits = 6
_error = 0.05
_pRecombination = 0.6
_pMutation = 0.4
_nRecombination = (_populationSize * 7.0)/2.0
_strategy = 1 #if 1 -> AG else -> EE
# --------------------------------------------

alimentos = pd.read_csv('alimentos.csv', sep=';')
del alimentos['Unnamed: 0']

aux = pd.DataFrame()
aux['alimento'] = alimentos['alimento']
aux['proteina'] = alimentos['proteina'].apply(lambda x: x*4)
aux['lipideos'] = alimentos['lipideos'].apply(lambda x: x*9)
aux['carboidrato'] = alimentos['carboidrato'].apply(lambda x: x*4)
aux['fibras'] = alimentos['fibras'].apply(lambda x: x*4)

############################## Graphical User Interface ####################################### 
def Signup(): # This is the signup definition, 
    global pwordE, nameE, credE
    global roots
 
    roots = Tk() # This creates the window, just a blank one.
    roots.title('Login') # This renames the title of said window to 'signup'
    roots.geometry('320x180')

    instruction = Label(roots, text='Please Enter Nutricional Credentials\n') # This puts a label, so just a piece of text saying 'please enter blah'
    instruction.grid(row = 0, column = 0, sticky = E) # This just puts it in the window, on row 0, col 0. If you want to learn more look up a tkinter tutorial :)
 
    nameL  = Label(roots, text = 'Username: ', font = font) # This just does the same as above, instead with the text new username.
    pwordL = Label(roots, text = 'Password: ', font = font) # ^^
    credL  = Label(roots, text = 'Credential: ', font = font)
    nameL.grid(row = 1, sticky = W) # Same thing as the instruction var just on different rows. :) Tkinter is like that.
    pwordL.grid(row = 2, sticky = W) # ^^
    credL.grid(row = 3, sticky = W)
 
    nameE = Entry(roots, bd = bd) # This now puts a text box waiting for input.
    pwordE = Entry(roots, show = '*', bd = bd) # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    credE  = Entry(roots, bd = bd)
    nameE.grid(row = 1, column  = 0, sticky = E) # You know what this does now :D
    pwordE.grid(row = 2, column = 0, sticky = E) # ^^
    credE.grid(row = 3, column  = 0, sticky = E)
 
    signupButton = Button(roots, text = 'Signup', command = FSSignup) # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
    signupButton.grid(row = 2, column = 2, columnspan = 2, rowspan = 1, sticky = W+E+N+S, padx = 30)
    roots.mainloop() # This just makes the window keep open, we will destroy it soon
 
def FSSignup():
    with open(creds, 'w') as f: # Creates a document using the variable we made at the top.
        f.write(nameE.get()) # nameE is the variable we were storing the input to. Tkinter makes us use .get() to get the actual string.
        f.write('\n') # Splits the line so both variables are on different lines.
        f.write(pwordE.get()) # Same as nameE just with pword var
        f.write('\n')
        f.write(credE.get())
        f.close() # Closes the file
 
    roots.destroy() # This will destroy the signup window. :)
    Login() # This will move us onto the login definition :D
 
def Login():
    global nameEL, pwordEL, credEL
    global rootA
 
    rootA = Tk() # This now makes a new window.
    rootA.title('Login') # This makes the window title 'login'
    rootA.geometry('320x180')
 
    instruction = Label(rootA, text = 'Please Login\n') # More labels to tell us what they do
    instruction.grid(sticky = E) # Blahdy Blah
 
    nameL  = Label(rootA, text='Username: ', font = font) # More labels
    pwordL = Label(rootA, text='Password: ', font = font) # ^
    credL  = Label(rootA, text='Credential: ', font = font)
    nameL.grid(row = 1, sticky = W)
    pwordL.grid(row = 2, sticky = W)
    credL.grid(row = 3, sticky = W)

    nameEL = Entry(rootA, bd = bd) # The entry input
    pwordEL = Entry(rootA, show='*', bd = bd)
    credEL = Entry(rootA, bd = bd)
    nameEL.grid(row = 1, column = 1)
    pwordEL.grid(row = 2, column = 1)
    credEL.grid(row = 3, column = 1)
  
    loginB = Button(rootA, text = 'Login', command = CheckLogin) # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(row = 2, column = 2, columnspan = 2, rowspan = 1, sticky = W+E+N+S, padx = 30)
 
    rmuser = Button(rootA, text = 'Delete User', fg = 'red', command = DelUser) # This makes the deluser button. blah go to the deluser def.
    rmuser.grid(row = 3, column = 2, columnspan = 2, rowspan = 1, sticky = W+E+N+S, padx = 30)
    rootA.mainloop()

def InputData():
    global rootNutri
    global kcalEL, rateProtEL, rateCarbEL, rateLipEL, rateFibEL

    rootNutri = Tk()
    rootNutri.title('Nutricional Inputs')
    rootNutri.geometry('320x120')

    kcalL       = Label(rootNutri, text = 'Kcal: ', font = font)
    rateProtL   = Label(rootNutri, text = 'Rate Prot: ', font = font)
    rateCarbL   = Label(rootNutri, text = 'Rate Carb: ', font = font)
    rateLipL    = Label(rootNutri, text = 'Rate Lip: ', font = font)
    rateFibL    = Label(rootNutri, text = 'Rate Fib: ', font = font)

    kcalL.grid(row = 1, sticky = W)
    rateProtL.grid(row = 2, sticky = W)
    rateCarbL.grid(row = 3, sticky = W)
    rateLipL.grid(row = 4, sticky = W)
    rateFibL.grid(row = 5, sticky = W)

    kcalEL = Entry(rootNutri, bd = bd) # The entry input
    rateProtEL = Entry(rootNutri, bd = bd)
    rateCarbEL = Entry(rootNutri, bd = bd)
    rateLipEL = Entry(rootNutri, bd = bd) # The entry input
    rateFibEL = Entry(rootNutri, bd = bd)
    kcalEL.grid(row = 1, column = 1)
    rateProtEL.grid(row = 2, column = 1)
    rateCarbEL.grid(row = 3, column = 1)
    rateLipEL.grid(row = 4, column = 1)
    rateFibEL.grid(row = 5, column = 1)
  
    getInput = Button(rootNutri, text = 'Get', command = SelectMeal) # This makes the login button, which will go to the CheckLogin def.
    getInput.grid(row = 3, column = 3, columnspan = 2, sticky = W, padx = 25)

    rootNutri.mainloop()
 
def CheckLogin():
    with open(creds) as f:
        data = f.readlines() # This takes the entire document we put the info into and puts it into the data variable
        uname = data[0].rstrip() # Data[0], 0 is the first line, 1 is the second and so on.
        pword = data[1].rstrip() # Using .rstrip() will remove the \n (new line) word from before when we input it
        cred  = data[2].rstrip()
        
        input_name = nameEL.get()
        input_pass = pwordEL.get()
        input_cred = credEL.get()
        rootA.destroy()

    if (input_name == uname) and (input_pass == pword) and (input_cred == cred): # Checks to see if you entered the correct data.
        InputData()
    else:
        Login()
 
def DelUser():
    os.remove(creds) # Removes the file
    rootA.destroy() # Destroys the login window
    Signup() # And goes back to the start!

def Testcheck():
    global selection, entries
    global rootMes
    selection = []

    for index, b in enumerate(bool_chk):
      if b.get(): selection.append(index)

    rootMeal.destroy()

    rootMes = Tk()
    rootMes.title("Get Measures")

    entries = []
    index   = 0
    i, j    = 0, 0

    for i in selection:
        label = Label(rootMes, text = "Minimum for " + aux['alimento'][i], font = font)
        label.grid(row = i, column = j, sticky = W)
        entries.append(Entry(rootMes, bd = bd))
        entries[index].grid(row = i, column = j+1)
        index += 1
 
    getInput = Button(rootMes, text = 'Ok', command = calcRegimen) # This makes the login button, which will go to the CheckLogin def.
    getInput.grid(column = j+1, columnspan = 2, sticky = E, padx = 50)

    rootMes.mainloop()

def calcRegimen():
    global refeicaoIN
    global fProt, fCarb, fLip, fFib

    fProt = (Kcal*rateProt)
    fCarb = (Kcal*rateCarb)
    fLip = (Kcal*rateLip)
    fFib = (Kcal*rateFib)

    refeicaoIN = []
    index = 0
    for i in selection:
        refeicaoIN.append((aux['alimento'][i], float(entries[index].get())))

    rootMes.destroy()

    result = evolutiveAlgorithm()

    rootRes = Tk()
    rootRes.title("Final Result: ")

    i = 0
    for food in result:
        instruction = Label(rootRes, text = refeicaoIN[i][0] + "  - " + str(food) + 'g', font = ('Helvetica', 10)) # More labels to tell us what they do
        instruction.grid(sticky = W)
        i += 1

def SelectMeal():
    global rootMeal
    global Kcal, rateProt, rateFib, rateCarb, rateLip
    global bool_chk

    Kcal        = float(kcalEL.get())
    rateProt    = float(rateProtEL.get())
    rateFib     = float(rateFibEL.get())
    rateCarb    = float(rateCarbEL.get())
    rateLip     = float(rateLipEL.get())

    rootNutri.destroy()

    bool_chk    = []
    chkbuttons  = []
    index       = 0

    rootMeal = Tk()
    rootMeal.title('Select Meal')

    sb      = Scrollbar(orient = "vertical")
    text    = Text(rootMeal, width = 40, height = 20, yscrollcommand = sb.set)
    sb.config(command = text.yview)
    sb.pack(side = "right", fill = "y")
    text.pack(side = "top", fill = "both", expand = True)

    for i in aux['alimento']:
      bool_chk.append(BooleanVar())
      chkbuttons.append(Checkbutton(text = i, variable = bool_chk[index]))
      index += 1

    for cb in chkbuttons:
        text.window_create("end", window = cb)
        text.insert("end", "\n")

    testbutton = Button(rootMeal, text = 'Confirm', command = Testcheck)
    testbutton.pack()

    rootMeal.mainloop()
################################## BACKEND #####################################

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

#    ok
def createPopulation(populationSize, refeicaoIN):
    population = []
    maxArray = []

    for food in refeicaoIN:
        maxArray.append(foodMaxAmount(food[0]))

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
        # print aux
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
    maxArray = []
    for food in refeicaoIN:
        maxArray.append(foodMaxAmount(food[0]))

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
            if(random.randint(0,100) < _pRecombination * 100):
                child1, child2 = coinRecombination(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

                # Mutation
            if(random.randint(0,100) < _pMutation * 100):
                child1 = mutation2(child1)
                child2 = mutation2(child2)
            else:
                child1, child2 = parent1, parent2

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

    #print fitness[nearestN(fitness)[0][0]]
    better = nearestN(fitness)[0]

    return population[better[0]]

if __name__ == '__main__':
    if os.path.isfile(creds):
        Login()
    else: # This if else statement checks to see if the file exists. If it does it will go to Login, if not it will go to Signup :)
        Signup()

    if creds in locals() or creds in globals():
        os.remove(creds)