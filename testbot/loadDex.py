import csv
import copy


##dex loader
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
