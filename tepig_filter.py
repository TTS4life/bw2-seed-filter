#!/usr/bin/python3
import os
import tkinter as tk 
from tkinter import ttk
from typing import Optional
from file.SSS4 import SSS4 as TepigFileSSS4
from file.Pokefinderfile import PokefinderFile
from rng.util import Gen5RNG

frame_entering_route20 = 430
frame_exiting_route20 = 490
frame_entering_ranch = 550
frame_exiting_ranch = 615
frame_min_for_candy = 360
frame_max_for_candy = 440

min_tepig_nature = 215
max_tepig_nature = 280

nature_search = "Naughty"

#grotto stuff
grotto_filled = [0] * 20
grotto_subslot = [0] * 20
grotto_slot = [0] * 20

def getBirds(seed):

	r20_encounter_table = {	
		# 0 - spring
		0: ["lv2 pidove","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv3 sunkern", "lv4 sunkern", "lv4 sunkern"],
		1: ["lv2 sunkern","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv3 sunkern", "lv4 sunkern", "lv4 sunkern"],
		2: ["lv2 pidove","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv3 sunkern", "lv4 sunkern", "lv4 sunkern"],
		3: ["lv2 pidove","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv3 sunkern", "lv4 sunkern", "lv4 sunkern"]
	}
	
	birds  = [ ]
	
	
	for x in range(frame_entering_route20,frame_exiting_route20):
		res = Gen5RNG.pokeGen(seed["seed"], x)
		if (res[0] #Encounterable
			and "pidove" in r20_encounter_table[seed["month"] % 4][res[3]] #Enc slot is Pidove  
			and res[4] not in [Gen5RNG.natures[1],Gen5RNG.natures[11],Gen5RNG.natures[16],Gen5RNG.natures[21]] #Nature isn't -def
			): 
			birds.append(f"{x}\t{r20_encounter_table[seed["month"] % 4][res[3]]}\t{res[4]}\t{'Low' if res[2] < 5 else 'High'}")

	# print(birds)
	return birds

def getDucks(seed):
	ranch_enc_slots = ["lv4 lillipup","lv5 azurill","lv5 patrat", "lv5 mareep", "lv5 lillipup", "lv5 psyduck", "lv6 lillipup", "lv7 pidove", "lv5 riolu", "lv7 lillpup", "lv7 riolu", "lv7 lillipup"]
	ducks=[]
	for x in range(frame_entering_ranch,frame_exiting_ranch):
		res = Gen5RNG.pokeGen(seed["seed"], x)
		if (res[0] 									 #Encounterable 
	  		and "psyduck" in ranch_enc_slots[res[3]] #It's a Psyduck 
	  		and res[5]==0):							 #It's ability is Damp
			
			ducks.append(f"{x}\t{ranch_enc_slots[res[3]]}\t{res[4]}\t{'Low' if res[2] < 5 else 'High'}")
	# print(ducks)
	return ducks

def getTID(seed, ivframe, challenge_mode = False):
	
	initial_frame = get_init_frame_id(seed, challenge_mode)
	extra_advances = ivframe - 14 # 1 extra advancement is always made from init_frame for TID 
	tmp = Gen5RNG.rngOf(seed, initial_frame + extra_advances) 
	rand = ((tmp >> 32) * 0xffffffff) >> 32
	tid = rand & 0xffff
	sid = rand >> 16
	return tid

def getPassword(TID):
	passwords = ["RESHIRAM", "ZEKROM", "9909", "7707", "2202"]
	return passwords[TID % 256 % 5]

def getUInt(seed, max):
    return ((seed >> 32) * max) >> 32

