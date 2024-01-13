#!/usr/bin/python3


import numpy as np
from numba_pokemon_prngs.mersenne_twister import MersenneTwister
from numba_pokemon_prngs.sha1 import SHA1
from numba_pokemon_prngs.enums import Language, Game, DSType
from keypresses import keypresses
import time
from datetime import date

seeds = []
times = []
dates = []

#Edit these parameters for your DS

timer0 = 0xc7c
ds_mac = 0x9BFB068FE

nature_search = 'Adamant'

file = None

def compute_dates():
	global dates

	months = [4, 8 , 12]
	days = [30, 31, 31]

	for i in range(2050, 2100):
		for idx, k in enumerate(months):
			curdate = date(i, k, days[idx])
			dow = curdate.weekday() + 1

			dates.append( (i, k, days[idx], dow) )


def compute_times():
    global times
    times = []
    for i in range(17, 23):
        for j in range(0, 60):
           for k in range(43, 45):
                  time1 = (i, j, k)
                  times.append(time1)



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

def rngAdvance(prev):
	next=0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next%0x10000000000000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

table = [[50, 100, 100, 100], [50, 50, 100, 100], [30, 50, 100, 100],[25, 30, 50, 100], [20, 25, 33, 50]]

def advance_table(prng):
    count = 0
    for i in range(5):
        for j in range(4):
            if table[i][j] == 100:
                break

            count += 1
            prng = rngAdvance(prng)
            rand = ((prng >> 32) * 101) >> 32
            if rand <= table[i][j]:
                break

    return prng, count

def initial_frame_bw(prng):
    count = 0

    for i in range(5):
        prng, num = advance_table(prng)
        count += num

    return count	

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
		f"Searching {seed['DATE'][0]}/{seed['DATE'][1]}/{seed['DATE'][2]}" +
		"Time: "+"{:02d}".format(int(seed["TIME"][0]))+":"+"{:02d}".format(int(seed["TIME"][1]))+":"+"{:02d}".format(int(seed["TIME"][2]))+"\n" +
		f"Timer0: {hex(seed['TIMER0'])}\n" +
		f"Key Presses: {seed['KEYPRESSES']}\n" 
		f"Lillipup:\n" +
		"IVs: " + str(seed["PUP_INFO"][0][0]) + "\n"
	 	f"Pup Frames: {seed['PUP_INFO'][0][1]} " 	
	) 
	
	file.write("\n\n")

def rand(seed, max):
	return ((seed) >> 32) * max  >> 32


def check_seed_for_pup(seed):
	
	rng = MersenneTwister(np.uint64(seed) >> np.uint32(32))
	stat1 = rng.next() >> np.uint32(27)
	stat2 = rng.next() >> np.uint32(27)
	stat3 = rng.next() >> np.uint32(27)
	stat4 = rng.next() >> np.uint32(27)
	stat5 = rng.next() >> np.uint32(27)
	stat6 = rng.next() >> np.uint32(27)

	if(stat1 >= 30 and stat2 == 31 and stat3 >= 30 and stat5 >= 30 and stat6 == 31 ):
		return [stat1, stat2, stat3, stat4, stat5, stat6]

def getPups(seed, initial_frame):

	pups = []
	ivs = check_seed_for_pup(seed)
	
	if(ivs is None):
		return []

	cur_seed = rngOf(seed, initial_frame)
	for x in range(initial_frame + 10, initial_frame + 60):
		res = pokeGen(cur_seed, x)

		if(res[0]                       #encounterable
			and res[3] in [9,11]        #encounter slots
			and res[4] == "Adamant"     #nature
			and res[-1] == 1):          #ability

			# pups.append(f"{ivs} {res[1]} {res[-2:]}")
			pups.append([ivs, res[1], res[-2:]])

		cur_seed = rngAdvance(seed)

	return pups

def mine_seeds(sha1, precompute, d):
	global times, timer0, file

	seeds_found = 0
	total_seeds = 0

	for time in times:
		for presses in keypresses:

			total_seeds += 1
			seed = {}
			sha1.set_button(presses[0])
			sha1.set_time(*time)

			seed["SEED"] = sha1.hash_seed(precompute)

			seed["INIT_FRAME"] = initial_frame_bw(seed["SEED"])
			seed["PUP_INFO"] = getPups(seed["SEED"], seed["INIT_FRAME"])

			#Make these checks as early as possible to save time
			if(len(seed["PUP_INFO"]) < 1 ):
				continue
		
			seed["DATE"] = d
			seed["TIMER0"] = timer0
			seed["TIME"] = time
			seed["KEYPRESSES"] = presses[1]


			add_seed_to_list(seed)
			seeds_found = seeds_found + 1

	return seeds_found, total_seeds


def main():
	global seeds, timer0, file, ds_mac

	start = time.time()

	seeds_found = 0
	total_seeds = 0

	sha1 = SHA1(version = Game.BLACK, language = Language.ENGLISH, ds_type=DSType.DS, mac = ds_mac, soft_reset=False, v_frame=8, gx_state=6 )
	sha1.set_timer0(timer0, 0x60)
	
	print("Computing dates...")
	compute_dates()
	
	print("Computing times...")
	compute_times()
	
	try:
		file = open(f"tts_pup_{hex(timer0)}.txt", "w", encoding="UTF-8")
	except IOError:
		print("Error trying to prep outfile")
		exit()

	print("Begin!")

	for d in dates:	

		print(f"{seeds_found} found out of {total_seeds} so far")
		
		print(f"Searching {d[0]}/{d[1]}/{d[2]}")
		
		sha1.set_date(*d)
		precompute = sha1.precompute()


		tmp_seeds_found, tmp_total_seeds = mine_seeds(sha1, precompute, d)

		seeds_found += tmp_seeds_found
		total_seeds += tmp_total_seeds

	file.close()

	end = time.time()
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print(f"Out of {total_seeds} searched {seeds_found} found in" + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


def test():
	getPups(0x3234cc9d923a8e64, 47)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		if(not file.closed):
			file.close()