import copy
import csv
import logging
import os
from asyncio.windows_events import NULL

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

import funcs

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()



##variables and stuff
logging.basicConfig(filename= "debug.log", level=logging.DEBUG)
fullDex = funcs.loadDex()
logging.info("dex loaded")
target = fullDex[0]
guesses = list()
guessTracker = 0
fullDexLength = len(fullDex)
guessStat = list()
for i in range(7):
	guessStat.append([0,0,0,0,0,0,0])
workingDex = fullDex.copy()

##functions


async def win(message, target):
	print("Dub Achieved")
	await message.channel.send("YOU GOT IT!\n name: {a}\tgen: {b}\ttypes: {c}/{d}\theight: {e}\tweight: {f}\n you managed to narrow it down to {g} pokemon".format(a=target[0],b=target[1],c=target[2],d=target[3],e=target[4],f=target[5],g=guessStat[5][5]))


async def lose(message, target, workingDex):
	print("loser")
	await message.channel.send("Nope, i was thinking of \n name: {a}\tgen: {b}\ttypes: {c}/{d}\theight: {e}\tweight: {f}\n you managed to narrow it down to {g} pokemon".format(a=target[0],b=target[1],c=target[2],d=target[3],e=target[4],f=target[5],g=guessStat[5][5]))
	if guessStat[5][5] < 50:
		outStr = "remaining pokemon: "
		for mon in workingDex:
			outStr = outStr + mon[0] + ", "


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
	elif message.content == "-newgame":
		await message.channel.send("starting new game!")
		target = list()
		logging.info("target nulled")
		guesses.clear()
		logging.info("guesses nulled")
		guessTracker = 0
		logging.info("guess tracker reset")
		guessStat.clear()
		for i in range(7):
			guessStat.append([0,0,0,0,0,0,0])	
		logging.info("guess stat reset")
		workingDex = fullDex.copy()
		logging.info("working dex reset")
		target = funcs.pickTarget(fullDex)
		await message.channel.send("i picked the target! Go ahead and guess")
	elif str(message.content).startswith("-guess "):
		print("guess command recognized")
		inputStr = message.content[7:]
		try:
			guess = funcs.getDexInfo(fullDex, inputStr)
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
			await win(message, target)
			return
		elif guessTracker == 7: 
			await lose(message, target, workingDex)
			return
		cg = guesses[guessTracker]
		funcs.genCheck(cg, target, guessStat, guessTracker)
		funcs.typeCheck(cg, target, guessStat, guessTracker)
		funcs.heightCheck(cg, target, guessStat, guessTracker)
		funcs.weightCheck(cg, target, guessStat, guessTracker)
		funcs.cutDex(cg, workingDex.copy(), guessStat, guessTracker, workingDex)
		await funcs.printGame(guessTracker,guessStat, guesses, message, workingDex,fullDex)
		guessTracker = guessTracker+1
		print("guess complete, fail to get " + target[0])	
	elif str(message.content).startswith("-dex "):
		print("dex command recognized")	
		await message.channel.send("Let me check my PokeDex that I totally invented...")
		temp = funcs.getDexInfo(fullDex, message.content[5:])
		await message.channel.send("Name: {a}\tGen: {b}\tTypes: {c}/{d}\tHeight: {e}\tWeight:{f}".format(a=temp[0],b=str(temp[1]),c=temp[2],d=temp[3],e=str(temp[4]),f=str(temp[5])))
	elif str(message.content).startswith("-cheat target "):
		print("cheat command recognized")
		await message.channel.send("cheat mode active")
		target = funcs.getDexInfo(fullDex, message.content[14:])
	elif message.content == "-credit":
		print("credit command recognized")	
		await message.channel.send("While I did make the bot, I didn't invent the game! Go show the original creator some love:\nhttps://squirdle.fireblend.com/\nhttps://github.com/fireblend/")
	elif message.content == "-help":
		print("help command recognized")
		await message.channel.send("-newgame *starts a newgame*\n-guess [pokemon name] *guesses a pokemon*\n-credit *shows the original creator of the game <3*")
   

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)

