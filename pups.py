#!/usr/bin/python3

from pathlib import Path
from file.Pokefinderfile import PokefinderFile
from rng.util import Gen5RNG


badDates=[[],[],[],[],[1,2,3,4,9,10,13,14,19,20,24,30],[],[],[],[1,2,8,9,10,11,18,19,23,24,29,30],[],[],[],[1,2,3,8,9,12,13,14,18,22,23,24,29,30]]

def pickup(seed, initial_frame):
	pickup = []

	for i in range(260):
		seed = Gen5RNG.rngAdvance(seed)

	for i in range(261, 700):
		seed = Gen5RNG.rngAdvance(seed)
		tmp1 = (seed >> 32) * 100
		tmp2 = (tmp1 >> 32)

		# print(i, tmp2)

		if(tmp2 < 10):
			next_frame = Gen5RNG.rngAdvance(seed)
			tmp1 = (next_frame >> 32) * 100
			tmp2 = (tmp1 >> 32)

			if(tmp2 == 98):
				pickup.append([f"{i}", tmp2])
	return pickup

def getPups(seed, initial_frame):
	
	cur_seed = Gen5RNG.rngOf(seed, initial_frame)
	pups = []
	for x in range(initial_frame + 10, initial_frame + 80):
		res = Gen5RNG.pokeGen(cur_seed, x)


		
		if(res[0]                       #encounterable
			and res[3] in [9,11]        #encounter slots
			and res[4] == "Adamant"     #nature
			and res[-1] == 1):          #ability

			pups.append(f"{res[1]} {res[-2:]}")
		
		cur_seed = Gen5RNG.rngAdvance(seed)

	return pups

table = [[50, 100, 100, 100], [50, 50, 100, 100], [30, 50, 100, 100],[25, 30, 50, 100], [20, 25, 33, 50]]

def advance_table(prng):
	count = 0
	for i in range(5):
		for j in range(4):
			if table[i][j] == 100:
				break

			count += 1
			prng = Gen5RNG.rngAdvance(prng)
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
		  

def main(infile, outfile):


	#Want to take this file, then get its directory and iterate over every pup file.

	file_path = Path(infile)
	out_path = Path(outfile)

	directory = file_path.parent

	foundseeds = 0
	output = open(outfile, "w", encoding="UTF-8")
	for file in directory.iterdir():
		print(Path.absolute(file), Path.absolute(out_path))
		if file.is_file() and Path.absolute(file) != Path.absolute(out_path):

			data = PokefinderFile(file)
			if not data.open():
				print("Failed to open file")
			
			seeds_analyzed = []


			i = 0
			while(seed := data.parseLine()):
				print(i)
				i += 1

				if seed["seed"] in seeds_analyzed:
					print(f"skipping dupe seed {hex(seed["seed"])}")
					continue

				seeds_analyzed.append(seed["seed"])
			
				print(hex(seed["seed"]))
				initial_frame = initial_frame_bw(seed["seed"])


				month = int(seed["month"])
				print(f"month {month}")
				if month % 4 != 0:
					print("bad month continue")
					continue
				date = int(seed["day"])
				if date in badDates[month]:
					print('bad day continue')
					continue

				pups = getPups(seed["seed"], initial_frame)
				if(len(pups) == 0):
					print("no pups continue")
					continue

				foundseeds += 1

				output.write(f"Seed: {hex(seed["seed"])}\n")
				output.write(f"Time: {seed["date"]}\n")
				output.write(f"Timer0: {hex(seed["timer0"])}\n")
				output.write(f"Keypresses: {seed["keypresses"]}\n")
				output.write(f"IVs: {seed["stats"]} \n")
				output.write(f"Initial Frame: {initial_frame} \n")
				output.write("Lillipups: \n")
				for x in pups:
					output.write(f"{str(pups)}\n")

					# output.write("Pickup: ")
					# for x in pickups:
					#     output.write(f"{str(x)} \n")
					# output.write("\n")
					# output.write("\n\n")
				output.write("\n")

	data.close()	
	output.close()

	print(f"{foundseeds} seeds found out of {len(seeds_analyzed)} seeds")

if __name__ == '__main__':    

	infile = "input.txt"
	out_file = input("file to write results to: ")
	main(infile, out_file)