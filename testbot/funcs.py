from asyncio.windows_events import NULL
import copy
import csv
import logging
import random



def getDexInfo(dexset, searchme):
	temp = 0
	for entry in dexset:
		if(entry[0].lower() == searchme.lower()):
			logging.info(searchme + " found as: " + str(dexset[temp]))
			return dexset[temp]
		temp = temp+1
	return NULL

def pickTarget(fd):
	temp = fd[random.randrange(len(fd))].copy()
	logging.info("{a} selected as target".format(a = temp[0]))
	return temp


async def printGame(guessTracker,guessStat,guesses, message):
	outString = "Gen\tType 1\tType 2\tHeight\tWeight\tName"
	for num in range(guessTracker+1):
		lineSet = "\n"
		
		#check gen
		match guessStat[num][0]:
			case 0:
				lineSet= lineSet + "✅\t"
			case -1:
				lineSet= lineSet + "🔼\t"
			case 1:
				lineSet= lineSet + "🔽\t"
		match guessStat[num][1]:
			case 0:
				lineSet= lineSet + "✅\t"
			case -1:
				lineSet= lineSet + "➡️\t"
			case 1:
				lineSet= lineSet + "❌\t"
		match guessStat[num][2]:
			case 0:
				lineSet= lineSet + "✅\t"
			case -1:
				lineSet= lineSet + "⬅️\t"
			case 1:
				lineSet= lineSet + "❌\t"
		match guessStat[num][3]:
			case 0:
				lineSet= lineSet + "✅\t"
			case -1:
				lineSet= lineSet + "🔼\t"
			case 1:
				lineSet= lineSet + "🔽\t"
		match guessStat[num][4]:
			case 0:
				lineSet= lineSet + "✅\t"
			case -1:
				lineSet= lineSet + "🔼\t"
			case 1:
				lineSet= lineSet + "🔽\t"
		lineSet= lineSet + guesses[num][0]
		outString= outString + lineSet
	await message.channel.send(outString)

def compare(val1,val2):
    if(val1 > val2):
        return -1
    if(val1 < val2):
        return 1
    return 0

def genCheck(g, target, guessStat, guessTracker):
	if int(target[1]) == int(g[1]): #gen match
		guessStat[guessTracker][0] = 0
	elif int(target[1]) <= int(g[1]): #high guess
		guessStat[guessTracker][0] = 1    
	elif int(target[1]) >= int(g[1]): #low guess
		guessStat[guessTracker][0] = -1

def typeCheck(g, target, guessStat, guessTracker):
	if target[2] == g[2]: #type 1 match
		guessStat[guessTracker][1] = 0
	else: 
		if target[2] != g[2] and target[3] != g[2]: #type 1 fail
			guessStat[guessTracker][1] = 1
		else:
			guessStat[guessTracker][1] = -1 #type 1 switch

	if target[3] == g[3]: #type 2 match
		guessStat[guessTracker][2] = 0
	if target[3] != g[3]: #type 2 fail
		if target[2] == g[3]:#type 2 switch
			guessStat[guessTracker][2] = -1
		else: guessStat[guessTracker][2] = 1 #type 2 fail

def heightCheck(g, target, guessStat, guessTracker):
	guessStat[guessTracker][3] = compare(float(target[4]), float(g[4]))

def weightCheck(g, target, guessStat, guessTracker):
	guessStat[guessTracker][4] = compare(float(target[5]), float(g[5]))

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