def get_init_frame_id(seed, challenge_mode = False):
	count = 7 if challenge_mode else 10

	for i in range(0, 3):
		# Round 1
		count += 1
		seed = Gen5RNG.rngOf(seed, 1)

		# Round 2
		count += 1
		seed = Gen5RNG.rngAdvance(seed)
		if ( getUInt(seed, 101) > 50):
			count += 1
			seed = Gen5RNG.rngOf(seed, 1)

		# Round 3
		count += 1
		seed = Gen5RNG.rngAdvance(seed)
		if (getUInt(seed, 101) > 30):    
			count += 1
			seed = Gen5RNG.rngOf(seed, 1)

		# Round 4
		count += 1
		seed = Gen5RNG.rngAdvance(seed) 
		if (getUInt(seed, 101) > 25):
			count += 1
			seed = Gen5RNG.rngAdvance(seed)
			if (getUInt(seed, 101) > 30):
				count += 1
				seed = Gen5RNG.rngOf(seed, 1)

		# Round 5
		count += 1
		seed = Gen5RNG.rngAdvance(seed)
		if (getUInt(seed, 101) > 20):
			count += 1
			seed = Gen5RNG.rngAdvance(seed) 
			if (getUInt(seed, 101) > 25):
				count += 1
				seed = Gen5RNG.rngAdvance(seed)
				if (getUInt(seed, 101) > 33):
					count += 1
					seed = Gen5RNG.rngOf(seed, 1)

		if( i == 0 ):
			seed = Gen5RNG.rngOf(seed, 1 if challenge_mode else 2)
		elif (i == 1):
			seed = Gen5RNG.rngOf(seed, 2 if challenge_mode else 4)

	return count


def rand_to_slot(rand):
	if(rand == 0):
		return 0
	if(rand <= 4):
		return 1
	if(rand <= 19):
		return 2
	if(rand == 20):
		return 3
	if(rand <=24):
		return 4
	if(rand <= 34):
		return 5
	if(rand <=59):
		return 6
	if(rand == 60):
		return 7
	if(rand <= 64):
		return 8
	if(rand <=74):
		return 9
	if(rand <= 99):
		return 10
	
	return 11


def clear_grottos():
	global grotto_slot, grotto_filled, grotto_slot, grotto_subslot
	grotto_filled = [False] * 20
	grotto_subslot = [0] * 20
	grotto_slot = [0] * 20


#There are 4 total advancements done during grotto check,
# but since idc about checking gender and whatnot, ignoring for now
def grottos_fill(seed):
	global grotto_filled, grotto_subslot, grotto_slot
	#There are 20 grottos, but for route 6 candy we only care about Route 6 which is index 3 of 0->20
	for i in range (0, 20): 
		if(grotto_filled[i] == False):
			seed = Gen5RNG.rngAdvance(seed)
			r = getUInt(seed, 100)
			if(r < 5):
				grotto_filled[i] = True
				seed = Gen5RNG.rngAdvance(seed)
				grotto_subslot[i] = getUInt(seed, 4)
				seed = Gen5RNG.rngAdvance(seed)
				grotto_slot[i] = rand_to_slot(getUInt(seed, 100))
				# print("grotto ", i, " got filled with ", str(grotto_subslot[i]), str(grotto_slot[i]))


def has_candy(grotto_index):
	if(grotto_filled[grotto_index] is True):
		if(grotto_subslot[grotto_index] == 0 and grotto_slot[grotto_index] == 7):
			return True
	return False

def tepig_ability_check(seed):
	global nature_search
	nature_frames = []
	rng = seed
	rng = Gen5RNG.rngOf(rng, min_tepig_nature)
	# -1 is to match RNG Reporter output
	for i in range(min_tepig_nature - 1, max_tepig_nature):
		natsel = Gen5RNG.getUInt(rng, 25)
		if(Gen5RNG.natures[natsel] == nature_search):
			nature_frames.append(i)
		rng = Gen5RNG.rngAdvance(rng)
		
	return nature_frames
	

def has_dragonite_and_zangoose():
	global grotto_filled, grotto_slot, grotto_subslot

	if(grotto_filled[19] is True and grotto_filled[11] is True):
		if(grotto_slot[19] == 0 ): #Dnite is all 4 slots
			if(grotto_subslot[11] in [0, 1] and grotto_slot[11] == 2 ):
				return True
	
	return False


