import copy
import csv
import logging
from distutils.log import debug
from operator import truediv
from random import randrange
from time import sleep

import main


def getDexInfo(dexset, searchme):
    temp = 0
    for entry in dexset:
        if(entry[0].lower() == searchme.lower()):
            logging.info(searchme + " found as: " + str(dexset[temp]))
            return dexset[temp]
        temp = temp+1

def pickTarget():
	temp = main.fullDex[randrange(len(main.fullDex))].copy()
	logging.info("{a} selected as target".format(a = temp[0]))
	return temp

def loadDex():
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
        dex.remove(dex[0])
    return dex.copy()
