import csv
from distutils.log import debug
from operator import truediv
from time import sleep
from random import randrange
import copy
import logging

def getDexInfo(dexset, searchme):
    temp = 0
    for entry in dexset:
        if(entry[0].lower() == searchme.lower()):
            logging.debug(searchme + " found as: " + str(dexset[temp]))
            return dexset[temp]
        temp = temp+1

                
def compare(val1,val2):
    if(val1 > val2):
        return -1
    if(val1 < val2):
        return 1
    return 0

def genCheck(g):
    if int(target[1]) == int(g[1]): #gen match
        guessStat[0] = 0
    elif int(target[1]) <= int(g[1]): #high guess
        guessStat[0] = 1    
    elif int(target[1]) >= int(g[1]): #low guess
        guessStat[0] = -1

def typeCheck(g):
    if target[2] == g[2]: #type 1 match
        guessStat[1] = 0
    else: 
        if target[2] != g[2] and target[3] != g[2]: #type 1 fail
            guessStat[1] = 1
        else:
            guessStat[1] = -1 #type 1 switch

    if target[3] == g[3]: #type 2 match
        guessStat[2] = 0
    if target[3] != g[3]: #type 2 fail
        if target[2] == g[3]:#type 2 switch
            guessStat[2] = -1
        else: guessStat[2] = 1 #type 2 fail

def heightCheck(g):
    guessStat[3] = compare(float(target[4]), float(g[4]))

def weightCheck(g):
    guessStat[4] = compare(float(target[5]), float(g[5]))

def printOutcome(g):
    print(g[0]+"\t",end="")
    if guessStat[0] == 0:
        print("✓"+"\t",end="")
    elif guessStat[0] == -1:
        print("↑"+"\t",end="")
    else:
        print("↓"+"\t",end="")
        
    if guessStat[1] == 0:
        print("✓"+"\t",end="")
    elif guessStat[1] == 1:
        print("x"+"\t",end="")
    else:
        print("<>"+"\t",end="")

    if guessStat[2] == 0:
        print("✓ "+"\t",end="")
    elif guessStat[2] == 1:
        print("x"+"\t",end="")
    else:
        print("<>"+"\t",end="")

    if guessStat[3] == 0:
        print("✓"+"\t",end="")
    elif guessStat[3] == -1:
        print("↑"+"\t",end="")
    else:
        print("↓"+"\t",end="")

    if guessStat[4] == 0:
        print("✓"+"\t",end="")
    elif guessStat[4] == -1:
        print("↑"+"\t",end="")
    else:
        print("↓"+"\t",end="")

