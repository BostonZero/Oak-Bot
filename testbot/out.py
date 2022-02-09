import copy
import csv
import logging
import os
from asyncio.windows_events import NULL
from distutils.log import debug
from operator import truediv
from random import randrange
from time import sleep

import discord
from dotenv import load_dotenv

import main


def printGame():
	outString = "Gen\tType 1\tType 2\tHeight\tWeight\tName"
	for num in range(main.guessTracker+1):
		lineSet = "\n"
		
		#check gen
		match main.guessStat[num][0]:
			case 0:
				lineSet.append("✅\t")
			case -1:
				lineSet.append("🔼\t")
			case 1:
				lineSet.append("🔽\t")
		match main.guessStat[num][1]:
			case 0:
				lineSet.append("✅\t")
			case -1:
				lineSet.append("➡️\t")
			case 1:
				lineSet.append("❌\t")
		match main.guessStat[num][2]:
			case 0:
				lineSet.append("✅\t")
			case -1:
				lineSet.append("⬅️\t")
			case 1:
				lineSet.append("❌\t")
		match main.guessStat[num][3]:
			case 0:
				lineSet.append("✅\t")
			case -1:
				lineSet.append("🔼\t")
			case 1:
				lineSet.append("🔽\t")
		match main.guessStat[num][4]:
			case 0:
				lineSet.append("✅\t")
			case -1:
				lineSet.append("🔼\t")
			case 1:
				lineSet.append("🔽\t")
		lineSet.append(main.guesses[num][0])


