#!/usr/bin/python3


import numpy as np
# import matplotlib.pyplot as plt
from numba_pokemon_prngs.mersenne_twister import MersenneTwister
import itertools
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType
from MT import MT
from keypresses import keypresses
import time

seeds = []
times = []

#Edit these parameters for your DS

month = 4
day = 30
year = 2008
dow = 3

timer0 = 0xc7c
ds_mac = 0x9BFB068FE


file = None

natures=['Hardy','Lonely','Brave','Adamant',
         'Naughty','Bold','Docile','Relaxed',
         'Impish','Lax','Timid','Hasty',
         'Serious','Jolly','Naive','Modest',
         'Mild','Quiet','Bashful','Rash',
         'Calm','Gentle','Sassy','Careful','Quirky']


def getLandSlot(sel):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    for x in range(0,12):
        if sel < parts[x]:
            return x

def compute_times():
	global times
	times = []
	i = 4
	j = 46
	for k in range(56, 57):
		time1 = (i, j, k)
		times.append(time1)

def rngAdvance(prev):
	next=0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next%0x10000000000000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

def getUInt(seed, max):
    return ((seed >> 32) * max) >> 32

	

def pokeGen(seed,frame):
	trigger = rngOf(seed,frame+2)
	slot = rngAdvance(trigger)
	ability = rngAdvance(slot)
	ability = rngAdvance(ability)
	pokenat = rngAdvance(ability)
	isEncounter = int((((trigger>>32)*0xFFFF)>>32)/0x290)
	if isEncounter <20:
		appear = True
	else:
		appear = False
	sel =((slot>>32)*100)>>32
	natsel = ((pokenat>>32)*25)>>32
	ability = ((ability>>32^0x10000^0x80000000)>>16)&1
	return [appear,frame,isEncounter,getLandSlot(sel),natures[natsel],ability]


def add_seed_to_list(seed):
	global file
	file.write(
		f"Seed: {hex(seed['SEED'])}\n" + 
		"Time: "+"{:02d}".format(int(seed["TIME"][0]))+":"+"{:02d}".format(int(seed["TIME"][1]))+":"+"{:02d}".format(int(seed["TIME"][2]))+"\n" +
		f"Timer0: {hex(seed['TIMER0'])}\n" +
		f"Key Presses: {seed['KEYPRESSES']}\n"
		f"Snivy:\n" +
		str(seed["SNIVY_INFO"]) + "\n")

	file.write("\n\n")

def rand(seed, max):
	return ((seed) >> 32) * max  >> 32


def check_seed_for_snivy(seed):

	rng = MersenneTwister(np.uint64(seed) >> np.uint32(32))
	rng.advance(1) #initialize 
	rng.advance(9) #lowest IV frame from New game
		
	stat1 = rng.next() >> np.uint32(27)
	stat2 = rng.next() >> np.uint32(27)
	stat3 = rng.next() >> np.uint32(27)
	stat4 = rng.next() >> np.uint32(27)
	stat5 = rng.next() >> np.uint32(27)
	stat6 = rng.next() >> np.uint32(27)
	



	if(stat1 >= 30 and stat2 >= 30):
		return [12, [stat1, stat2, stat3, stat4, stat5, stat6]]

def mine_seeds(sha1, precompute):
	global times, timer0

	seeds_found = 0

	for time in times:
		for presses in keypresses:

			seed = {}
			sha1.set_button(presses[0])
			sha1.set_time(*time)

			seed["SEED"] = sha1.hash_seed(precompute)

			seed["SNIVY_INFO"] = check_seed_for_snivy(seed["SEED"])

			#Make these checks as early as possible to save time
			if(seed["SNIVY_INFO"] is None):
				continue
			
			
			seed["MONTH"] = month

			seed["TIMER0"] = timer0
			seed["TIME"] = time
			seed["KEYPRESSES"] = presses[1]

			add_seed_to_list(seed)
			seeds_found = seeds_found + 1
	return seeds_found


def main():
	global seeds, timer0, file, ds_mac

	start = time.time()

	sha1 = SHA1(version = Game.BLACK, language = Language.ENGLISH, ds_type=DSType.DS, mac = ds_mac, soft_reset=False, v_frame=8, gx_state=6 )
	sha1.set_timer0(timer0, 0x60)
	date = (year, month, day, dow)
	sha1.set_date(*date)
	precompute = sha1.precompute()

	print("Computing times...")
	compute_times()

	try:
		file = open(f"tts_snivy_{hex(timer0)}.txt", "w", encoding="UTF-8")
	except IOError:
		print("Error trying to prep outfile")
		exit()

	print("Begin!")
	seeds_found = mine_seeds(sha1, precompute)

	file.close()

	end = time.time()
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print(str(seeds_found) + " found in {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


def test():
	seed = 0x1712daad4d0f4c7d

	candy_frames = check_seed_for_snivy(seed)
	print(candy_frames)

if __name__ == '__main__':
    main()