def grotto_check(seed):
	seed = Gen5RNG.rngOf(seed, frame_min_for_candy)
	candy_frames = []

	#The 3 is to make the frames align with what they actually are in game,
	#Not sure where I am actually missing advancements here
	for i in range(frame_min_for_candy + 3, frame_max_for_candy):
		clear_grottos()
		#Attempt to fill grottos on current RNG seed
		grottos_fill(seed)
		#Check R6 grotto for candy
		if(has_candy(3)):
			candy_frames.append(i)

		seed = Gen5RNG.rngAdvance(seed)

	return candy_frames

def processSeed(input_seed, ivframe, month):
	print(f"seed: {input_seed}, ivframe: {ivframe}")

	try:
		seed = {
			"seed": int(input_seed, 16),
			"ivframe": int(ivframe),
			"month": int(month)
		}
	

		seed["NMTID"] = getTID(seed["seed"], seed["ivframe"])
		seed["NMPASS"] = getPassword(seed["NMTID"])

		seed["CMTID"] = getTID(seed["seed"], seed["ivframe"], True)
		seed["CMPASS"] = getPassword(seed["CMTID"])

		seed["ducks"] = getDucks(seed)
		seed["birds"] = getBirds(seed)

		# print("formatting output for " + str(seed))
		output = format_output(seed)

	except Exception as ex:
		raise(ex)

	return output



def processFile(input_file, output_file):
	global nature_search

	# print("Instantiating SSS4 wtih file ", input_file)
	file = PokefinderFile(input_file)
	if not file.open():
		print("failure to open file")
		exit()

	output = open(output_file, "w", encoding="UTF-8")

	seeds = []

	while (seed := file.parseLine()):

		if seed["seed"] in seeds:
			print("skipping dupe seed")
			continue

		seeds.append(seed["seed"])
		
		seed["TEPIG_INFO"] = tepig_ability_check(seed["seed"])
		
		seed["R6GROTTO"] = grotto_check(seed["seed"])
		# if(len(seed["R6GROTTO"]) < 1):
		# 	continue

		seed["NMTID"] = getTID(seed["seed"], int(seed["ivframe"]))
		seed["NMPASS"] = getPassword(seed["NMTID"])

		seed["CMTID"] = getTID(seed["seed"], int(seed["ivframe"]), True)
		seed["CMPASS"] = getPassword(seed["CMTID"])

		seed["ducks"] = getDucks(seed)
		seed["birds"] = getBirds(seed)
		
		if len(seed["birds"]) == 0 or len(seed["ducks"]) == 0:
			print("NO ducks/birds ", len(seeds))
			continue
		
		output.write("Seed: " + str(hex(seed["seed"]))+"\n")
		output.write(f"Time: {seed['date']}\n")
		output.write(f"Timer0: {hex(seed["timer0"])}\n")
		output.write(f"Key Presses: {seed["keypresses"]}\n")
		output.write(f"TID: {seed['NMTID']} ({seed['NMPASS']}), CM: {seed['CMTID']} ({seed['CMPASS']})\n")
		output.write("Tepig:"+"\n")
		output.write(f"{seed["ivframe"]} {seed["stats"]}\n")
		output.write(f"{nature_search} Frames: {seed["TEPIG_INFO"]}\n")
		for x in seed["birds"]:
			output.write(x+"\n")
		for y in seed["ducks"]:
			output.write(y+"\n")
		if("R6GROTTO" in seed and len(seed["R6GROTTO"]) > 0):
			output.write(f"Candy frame: {seed['R6GROTTO']}\n")
		output.write("\n\n")
	file.close()
	output.close()

	print(f"Analyzed {len(seeds)} seeds")

def format_output(seed):
	
	output = f"{seed['seed']}\n"
	output += f"{seed['ivframe']}\n"
	output += f"{seed['month']}\n"
	output += f"TID: {seed['NMTID']} ({seed['NMPASS']})\n"
	output += f"CMTID: {seed['CMTID']} ({seed['CMPASS']})\n"
	
	for bird in seed['birds']:
		tmp = str(bird).replace("\t", "   ")
		output += f"{tmp}\n"

	for duck in seed['ducks']:
		tmp = str(duck).replace("\t", "   ")
		output += f"{tmp}\n"


	return output


def main(input_file, output_file):
	processFile(input_file, output_file)
