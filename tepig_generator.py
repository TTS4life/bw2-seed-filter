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

month = 9
day = 18
year = 2048
dow = 5

timer0 = 0x10f7
ds_mac = 0x9BF6D93CE # Sugar - 9BF6D93CE

nature_search = 'Naughty'

file = None

#Edit these for frame windows for different things. Only the lack of doves/ducks 
# will cause a seed to not appear in the final product. Candy will only appear in output if
# A candy frame is found in given range
frame_entering_route20 = 430
frame_exiting_route20 = 490
frame_entering_ranch = 550
frame_exiting_ranch = 615
frame_min_for_candy = 360
frame_max_for_candy = 440

min_tepig_nature = 215
max_tepig_nature = 275



grotto_filled = [0] * 20
grotto_subslot = [0] * 20
grotto_slot = [0] * 20

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
    for i in range(0, 24):
        for j in range(0, 60):
           for k in range(0, 60):
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

def tepig_ability_check(seed):
	global nature_search
	nature_frames = []
	rng = seed
	rng = rngOf(rng, min_tepig_nature)
	# -1 is to match RNG Reporter output
	for i in range(min_tepig_nature - 1, max_tepig_nature):
		natsel = rand(rng, 25)
		if(natures[natsel] == nature_search):
			nature_frames.append(i)
		rng = rngAdvance(rng)
		
	return nature_frames
	

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

def getBirds(seed):
	route_20_summer = ["lv2 sunkern","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv3 sunkern", "lv4 sunkern", "lv4 sunkern"]
	route_20_encounters = ["lv2 pidove","lv2 sewaddle","lv3 patrat", "lv3 purrloin", "lv3 patrat", "lv3 sewaddle", "lv4 pidove", "lv4 sewaddle", "lv4 purrloin", "lv4 sunkern", "lv4 purrloin", "lv4 sunkern"]
	birds  = [ ]
	pidove_slots = []
	
	if(seed["MONTH"] % 4 == 2): #summer
		pidove_slots = [ 6 ]
		slots = route_20_summer
	else:
		pidove_slots = [ 0, 6 ]
		slots = route_20_encounters
	
	for frame in range(frame_entering_route20,frame_exiting_route20):
		res = pokeGen(seed["SEED"], frame)
		
		if(res[0] #encounterable 
	 		and res[3] in pidove_slots ):	
			check_type = "Low" if res[2]<5 else "High"

			birds.append(f"{res[1]}\t{slots[res[3]]}\t{res[4]}\t{res[5]}\t{check_type}")


	return birds

