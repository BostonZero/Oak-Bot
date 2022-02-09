import csv
from distutils.log import debug
from operator import truediv
from time import sleep
from random import randrange
import copy
import logging
import main




def compare(val1,val2):
    if(val1 > val2):
        return -1
    if(val1 < val2):
        return 1
    return 0

def genCheck(g):
    if int(main.target[1]) == int(g[1]): #gen match
        main.guessStat[main.guessTracker][0] = 0
    elif int(main.target[1]) <= int(g[1]): #high guess
        main.guessStat[main.guessTracker][0] = 1    
    elif int(main.target[1]) >= int(g[1]): #low guess
        main.guessStat[main.guessTracker][0] = -1

def typeCheck(g):
    if main.target[2] == g[2]: #type 1 match
        main.guessStat[main.guessTracker][1] = 0
    else: 
        if main.target[2] != g[2] and main.target[3] != g[2]: #type 1 fail
            main.guessStat[main.guessTracker][1] = 1
        else:
            main.guessStat[main.guessTracker][1] = -1 #type 1 switch

    if main.target[3] == g[3]: #type 2 match
        main.guessStat[main.guessTracker][2] = 0
    if main.target[3] != g[3]: #type 2 fail
        if main.target[2] == g[3]:#type 2 switch
            main.guessStat[main.guessTracker][2] = -1
        else: main.guessStat[main.guessTracker][2] = 1 #type 2 fail

def heightCheck(g):
    main.guessStat[main.guessTracker][3] = compare(float(main.target[4]), float(g[4]))

def weightCheck(g):
    main.guessStat[main.guessTracker][4] = compare(float(main.target[5]), float(g[5]))
