from Tkinter import *
import os, sys
import numpy as np
import pandas as pd

creds = 'tempfile.temp' # This just sets the variable creds to 'tempfile.temp'

font        = ("Helvetica", 10)
bd          = 3
def Signup(): # This is the signup definition, 
    global pwordE # These globals just make the variables global to the entire script, meaning any definition can use them
    global nameE
    global credE
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
    global nameEL
    global pwordEL # More globals :D
    global credEL
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
    global Kcal
    global rateProt
    global rateCarb
    global rateLip
    global rateFib
    global rootNutri

    rootNutri = Tk()
    rootNutri.title('Nutricional Inputs')
    rootNutri.geometry('320x240')

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
    getInput.grid(column = 2, columnspan = 2, sticky = W)

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
    global selection
    selection = []

    for index, b in enumerate(bool_chk):
      if b.get(): selection.append(index)

    print selection

def SelectMeal():
    global rootMeal
    global bool_chk

    rootNutri.destroy()

    alimentos = pd.read_csv('alimentos.csv', sep=';')
    del alimentos['Unnamed: 0']
    aux = pd.DataFrame()
    aux['alimento'] = alimentos['alimento']

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

if __name__ == '__main__':
    if os.path.isfile(creds):
        Login()
    else: # This if else statement checks to see if the file exists. If it does it will go to Login, if not it will go to Signup :)
        Signup()
        
    if creds in locals() or creds in globals():
        os.remove(creds)