def getDucks(seed):
	ranch_encounter_slots = ["lv4 lillipup","lv5 azurill","lv5 patrat", "lv5 mareep", "lv5 lillipup", "lv5 psyduck", "lv6 lillipup", "lv7 pidove", "lv5 riolu", "lv7 lillpup", "lv7 riolu", "lv7 lillipup"]
	ducks=[]
	for x in range(frame_entering_ranch,frame_exiting_ranch):
		res = pokeGen(seed["SEED"], x)
		if res[0] and res[3]==5 and res[5]==0:
			if res[2]<5:
				ducks.append(str(res[1])+"\t"+ranch_encounter_slots[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" Low")
			else:
				ducks.append(str(res[1])+"\t"+ranch_encounter_slots[int(res[3])]+"\t"+res[4]+"\t"+str(res[5])+" High")
	return ducks

def get_init_frame_id(seed, challenge_mode = False):
	count = 7 if challenge_mode else 10

	for i in range(0, 3):
		# Round 1
		count += 1
		seed = rngOf(seed, 1)

		# Round 2
		count += 1
		seed = rngAdvance(seed)
		if ( getUInt(seed, 101) > 50):
			count += 1
			seed = rngOf(seed, 1)

		# Round 3
		count += 1
		seed = rngAdvance(seed)
		if (getUInt(seed, 101) > 30):    
			count += 1
			seed = rngOf(seed, 1)

		# Round 4
		count += 1
		seed = rngAdvance(seed) 
		if (getUInt(seed, 101) > 25):
			count += 1
			seed = rngAdvance(seed)
			if (getUInt(seed, 101) > 30):
				count += 1
				seed = rngOf(seed, 1)

		# Round 5
		count += 1
		seed = rngAdvance(seed)
		if (getUInt(seed, 101) > 20):
			count += 1
			seed = rngAdvance(seed) 
			if (getUInt(seed, 101) > 25):
				count += 1
				seed = rngAdvance(seed)
				if (getUInt(seed, 101) > 33):
					count += 1
					seed = rngOf(seed, 1)

		if( i == 0 ):
			seed = rngOf(seed, 1 if challenge_mode else 2)
		elif (i == 1):
			seed = rngOf(seed, 2 if challenge_mode else 4)

	return count

def getTID(seed, ivframe, challenge_mode = False):
	
	initial_frame = get_init_frame_id(seed, challenge_mode)
	extra_advances = ivframe - 14 # 1 extra advancement is always made from init_frame for TID 
	tmp = rngOf(seed, initial_frame + extra_advances) 
	rand = ((tmp >> 32) * 0xffffffff) >> 32
	tid = rand & 0xffff
	sid = rand >> 16
	return tid

def getPassword(TID):
	passwords = ["RESHIRAM", "ZEKROM", "9909", "7707", "2202"]
	return passwords[TID % 256 % 5]

def add_seed_to_list(seed):
	global file
	file.write(
		f"Seed: {hex(seed['SEED'])}\n" + 
		"Time: "+"{:02d}".format(int(seed["TIME"][0]))+":"+"{:02d}".format(int(seed["TIME"][1]))+":"+"{:02d}".format(int(seed["TIME"][2]))+"\n" +
		f"Timer0: {hex(seed['TIMER0'])}\n" +
		f"Key Presses: {seed['KEYPRESSES']}\n"
		f"TID: {seed['NMTID']} ({seed['NMPASS']}), CM: {seed['CMTID']} ({seed['CMPASS']})\n" +
		f"Tepig:\n" +
		str(seed["TEPIG_INFO"]) + "\n")
	
	if(len(seed["R6GROTTO"]) > 0):
		file.write(f"Route 6 Grotto Candy Frames: {seed['R6GROTTO']}\n")
	
	for x in seed["DOVES"]:
		file.write(f"{x}\n")
	
	for x in seed["DUCKS"]:
		file.write(f"{x}\n")

	file.write("\n\n")

def rand(seed, max):
	return ((seed) >> 32) * max  >> 32

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


def check_seed_for_tepig(seed):

	rng = MersenneTwister(np.uint64(seed) >> np.uint32(32))
	rng.advance(1) #initialize 
	rng.advance(15) #lowest IV frame from New game
		
	stat1 = rng.next() >> np.uint32(27)
	stat2 = rng.next() >> np.uint32(27)
	stat3 = rng.next() >> np.uint32(27)
	stat4 = rng.next() >> np.uint32(27)
	stat5 = rng.next() >> np.uint32(27)
	stat6 = rng.next() >> np.uint32(27)
	stat7 = rng.next() >> np.uint32(27)
	stat8 = rng.next() >> np.uint32(27)


	if nature_search == 'Naughty':
		if(stat1 >= 27 and stat2 >= 29 and stat3 >= 29 and stat4 >= 29 and stat6 == 25 ):
			return [15, [stat1, stat2, stat3, stat4, stat5, stat6], tepig_ability_check(seed)]

		if(stat2 >= 27 and stat3 >= 29 and stat4 >= 29 and stat5 >= 29 and stat7 == 25):
			return [16, [stat2, stat3, stat4, stat5, stat6, stat7], tepig_ability_check(seed)]
			
		# if(stat3 >= 27 and stat4 >= 29 and stat5 >= 29 and stat6 >= 29 and stat8 == 25):
		# 	return [17, [stat3, stat4, stat5, stat6, stat7, stat8], tepig_ability_check(seed)]

	#28/29/30/30/20/30
	if nature_search == 'Rash':
		if(stat1 >= 27 and stat2 >= 29 and stat3 >= 29 and stat4 >= 29 and stat6 >= 26 ):
			return [15, [stat1, stat2, stat3, stat4, stat5, stat6], tepig_ability_check(seed)]
		if(stat2 >= 27 and stat3 >= 29 and stat4 >= 29 and stat5 >= 29 and stat7 >= 26):
			return [16, [stat2, stat3, stat4, stat5, stat6, stat7], tepig_ability_check(seed)]	
		# if(stat3 >= 28 and stat4 >= 29 and stat5 >= 30 and stat6 >= 30 and stat7 >= 20 and stat8 >= 30):
		# 		return [17, [stat3, stat4, stat5, stat6, stat7, stat8], tepig_ability_check(seed)]
		


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
	for i in range (0, 5): 
		if(grotto_filled[i] == False):
			seed = rngAdvance(seed)
			r = rand(seed, 100)
			if(r < 5):
				grotto_filled[i] = True
				seed = rngAdvance(seed)
				grotto_subslot[i] = rand(seed, 4)
				seed = rngAdvance(seed)
				grotto_slot[i] = rand_to_slot(rand(seed, 100))
				# print("grotto ", i, " got filled with ", str(grotto_subslot[i]), str(grotto_slot[i]))


def has_candy(grotto_index):
	if(grotto_filled[grotto_index] is True):
		if(grotto_subslot[grotto_index] == 0 and grotto_slot[grotto_index] == 7):
			return True
	return False


def grotto_check(seed):
	seed = rngOf(seed, frame_min_for_candy)
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

		seed = rngAdvance(seed)

	return candy_frames

def mine_seeds(sha1, precompute):
	global times, timer0

	seeds_found = 0

	for time in times:
		for presses in keypresses:

			seed = {}
			sha1.set_button(presses[0])
			sha1.set_time(*time)

			seed["SEED"] = sha1.hash_seed(precompute)
			seed["MONTH"] = month

			seed = gather_seed_info(seed)

			if seed is None:
				continue
			
			seed["TIMER0"] = timer0
			seed["TIME"] = time
			seed["KEYPRESSES"] = presses[1]



			add_seed_to_list(seed)
			seeds_found = seeds_found + 1
	return seeds_found

def gather_seed_info(seed):

	seed["TEPIG_INFO"] = check_seed_for_tepig(seed["SEED"])
	#Make these checks as early as possible to save time
	if(seed["TEPIG_INFO"] is None or len(seed["TEPIG_INFO"][2]) < 1):
		return None

	seed["R6GROTTO"] = grotto_check(seed["SEED"])
	if(len(seed["R6GROTTO"]) < 1):
		return None

	seed["DUCKS"] = getDucks(seed)
	seed["DOVES"] = getBirds(seed)

	seed["NMTID"] = getTID(seed["SEED"], seed["TEPIG_INFO"][0])
	seed["NMPASS"] = getPassword(seed["NMTID"])

	seed["CMTID"] = getTID(seed["SEED"], seed["TEPIG_INFO"][0], True)
	seed["CMPASS"] = getPassword(seed["CMTID"])

	if(len(seed["DUCKS"]) == 0 or len(seed["DOVES"]) == 0):
		return None
	
	return seed



def main():
	global seeds, timer0, file, ds_mac

	start = time.time()

	sha1 = SHA1(version = Game.WHITE2, language = Language.ENGLISH, ds_type=DSType.DS, mac = ds_mac, soft_reset=False, v_frame=8, gx_state=6 )
	sha1.set_timer0(timer0, 0x82)
	date = (year, month, day, dow)
	sha1.set_date(*date)
	precompute = sha1.precompute()

	print("Computing times...")
	compute_times()

	try:
		file = open(f"tts_{nature_search}_{hex(timer0)}.txt", "w", encoding="UTF-8")
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
	seed = {"SEED": 0x8b83adc5f4516a00,
		 	"MONTH": 3}
	gather_seed_info(seed)
	print(seed)
	

if __name__ == '__main__':
    main()