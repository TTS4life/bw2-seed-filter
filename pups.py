#!/usr/bin/python3

from os import listdir, getcwd
from os.path import isfile, join
from file.pokefileFile import pokefileFile


def rngAdvance(prev):
	next= 0x5D588B656C078965 * prev + 0x0000000000269EC3
	return next%0x10000000000000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

def getLandSlot(sel):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    for x in range(0,12):
        if sel<parts[x]:
            return x

def pokeGen(seed,frame):
	trigger = rngOf(seed,frame+2)
	slot = rngAdvance(trigger)
	ability = rngAdvance(slot)
	ability = rngAdvance(ability)
	pokenat = rngAdvance(ability)
	isEncounter = int((((trigger>>32)*0xFFFF)>>32)/0x290)
	if isEncounter < 14:
		appear = True
	else:
		appear = False
	sel =((slot>>32)*100)>>32
	natsel = ((pokenat>>32)*25)>>32
	ability = ((ability>>32^0x10000^0x80000000)>>16)&1
	return [appear,frame,isEncounter,getLandSlot(sel),natures[natsel],ability]

badDates=[[],[],[],[],[1,2,3,4,9,10,13,14,19,20,24,30],[],[],[],[1,2,8,9,10,11,18,19,23,24,29,30],[],[],[],[1,2,3,8,9,12,13,14,18,22,23,24,29,30]]

def pickup(seed, initial_frame):
    pickup = []

    for i in range(260):
        seed = rngAdvance(seed)

    for i in range(261, 700):
        seed = rngAdvance(seed)
        tmp1 = (seed >> 32) * 100
        tmp2 = (tmp1 >> 32)

        # print(i, tmp2)

        if(tmp2 < 10):
            next_frame = rngAdvance(seed)
            tmp1 = (next_frame >> 32) * 100
            tmp2 = (tmp1 >> 32)

            if(tmp2 == 98):
                pickup.append([f"{i}", tmp2])
    return pickup

def getPups(seed, initial_frame):
    
    cur_seed = rngOf(seed, initial_frame)
    pups = []
    for x in range(initial_frame + 10, initial_frame + 40):
        res = pokeGen(cur_seed, x)


        
        if(res[0]                       #encounterable
            and res[3] in [9,11]        #encounter slots
            and res[4] == "Adamant"     #nature
            and res[-1] == 1):          #ability

            pups.append(f"{res[1]} {res[-2:]}")
        
        cur_seed = rngAdvance(seed)

    return pups

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
          

def main(infile, outfile):

    data = PokefinderFile(infile)
    data.open()
    seeds_analyzed = []

    output = open(outfile, "w", encoding="UTF-8")

    while(seed := data.parseLine()):
    

        initial_frame = initial_frame_bw(seed)


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
        output.write(f"Time: {date}\n")
        output.write(f"Timer0: {seed["timer0"]}\n")
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

        seedLst.close()
        output.close()

        print(f"{foundseeds} seeds found out of {seedcount} seeds")

if __name__ == '__main__':    

    out_file = input("file to write results to: ")
    main(out_file)