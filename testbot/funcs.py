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
	outString = "Gen\tType 1\tType 2\tHeight\tWeight\tName\teliminated"
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
		lineSet= lineSet + guesses[num][0] + str(guessStat[num][5])
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

def cutDex(g, wd, guessStat, guessTracker, workingDex):
	oldSize = len(wd)
	for entry in wd:
		#check gen
		if guessStat[guessTracker][0] == 0:
			if int(g[1]) == int(entry[1]):
				pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a generation ruleout. {b} should equal {c} but is not".format(a = entry[0], b = g[1], c = entry[1]))
					workingDex.remove(entry) 
				except ValueError: 
					pass
				continue
		elif guessStat[guessTracker][0] == 1:
			if int(g[1]) > int(entry[1]):
				pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a generation ruleout. {b} should be greater than {c} but is not".format(a = entry[0], b = g[1], c = entry[1]))
					workingDex.remove(entry) 
				except ValueError: 
					pass
				continue
		elif guessStat[guessTracker][0] == -1:
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
		if guessStat[guessTracker][3] == 0:
			if float(g[4]) == float(entry[4]): pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a height ruleout. {b}({c}) should equal {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[4],d = entry[4]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][3] == 1:
			if float(g[4]) > float(entry[4]): pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a height ruleout. {b}({c}) should be greater than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[4],d = entry[4]))
					workingDex.remove(entry)
				except ValueError: pass
				continue
		elif guessStat[guessTracker][3] == -1:
			if float(g[4]) < float(entry[4]): pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a height ruleout. {b}({c}) should be greater than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[4],d = entry[4]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue

		#check weight
		if guessStat[guessTracker][4] == 0:
			if float(g[5]) == float(entry[5]): pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a weight ruleout. {b}({c}) should be equal to {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[5],d = entry[5]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][4] == 1:
			if float(g[5]) > float(entry[5]): pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a weight ruleout. {b}({c}) should be greater than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[5],d = entry[5]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][4] == -1:
			if float(g[5]) < float(entry[5]): pass
			else: 
				try:
					logging.debug("deleting entry for {a} for a weight ruleout. {b}({c}) should be less than {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[5],d = entry[5]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue


		#check type1
		if guessStat[guessTracker][1] == -1:
			if g[2] == entry[3]: pass
			else: 
				try: 
					logging.debug("deleting entry for {a} for a type1(switch) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[2],d = entry[3]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][1] == 0:
			if g[2] == entry[2]: pass
			else: 
				try: 
					logging.debug("deleting entry for {a} for a type1(match) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[2],d = entry[2]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][1] == 1:
			if g[2] != entry[2]: pass
			else: 
				try: 
					logging.debug("deleting entry for {a} for a type1(false) ruleout. {b}({c}) should be different from {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[2],d = entry[2]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue

		#check type2
		if guessStat[guessTracker][2] == -1:
			if g[3] == entry[2]: pass
			else: 
				try: 
					logging.debug("deleting entry for {a} for a type2(switch) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[3],d = entry[2]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][2] == 0:
			if g[3] == entry[3]: pass
			else: 
				try: 
					logging.debug("deleting entry for {a} for a type1(match) ruleout. {b}({c}) should be the same as {a}({d}) but is not".format(a = entry[0], b = g[0],c = g[3],d = entry[3]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue
		elif guessStat[guessTracker][2] == 1:
			if g[3] != entry[3]: pass
			else: 
				try: 
					logging.debug("deleting entry for {a} for a type1(false) ruleout. {b}({c}) should be different from{a}({d}) but is not".format(a = entry[0], b = g[0],c = g[3],d = entry[3]))
					workingDex.remove(entry) 
				except ValueError: pass
				continue






	logging.info("old wd size: {a}\t new wd size: {b}\t elimation this round: {c}".format(a = str(oldSize), b = str(len(workingDex)),c = str(oldSize-len(workingDex))))
	print("\n" + str(oldSize) + "-" + str(len(workingDex)) + " = " + str(oldSize-len(workingDex)) + " eliminated!")
	guessStat[guessTracker][5] = oldSize-len(workingDex)