def pareDex(wd, g):
    oldSize = len(wd)
    for entry in wd:
        #check gen
        if guessStat[0] == 0:
            if int(g[1]) == int(entry[1]):
                pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a generation ruleout. {b} should equal {c} but is not".format(a = entry[0], b = g[1], c = entry[1]))
                    workingDex.remove(entry) 
                except ValueError: 
                    pass
                continue
        elif guessStat[0] == 1:
            if int(g[1]) > int(entry[1]):
                pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a generation ruleout. {b} should be greater than {c} but is not".format(a = entry[0], b = g[1], c = entry[1]))
                    workingDex.remove(entry) 
                except ValueError: 
                    pass
                continue
        elif guessStat[0] == -1:
            if int(g[1]) < int(entry[1]):
                pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a generation ruleout. {b} should be less than {c} but is not".format(a = entry[0], b = g[1], c = entry[1]))
                    workingDex.remove(entry) 
                except ValueError: 
                    pass
                continue

        #check height
        if guessStat[3] == 0:
            if float(g[4]) == float(entry[4]): pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a height ruleout. {b}({c}) should equal {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[4],d = entry[4]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[3] == 1:
            if float(g[4]) > float(entry[4]): pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a height ruleout. {b}({c}) should be greater than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[4],d = entry[4]))
                    workingDex.remove(entry)
                except ValueError: pass
                continue
        elif guessStat[3] == -1:
            if float(g[4]) < float(entry[4]): pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a height ruleout. {b}({c}) should be greater than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[4],d = entry[4]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue

        #check weight
        if guessStat[4] == 0:
            if float(g[5]) == float(entry[5]): pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a weight ruleout. {b}({c}) should be equal to {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[5],d = entry[5]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[4] == 1:
            if float(g[5]) > float(entry[5]): pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a weight ruleout. {b}({c}) should be greater than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[5],d = entry[5]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[4] == -1:
            if float(g[5]) < float(entry[5]): pass
            else: 
                try:
                    logging.debug("deleting entry for {a} for a weight ruleout. {b}({c}) should be less than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[5],d = entry[5]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue


        #check type1
        if guessStat[1] == -1:
            if g[2] == entry[3]: pass
            else: 
                try: 
                    logging.debug("deleting entry for {a} for a type1(switch) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[2],d = entry[3]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[1] == 0:
            if g[2] == entry[2]: pass
            else: 
                try: 
                    logging.debug("deleting entry for {a} for a type1(match) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[2],d = entry[2]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[1] == 1:
            if g[2] != entry[2]: pass
            else: 
                try: 
                    logging.debug("deleting entry for {a} for a type1(false) ruleout. {b}({c}) should be different from {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[2],d = entry[2]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        #check type2
        if guessStat[2] == -1:
            if g[3] == entry[2]: pass
            else: 
                try: 
                    logging.debug("deleting entry for {a} for a type2(switch) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[3],d = entry[2]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[2] == 0:
            if g[3] == entry[3]: pass
            else: 
                try: 
                    logging.debug("deleting entry for {a} for a type1(match) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[3],d = entry[3]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue
        elif guessStat[2] == 1:
            if g[3] != entry[3]: pass
            else: 
                try: 
                    logging.debug("deleting entry for {a} for a type1(false) ruleout. {b}({c}) should be different from{a}({d}) but is not".format(a = entry[0], b = g[0],c = g[3],d = entry[3]))
                    workingDex.remove(entry) 
                except ValueError: pass
                continue






    logging.info("old wd size: {a}\t new wd size: {b}\t elimation this round: {c}".format(a = str(oldSize), b = str(len(workingDex)),c = str(oldSize-len(workingDex))))
    print("\n" + str(oldSize) + "-" + str(len(workingDex)) + " = " + str(oldSize-len(workingDex)) + " eliminated!")

def lose():
    print("You failed to guess:")
    for item in target:
        print(item,end="\t")
        print()
    print("the remaining pool was:")
    for entry in workingDex:
        for item in entry:
            print(item,end="\t")
        print()

cont = 1
logging.basicConfig(filename= "debug.log", level=logging.DEBUG)
while(cont):
    with open('pokedex.csv') as dexFile:
        #initialization of the dex
        csv_reader = csv.reader(dexFile, delimiter=',')
        dex = list()
        #   name, gen, type1, type2, height, weight
        for row in dexFile:
            row = row.strip("\n")
            row = list(row.split(","))
            temp = list()
            for value in row:
                temp.append(value)
            dex.append(temp)
        guessStatModel = [0,0,0,0,0]
        guessStat = guessStatModel.copy()
        dex.remove(dex[0])
        workingDex = dex.copy()
        #target = dex[randrange(665)].copy()
        target = dex[27].copy()
        logging.info("{a} selected as target".format(a = target[0]))
        while True:
            try:
                guess1in = input("Make a lowercase guess: ")
                guess1 = getDexInfo(dex, guess1in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess1 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            break
        genCheck(guess1)
        typeCheck(guess1)
        heightCheck(guess1)
        weightCheck(guess1)
        
        printOutcome(guess1)
        
        pareDex(workingDex.copy(), guess1)
        while True:
            try:
                guess2in = input("Make a lowercase guess: ")
                guess2 = getDexInfo(dex, guess2in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess2 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            continue
        genCheck(guess2)
        typeCheck(guess2)
        heightCheck(guess2)
        weightCheck(guess2)
        
        printOutcome(guess2)
        pareDex(workingDex.copy(), guess2.copy())

        while True:
            try:
                guess3in = input("Make a lowercase guess: ")
                guess3 = getDexInfo(dex, guess3in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess3 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            continue
        genCheck(guess3)
        typeCheck(guess3)
        heightCheck(guess3)
        weightCheck(guess3)
        
        printOutcome(guess3)
        pareDex(workingDex.copy(), guess3.copy())
        while True:
            try:
                guess4in = input("Make a lowercase guess: ")
                guess4 = getDexInfo(dex, guess4in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess4 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            continue
        genCheck(guess4)
        typeCheck(guess4)
        heightCheck(guess4)
        weightCheck(guess4)
        
        printOutcome(guess4)
        pareDex(workingDex.copy(), guess4.copy())

        while True:
            try:      
                guess5in = input("Make a lowercase guess: ")
                guess5 = getDexInfo(dex, guess5in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess5 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            continue
        genCheck(guess5)
        typeCheck(guess5)
        heightCheck(guess5)
        weightCheck(guess5)
        
        printOutcome(guess5)
        pareDex(workingDex.copy(), guess5.copy())

        while True:
            try:
                guess6in = input("Make a lowercase guess: ")
                guess6 = getDexInfo(dex, guess6in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess6 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            continue
        genCheck(guess6)
        typeCheck(guess6)
        heightCheck(guess6)
        weightCheck(guess6)
        
        printOutcome(guess6)
        pareDex(workingDex.copy(), guess6.copy())



        while True:
            try:
                guess7in = input("Make a lowercase guess: ")
                guess7 = getDexInfo(dex, guess7in).copy()
            except AttributeError:
                print("check for typo")
                continue
            break
        if guess7 == target:
            print("YOU GOT IT!")
            cont = int(input("continue playing?: "))
            continue
        genCheck(guess7)
        typeCheck(guess7)
        heightCheck(guess7)
        weightCheck(guess7)
        
        printOutcome(guess7)
        pareDex(workingDex.copy(), guess7.copy())
        
        lose()
        cont = int(input("continue playing?: "))
        continue
        




        

