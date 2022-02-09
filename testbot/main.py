import copy
import csv
import logging
import os
from asyncio.windows_events import NULL

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv


# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()
import funcs


##variables and stuff
logging.basicConfig(filename= "debug.log", level=logging.DEBUG)
fullDex = funcs.loadDex()
logging.info("dex loaded")
target = fullDex[0]
guesses = list()
guessTracker = 0
fullDexLength = len(fullDex)
guessStat = list()
for i in range(6):
	guessStat.append([0,0,0,0,0,0])
workingDex = fullDex.copy()

##functions


def win():
	print("Dub Achieved")

def lose():
	print("you are bad at this")







# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = Bot(command_prefix=".")

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
    

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	global target, guesses, guessTracker, workingDex, fullDex
	if message.content == "hello":
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("hey dirtbag")
	if message.content == "ng":
		await message.channel.send("starting new game!")
		target = list()
		logging.info("target nulled")
		guesses.clear()
		logging.info("guesses nulled")
		guessTracker = 0
		logging.info("guess tracker reset")
		guessStat.clear()
		for i in range(6):
			guessStat.append([0,0,0,0,0,0])	
		logging.info("guess stat reset")
		workingDex = fullDex.copy()
		logging.info("working dex reset")
		target = funcs.pickTarget(fullDex)
		await message.channel.send("i picked the target! Go ahead and guess")
	if str(message.content).startswith("-guess "):
		inputStr = message.content[7:]
		try:
			guess = funcs.getDexInfo(workingDex, inputStr)
			if guess != NULL:
				guesses.append(guess)
			else: 
				logging.error("INPUT DOES NOT MATCH POKEMON NAME")
				await message.channel.send("I've never encountered a pokemon by that name... Are you sure that's its name?")
				return
		except AttributeError:
			logging.error("INPUT DOES NOT MATCH POKEMON NAME")
			await message.channel.send("I've never encountered a pokemon by that name... Are you sure that's its name?")
			return
		if target == guesses[guessTracker]: 
			win()
			return
		elif guessTracker == 5: 
			lose()
			return
		cg = guesses[guessTracker]
		funcs.genCheck(cg, target, guessStat, guessTracker)
		funcs.typeCheck(cg, target, guessStat, guessTracker)
		funcs.heightCheck(cg, target, guessStat, guessTracker)
		funcs.weightCheck(cg, target, guessStat, guessTracker)
		await funcs.printGame(guessTracker,guessStat,guesses, message)
		guessTracker = guessTracker+1
		print("guess complete, fail to get " + target[0])
		
# @bot.command()
# async def newgame(ctx, arg):
# 	print("newgame")
# 	global target,guesses,guessTracker,workingDex,fullDex
# 	await ctx.channel.send("starting new game!")
# 	target = list()
# 	logging.info("target nulled")
# 	guesses.clear()
# 	logging.info("guesses nulled")
# 	guessTracker = 0
# 	logging.info("guess tracker reset")
# 	guessStat.clear()
# 	for i in range(6):
# 		guessStat.append([0,0,0,0,0,0])	
# 	logging.info("guess stat reset")
# 	workingDex = fullDex.copy()
# 	logging.info("working dex reset")
# 	target = funcs.pickTarget()
# 	await ctx.channel.send("i picked the target! Go ahead and guess")


    

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)

